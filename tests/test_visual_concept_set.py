import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_visual_concept_set.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_visual_concept_set", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualConceptSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def commercial_job(self):
        return {
            "commercial_job_id": "CJ-B24-LICENSE-001",
            "status": "COMMERCIAL_JOB_LOCKED",
            "product_or_service": "Bitrix24 license",
            "job_type": "PURCHASE_OR_RENEWAL",
            "purchase_renewal_structure": "SEPARATE_VARIANTS",
            "target_transaction": "purchase or renew a Bitrix24 license",
            "allowed_message_scope": ["license purchase", "license renewal"],
            "excluded_job_types": ["IMPLEMENTATION_SERVICE", "CONSULTATION"],
            "source_basis": "USER_EXPLICIT",
            "source_note": None,
            "change_requires_controller_reapproval": True,
        }

    def quality(self):
        return {
            "reviewed_by": "ART_DIRECTOR_REVIEWER",
            "status": "PASS",
            "checks": {key: "PASS" for key in (
                "commercial_job_fidelity",
                "professional_category_fit",
                "ad_not_presentation_slide",
                "hierarchy",
                "typography",
                "cta_integration",
                "visual_distinctiveness",
                "anti_template",
                "small_format_viability",
            )},
            "notes": "Synthetic pre-show quality review",
        }

    def concept(self, root: Path, suffix: str, axes: dict[str, str]):
        artifact = root / f"concept-{suffix}.png"
        artifact.write_bytes(f"visual-{suffix}".encode())
        preview = {
            "visual_concept_id": f"VC-{suffix}",
            "commercial_job_id": "CJ-B24-LICENSE-001",
            "status": "VISUAL_CONCEPT_RENDERED",
            "artifact_path": artifact.as_posix(),
            "artifact_sha256": self.module.sha256_file(artifact),
            "width": 300,
            "height": 250,
            "approval_scope": "VISUAL_SYSTEM_WITH_ASSET_SLOTS",
            "concept_summary": {
                "core_idea": f"concept {suffix}",
                "commercial_angle": "purchase or renewal of Bitrix24 license",
                "primary_aoi": "license decision",
                "scan_path": ["commercial hook", "product cue", "CTA", "brand"],
                "style_strategy": "synthetic strategy",
                "typography": "enterprise Cyrillic sans",
                "lighting": "restrained",
                "adaptation_note": "preserve commercial job in micro formats",
            },
            "asset_slots": [
                {
                    "asset_id": "logo",
                    "role": "LOGO",
                    "preview_mode": "TEXT_BRAND_PLACEHOLDER",
                    "production_ready": False,
                    "generated_fake_asset": False,
                    "source": None,
                    "notes": "Concept-only brand anchor",
                }
            ],
            "production_asset_readiness": "NEEDS_ASSET",
            "not_for_delivery": True,
            "policy_note": "Synthetic fixture",
        }
        preview_path = root / f"preview-{suffix}.json"
        preview_path.write_text(json.dumps(preview, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "visual_concept_id": f"VC-{suffix}",
            "label": f"Concept {suffix}",
            "preview_contract_path": preview_path.as_posix(),
            "preview_contract_sha256": self.module.sha256_file(preview_path),
            "artifact_path": artifact.as_posix(),
            "artifact_sha256": self.module.sha256_file(artifact),
            "design_axes": axes,
            "quality_review": self.quality(),
        }

    def concept_set(self, root: Path, *, mode="EXPLORE_3", source="INTERNAL_RECOMMENDATION"):
        concepts = [
            self.concept(root, "A", {
                "hero_logic": "license decision typography",
                "composition_system": "asymmetric type-led field",
                "attention_profile": "offer first",
                "typography_profile": "bold enterprise grotesk",
                "graphic_device": "license keyline system",
                "lighting_language": "flat high-clarity",
            }),
            self.concept(root, "B", {
                "hero_logic": "product edition selector",
                "composition_system": "split product-choice grid",
                "attention_profile": "product proof first",
                "typography_profile": "technical information sans",
                "graphic_device": "edition modules",
                "lighting_language": "restrained dimensional separation",
            }),
            self.concept(root, "C", {
                "hero_logic": "renewal continuity signal",
                "composition_system": "editorial diagonal flow",
                "attention_profile": "typographic statement",
                "typography_profile": "condensed commercial sans",
                "graphic_device": "continuity rail",
                "lighting_language": "quiet contrast spotlight",
            }),
        ]
        if mode == "SINGLE_USER_LOCKED":
            concepts = concepts[:1]
        sheet = root / "concept-contact-sheet.png"
        sheet.write_bytes(b"contact-sheet")
        return {
            "concept_set_id": "VCS-001",
            "status": "VISUAL_CONCEPT_SET_RENDERED",
            "commercial_job_id": "CJ-B24-LICENSE-001",
            "commercial_job_sha256": self.module.canonical_sha(self.commercial_job()),
            "mode": mode,
            "direction_lock_source": source,
            "user_lock_evidence": "User explicitly chose direction A" if source == "USER_LOCKED" else None,
            "representative_size": "300x250",
            "concepts": concepts,
            "comparison_contact_sheet_path": sheet.as_posix(),
            "comparison_contact_sheet_sha256": self.module.sha256_file(sheet),
        }

    def test_unlocked_first_round_requires_three_and_passes_when_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.module.validate(self.commercial_job(), self.concept_set(root))
            self.assertEqual(result["status"], "VISUAL_CONCEPT_SET_AWAITING_USER_SELECTION")
            self.assertEqual(result["visual_exploration_count"], 3)
            self.assertTrue(all(item["distinct_axes"] >= 3 for item in result["pairwise_distinction"]))
            self.assertFalse(result["full_production_allowed"])

    def test_internal_recommendation_is_not_user_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept_set = self.concept_set(root, mode="SINGLE_USER_LOCKED", source="INTERNAL_RECOMMENDATION")
            with self.assertRaises(self.module.VisualConceptSetError):
                self.module.validate(self.commercial_job(), concept_set)

    def test_explicit_user_lock_allows_single_concept(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept_set = self.concept_set(root, mode="SINGLE_USER_LOCKED", source="USER_LOCKED")
            result = self.module.validate(self.commercial_job(), concept_set)
            self.assertEqual(result["visual_exploration_count"], 1)
            self.assertEqual(result["direction_lock_source"], "USER_LOCKED")

    def test_palette_swap_level_similarity_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept_set = self.concept_set(root)
            concept_set["concepts"][1]["design_axes"] = dict(concept_set["concepts"][0]["design_axes"])
            concept_set["concepts"][1]["design_axes"]["lighting_language"] = "slightly different color light"
            with self.assertRaises(self.module.VisualConceptSetError):
                self.module.validate(self.commercial_job(), concept_set)

    def test_presentation_slide_like_concept_fails_before_user_show(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept_set = self.concept_set(root)
            concept_set["concepts"][0]["quality_review"]["checks"]["ad_not_presentation_slide"] = "FAIL"
            with self.assertRaises(self.module.VisualConceptSetError):
                self.module.validate(self.commercial_job(), concept_set)

    def test_stale_commercial_job_binding_rejects_concept_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept_set = self.concept_set(root)
            concept_set["commercial_job_id"] = "CJ-OLD-IMPLEMENTATION"
            with self.assertRaises(self.module.VisualConceptSetError):
                self.module.validate(self.commercial_job(), concept_set)

    def test_preview_bound_to_old_commercial_job_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept_set = self.concept_set(root)
            entry = concept_set["concepts"][0]
            preview_path = Path(entry["preview_contract_path"])
            preview = json.loads(preview_path.read_text(encoding="utf-8"))
            preview["commercial_job_id"] = "CJ-OLD-IMPLEMENTATION"
            preview_path.write_text(json.dumps(preview, ensure_ascii=False, indent=2), encoding="utf-8")
            entry["preview_contract_sha256"] = self.module.sha256_file(preview_path)
            with self.assertRaises(self.module.VisualConceptSetError):
                self.module.validate(self.commercial_job(), concept_set)


if __name__ == "__main__":
    unittest.main()
