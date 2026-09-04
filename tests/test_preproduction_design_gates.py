import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PreproductionDesignGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.freeze = load(ROOT / "scripts" / "freeze_preproduction_design.py", "freeze_preproduction_design")
        cls.materializer = load(ROOT / "scripts" / "materialize_competitive_research_jobs.py", "materialize_competitive_research_jobs")

    def matrix(self, root: Path):
        return {
            "run_id": "preprod-demo",
            "expected_output_files": 2,
            "banner_matrix": [
                {"job_id": "C01-S300x250-V01-Lru", "concept_id": "C01", "variant_id": "V01", "language": "ru", "width": 300, "height": 250, "dimension": "300x250", "layout_family": "rectangle", "output_path": (root / "out" / "300x250.png").as_posix()},
                {"job_id": "C01-S320x50-V01-Lru", "concept_id": "C01", "variant_id": "V01", "language": "ru", "width": 320, "height": 50, "dimension": "320x50", "layout_family": "micro_horizontal", "output_path": (root / "out" / "320x50.png").as_posix()},
            ],
        }

    def research(self):
        creatives = []
        for index, advertiser in enumerate(("A", "B", "B"), 1):
            creatives.append({
                "creative_id": f"AD-{index}",
                "advertiser": advertiser,
                "source_type": "GOOGLE_ADS_TRANSPARENCY",
                "source_url": f"https://example.invalid/ad-{index}",
                "creative_type": "static_display",
                "commercial_angle": "verified category observation",
                "visual_system": {
                    "hero_type": "product-ui",
                    "composition": "copy-left product-right",
                    "typography": "restrained sans",
                    "palette_contrast": "neutral plus accent",
                    "cta_treatment": "single action",
                    "whitespace_density": "moderate",
                    "trust_signals": ["real product UI"],
                    "image_treatment": "technical product visualization",
                    "lighting": None,
                },
                "performance_evidence": {"tier": "E_DESIGN_REFERENCE_ONLY", "note": "design reference only", "conversion_metric_verified": False},
                "transferable_principles": ["real product proof beats generic cloud clipart"],
                "do_not_copy": ["logo", "copy"],
            })
        return {
            "research_id": "CR-001",
            "status": "COMPETITIVE_RESEARCH_COMPLETE",
            "coverage_status": "FULL",
            "degradation_reason": None,
            "category": "B2B CRM/cloud",
            "creatives": creatives,
            "synthesis": {
                "commercial_patterns": ["benefit first"],
                "visual_patterns": ["product UI"],
                "trust_patterns": ["real interface"],
                "category_cliches": ["generic cloud icon"],
                "opportunities": ["enterprise product realism"],
            },
        }

    def artifacts(self, root: Path):
        matrix = self.matrix(root)
        research = self.research()
        research_sha = self.freeze.canonical_sha(research)
        category_map = {
            "category_map_id": "CDM-001",
            "research_id": "CR-001",
            "research_sha256": research_sha,
            "category": "B2B CRM/cloud",
            "source_creative_ids": ["AD-1", "AD-2", "AD-3"],
            "mature_category_signals": ["real UI/product evidence"],
            "dominant_patterns": ["copy-left product-right"],
            "hero_strategies": ["real product UI"],
            "trust_signals": ["partner/proof only when verified"],
            "category_cliches": ["generic cloud icon"],
            "generic_ai_risks": ["toy 3D cloud", "clipart workflow"],
            "design_opportunities": ["enterprise product realism"],
            "performance_interpretation": "No conversion inference from reference-only ads",
        }
        category_sha = self.freeze.canonical_sha(category_map)
        design_brief = {
            "design_brief_id": "DB-001",
            "competitive_research_id": "CR-001",
            "competitive_research_sha256": research_sha,
            "category_map_id": "CDM-001",
            "category_map_sha256": category_sha,
            "campaign": {"objective": "lead"},
            "commercial_message": {"primary_proposition": "Cloud CRM", "cta": "Get consultation"},
            "commercial_lock": {
                "primary_proposition": "Cloud CRM",
                "approved_ctas": ["Get consultation", "Request demo"],
                "product_variant": "cloud",
                "supporting_proof": None,
                "mandatory_qualifiers": [],
                "copy_change_requires_controller_reapproval": True,
            },
            "audience": {"primary": "B2B"},
            "brand_context": {"brand_id": "brand", "display_name": "BRAND"},
            "brand_identity_lock": {
                "brand_id": "brand",
                "display_name": "BRAND",
                "logo_asset_required": False,
                "alternate_names_allowed": [],
            },
            "art_direction_strategy": {"mode": "ART_DIRECTION_PREVIEW_3", "candidate_count": 3, "representative_format": "300x250"},
            "visual_hierarchy": {"primary_aoi": "product UI", "primary_message": "offer", "intended_scan_path": ["product", "headline", "cta"], "brand_priority": 4},
            "image_strategy": {"hero_type": "product-led", "product_scale": "dominant", "copy_safe_area_required": True},
            "required_assets": [],
            "asset_quality_policy": {
                "reject_low_resolution_assets": True,
                "reject_generic_ai_clipart": True,
                "reject_unapproved_toy_clay_style": True,
                "reject_style_mismatch": True,
                "require_professional_category_fit": True,
            },
            "typography": {"character": "enterprise"},
            "color": {"strategy": "brand-led"},
            "layout": {"alignment": "deliberate"},
            "lighting": {"strategy": "restrained"},
            "information_density": {"policy": "glance-first"},
            "small_format_policy": {"removal_order": ["support"]},
            "outputs": {"concept_count": 1, "variant_count": 1, "languages": ["ru"], "sizes": ["300x250", "320x50"], "expected_files": 2},
            "review_requirements": {"actual_size": True, "asset_quality": True, "professional_category_fit": True, "thumbnail": True, "grayscale": True, "squint": True},
        }
        design_sha = self.freeze.canonical_sha(design_brief)
        art_approval = {
            "approval_id": "ADA-001",
            "status": "APPROVED",
            "approved_by": "USER",
            "design_brief_id": "DB-001",
            "design_brief_sha256": design_sha,
            "selected_direction": {
                "art_direction_id": "AD-ENTERPRISE-01",
                "label": "Enterprise Product Reality",
                "candidate_ids": ["A", "B", "C"],
                "visual_thesis": "serious product-led B2B",
                "composition": "copy-left product-right",
                "hero_strategy": "real product UI, no clipart",
                "typography": "restrained enterprise grotesk",
                "palette": "brand-led neutral",
                "lighting_image_treatment": "clean restrained technical",
                "graphic_device": "product interface depth",
                "trust_signals": ["real UI"],
                "whitespace_character": "controlled",
                "anti_patterns": ["toy cloud", "generic AI clipart"],
            },
        }
        art_sha = self.freeze.canonical_sha(art_approval)
        preview = root / "representative.png"
        preview.write_bytes(b"high-fidelity-representative")
        representative = {
            "approval_id": "RDA-001",
            "status": "APPROVED",
            "approved_by": "USER",
            "art_direction_approval_id": "ADA-001",
            "art_direction_approval_sha256": art_sha,
            "art_direction_id": "AD-ENTERPRISE-01",
            "preview_id": "PREVIEW-300x250-01",
            "artifact_path": preview.as_posix(),
            "artifact_sha256": self.freeze.sha256_file(preview),
            "width": 300,
            "height": 250,
            "quality_checks": {key: "PASS" for key in (
                "asset_quality", "professional_category_fit", "hierarchy", "typography", "brand_fidelity",
                "commercial_message_fidelity", "hero_crop", "lighting_contrast", "cta_clarity", "anti_generic_ai",
            )},
        }
        paths = {}
        for name, value in (("research", research), ("category", category_map), ("brief", design_brief), ("art", art_approval), ("representative", representative)):
            path = root / f"{name}.json"
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
            paths[name] = path
        return matrix, research, category_map, design_brief, art_approval, representative, paths

    def freeze_all(self, root: Path, **kwargs):
        matrix, research, category, brief, art, representative, paths = self.artifacts(root)
        return self.freeze.freeze_preproduction(
            matrix, research, category, brief, art, representative, root / "preproduction-freeze.json",
            research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"],
            art_approval_path=paths["art"], representative_approval_path=paths["representative"], **kwargs,
        )

    def test_complete_chain_freezes_before_scale_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.freeze_all(Path(tmp))
            self.assertEqual(result["status"], "PREPRODUCTION_FROZEN")
            self.assertEqual(result["research_rigor"], "FULL")
            self.assertEqual(result["selected_art_direction_id"], "AD-ENTERPRISE-01")
            self.assertEqual(result["commercial_lock"]["approved_ctas"], ["Get consultation", "Request demo"])
            self.assertEqual(result["brand_identity_lock"]["display_name"], "BRAND")

    def test_full_research_requires_multiple_real_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, research, category, brief, art, representative, paths = self.artifacts(root)
            research["creatives"] = research["creatives"][:1]
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.freeze.freeze_preproduction(matrix, research, category, brief, art, representative, root / "freeze.json", research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"], art_approval_path=paths["art"], representative_approval_path=paths["representative"])
            self.assertEqual(ctx.exception.code, "COMPETITIVE_RESEARCH_COVERAGE_LOW")

    def test_degraded_research_requires_explicit_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, research, category, brief, art, representative, paths = self.artifacts(root)
            research["coverage_status"] = "DEGRADED"
            research["degradation_reason"] = "Only one market source available"
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.freeze.freeze_preproduction(matrix, research, category, brief, art, representative, root / "freeze.json", research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"], art_approval_path=paths["art"], representative_approval_path=paths["representative"])
            self.assertEqual(ctx.exception.code, "COMPETITIVE_RESEARCH_DEGRADED")

    def test_commercial_message_change_requires_new_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, research, category, brief, art, representative, paths = self.artifacts(root)
            brief["commercial_message"]["cta"] = "Unapproved CTA"
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.freeze.freeze_preproduction(matrix, research, category, brief, art, representative, root / "freeze.json", research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"], art_approval_path=paths["art"], representative_approval_path=paths["representative"])
            self.assertEqual(ctx.exception.code, "COMMERCIAL_LOCK_MISMATCH")

    def test_brand_identity_drift_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, research, category, brief, art, representative, paths = self.artifacts(root)
            brief["brand_context"]["display_name"] = "UNAPPROVED BRAND"
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.freeze.freeze_preproduction(matrix, research, category, brief, art, representative, root / "freeze.json", research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"], art_approval_path=paths["art"], representative_approval_path=paths["representative"])
            self.assertEqual(ctx.exception.code, "BRAND_IDENTITY_UNRESOLVED")

    def test_stale_representative_hash_blocks_scale_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix, research, category, brief, art, representative, paths = self.artifacts(root)
            Path(representative["artifact_path"]).write_bytes(b"changed-after-approval")
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.freeze.freeze_preproduction(matrix, research, category, brief, art, representative, root / "freeze.json", research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"], art_approval_path=paths["art"], representative_approval_path=paths["representative"])
            self.assertEqual(ctx.exception.code, "REPRESENTATIVE_APPROVAL_STALE")

    def test_reference_only_ad_cannot_be_called_high_converting(self):
        research = self.research()
        research["creatives"][0]["performance_evidence"]["note"] = "high-converting design"
        with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
            self.freeze._validate_research(research, False)
        self.assertEqual(ctx.exception.code, "PERFORMANCE_CLAIM_UNSUPPORTED")

    def test_competitive_materializer_creates_one_readonly_job_per_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = {"research_id": "CR-001", "category": "B2B CRM", "targets": [
                {"target_id": "T1", "advertiser_or_query": "Bitrix24 integrator"},
                {"target_id": "T2", "advertiser_or_query": "CRM automation"},
            ]}
            result = self.materializer.materialize(plan, root / "research")
            self.assertEqual(result["expected_reports"], 2)
            task = Path(result["jobs"][0]["task_path"]).read_text(encoding="utf-8")
            self.assertIn("COMPETITOR_RESEARCHER", task)
            self.assertIn("Never call D/E evidence high-converting", task)


if __name__ == "__main__":
    unittest.main()
