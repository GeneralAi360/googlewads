import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZE = ROOT / "scripts" / "materialize_review_jobs.py"
ASSESS = ROOT / "scripts" / "assess_pack_readiness.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ReviewReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.materializer = load(MATERIALIZE, "materialize_review_jobs")
        cls.assessor = load(ASSESS, "assess_pack_readiness")

    def fixture(self, root: Path, count: int = 2):
        rows = []
        files = []
        for index in range(1, count + 1):
            job = f"C01-S300x250-V{index:02d}-Lru"
            output = root / f"{job}.png"
            output.write_bytes(f"banner-{index}".encode())
            digest = self.assessor.sha256_file(output)
            rows.append({"job_id": job, "concept_id": "C01", "variant_id": f"V{index:02d}", "language": "ru", "width": 300, "height": 250, "layout_family": "rectangle", "output_path": output.as_posix()})
            files.append({"job_id": job, "concept_id": "C01", "variant_id": f"V{index:02d}", "language": "ru", "path": output.as_posix(), "sha256": digest, "width": 300, "height": 250, "status": "PASS"})
        matrix = {"run_id": "review-demo", "expected_output_files": count, "banner_matrix": rows}
        manifest = {"campaign_id": "review-demo", "files": files}
        manifest_path = root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return matrix, manifest, manifest_path

    def banner_review(self, item, independent=True, status="PASS"):
        value = "PASS" if status == "PASS" else "FAIL"
        return {
            "job_id": item["job_id"],
            "reviewer_role": "DESIGN_REVIEWER",
            "independent_context": independent,
            "reviewed_output_path": item["path"],
            "reviewed_output_sha256": item["sha256"],
            "status": status,
            "checks": {
                "concept_fidelity": value,
                "brand_fidelity": value,
                "asset_quality": value,
                "professional_category_fit": value,
                "visual_hierarchy": value,
                "lighting_focal_guidance": value,
                "typography_legibility": value,
                "color_contrast": value,
                "information_density": value,
                "crop_safe_zones": value,
                "cta_clarity": value,
                "anti_generic_ai": value,
                "actual_size_check": value,
            },
            "findings": [],
        }

    def pack_review(self, manifest_path, independent=True, status="PASS"):
        value = "PASS" if status == "PASS" else "FAIL"
        return {
            "reviewer_role": "PACK_REVIEWER",
            "independent_context": independent,
            "manifest_sha256": self.assessor.sha256_file(manifest_path),
            "status": status,
            "checks": {
                "all_expected_files_present": value,
                "no_unintended_duplicates": value,
                "cross_size_concept_consistency": value,
                "brand_consistency": value,
                "professional_category_consistency": value,
                "asset_quality_consistency": value,
                "intentional_layout_adaptation": value,
                "small_format_simplification": value,
                "contact_sheet_review": value,
            },
            "findings": [],
        }

    def write_passing_reviews(self, root, manifest, manifest_path, independent=True):
        review_dir = root / "reviews"
        review_dir.mkdir()
        for item in manifest["files"]:
            (review_dir / f"{item['job_id']}.review.json").write_text(json.dumps(self.banner_review(item, independent=independent)), encoding="utf-8")
        pack_path = root / "pack-review.json"
        pack_path.write_text(json.dumps(self.pack_review(manifest_path, independent=independent)), encoding="utf-8")
        return review_dir, pack_path

    def test_materializer_creates_one_readonly_task_per_banner_and_pack_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root)
            result = self.materializer.materialize_reviews(matrix, manifest, root / "review-run", manifest_path=manifest_path, contact_sheet_path=root / "contact.png")
            self.assertEqual(result["expected_banner_reviews"], 2)
            self.assertEqual(len(result["banner_reviews"]), 2)
            self.assertTrue((root / "review-run" / "pack-review-task.md").is_file())
            self.assertFalse((root / "review-run" / "pack-review.json").exists())
            self.assertTrue(all(Path(item["task_path"]).is_file() for item in result["banner_reviews"]))
            self.assertFalse(result["design_qa_attached"])
            task = Path(result["banner_reviews"][0]["task_path"]).read_text(encoding="utf-8")
            self.assertIn("asset quality", task)
            self.assertIn("professional category fit", task)
            self.assertIn("anti-generic-AI", task)

    def test_materializer_attaches_hash_bound_design_qa_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            item = manifest["files"][0]
            qa_root = root / "qa"
            qa_root.mkdir()
            views = {
                "actual": item["path"],
                "grayscale": (qa_root / "grayscale.png").as_posix(),
                "squint": (qa_root / "squint.png").as_posix(),
                "thumbnail_board": (qa_root / "thumbnail-board.png").as_posix(),
            }
            for name, path in views.items():
                if name != "actual":
                    Path(path).write_bytes(b"diagnostic")
            qa_index = {
                "artifact_role": "DESIGN_QA_DIAGNOSTICS_ONLY",
                "delivery_asset": False,
                "jobs": [
                    {
                        "job_id": item["job_id"],
                        "source_sha256": item["sha256"],
                        "views": views,
                    }
                ],
            }
            qa_path = root / "design-qa-index.json"
            qa_path.write_text(json.dumps(qa_index), encoding="utf-8")
            result = self.materializer.materialize_reviews(
                matrix,
                manifest,
                root / "review-run",
                manifest_path=manifest_path,
                qa_index_path=qa_path,
            )
            self.assertTrue(result["design_qa_attached"])
            self.assertTrue(result["banner_reviews"][0]["design_qa_attached"])
            task = Path(result["banner_reviews"][0]["task_path"]).read_text(encoding="utf-8")
            self.assertIn("25% glance board", task)
            self.assertIn("Grayscale hierarchy", task)
            self.assertIn("Squint/blur hierarchy", task)

    def test_materializer_rejects_stale_design_qa_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            item = manifest["files"][0]
            qa_path = root / "design-qa-index.json"
            qa_path.write_text(
                json.dumps(
                    {
                        "jobs": [
                            {
                                "job_id": item["job_id"],
                                "source_sha256": "0" * 64,
                                "views": {
                                    "actual": item["path"],
                                    "grayscale": "g.png",
                                    "squint": "s.png",
                                    "thumbnail_board": "t.png",
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(self.materializer.ReviewMaterializeError) as ctx:
                self.materializer.materialize_reviews(
                    matrix,
                    manifest,
                    root / "review-run",
                    manifest_path=manifest_path,
                    qa_index_path=qa_path,
                )
            self.assertIn("stale design QA", str(ctx.exception))

    def test_missing_banner_reviews_block_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root)
            review_dir = root / "reviews"
            review_dir.mkdir()
            pack_path = root / "pack-review.json"
            pack_path.write_text(json.dumps(self.pack_review(manifest_path)), encoding="utf-8")
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path)
            self.assertEqual(result["status"], "REVIEW_INCOMPLETE")
            self.assertFalse(result["completion_claim_allowed"])

    def test_all_exact_artifact_independent_reviews_allow_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root)
            review_dir, pack_path = self.write_passing_reviews(root, manifest, manifest_path)
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path)
            self.assertEqual(result["status"], "READY")
            self.assertEqual(result["delivery_status"], "COMPLETE")
            self.assertEqual(result["run_rigor"], "FULL")
            self.assertTrue(result["completion_claim_allowed"])

    def test_asset_quality_failure_blocks_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            review_dir, pack_path = self.write_passing_reviews(root, manifest, manifest_path)
            review_path = next(review_dir.glob("*.review.json"))
            review = json.loads(review_path.read_text())
            review["checks"]["asset_quality"] = "FAIL"
            review["status"] = "FAIL"
            review_path.write_text(json.dumps(review), encoding="utf-8")
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path)
            self.assertEqual(result["status"], "REVIEW_FAILED")
            self.assertFalse(result["completion_claim_allowed"])

    def test_stale_banner_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            review_dir, pack_path = self.write_passing_reviews(root, manifest, manifest_path)
            review_path = next(review_dir.glob("*.review.json"))
            review = json.loads(review_path.read_text())
            review["reviewed_output_sha256"] = "0" * 64
            review_path.write_text(json.dumps(review), encoding="utf-8")
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path)
            self.assertEqual(result["status"], "REVIEW_FAILED")
            self.assertIn("stale", result["failed_banner_reviews"][0]["reason"])

    def test_non_independent_review_blocks_full_rigor_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            review_dir, pack_path = self.write_passing_reviews(root, manifest, manifest_path, independent=False)
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path)
            self.assertEqual(result["status"], "REVIEW_FAILED")
            self.assertEqual(result["run_rigor"], "DEGRADED")
            self.assertFalse(result["completion_claim_allowed"])

    def test_degraded_review_can_report_complete_delivery_when_explicitly_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            review_dir, pack_path = self.write_passing_reviews(root, manifest, manifest_path, independent=False)
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path, require_independent=False)
            self.assertEqual(result["status"], "READY")
            self.assertEqual(result["delivery_status"], "COMPLETE")
            self.assertEqual(result["run_rigor"], "DEGRADED")
            self.assertTrue(result["completion_claim_allowed"])

    def test_pack_review_failure_blocks_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, manifest, manifest_path = self.fixture(root, count=1)
            review_dir, pack_path = self.write_passing_reviews(root, manifest, manifest_path)
            pack_path.write_text(json.dumps(self.pack_review(manifest_path, status="FAIL")), encoding="utf-8")
            result = self.assessor.assess_readiness(matrix, manifest, review_dir, pack_path, manifest_path=manifest_path)
            self.assertEqual(result["status"], "REVIEW_FAILED")
            self.assertFalse(result["completion_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
