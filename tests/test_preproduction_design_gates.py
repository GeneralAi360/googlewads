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
                "creative_id": f"AD-{index}", "advertiser": advertiser,
                "source_type": "GOOGLE_ADS_TRANSPARENCY", "source_url": f"https://example.invalid/ad-{index}",
                "creative_type": "static_display", "commercial_angle": "verified category observation",
                "visual_system": {
                    "hero_type": "product-ui", "composition": "copy-left product-right", "typography": "restrained sans",
                    "palette_contrast": "neutral plus accent", "cta_treatment": "single action", "whitespace_density": "moderate",
                    "trust_signals": ["real product UI"], "image_treatment": "technical product visualization", "lighting": None,
                },
                "performance_evidence": {"tier": "E_DESIGN_REFERENCE_ONLY", "note": "design reference only", "conversion_metric_verified": False},
                "transferable_principles": ["real product proof beats generic cloud clipart"], "do_not_copy": ["logo", "copy"],
            })
        return {
            "research_id": "CR-001", "status": "COMPETITIVE_RESEARCH_COMPLETE", "coverage_status": "FULL",
            "degradation_reason": None, "category": "B2B CRM/cloud", "creatives": creatives,
            "synthesis": {
                "commercial_patterns": ["benefit first"], "visual_patterns": ["product UI"],
                "trust_patterns": ["real interface"], "category_cliches": ["generic cloud icon"],
                "opportunities": ["enterprise product realism"],
            },
        }

    def artifacts(self, root: Path):
        matrix = self.matrix(root)
        research = self.research()
        research_sha = self.freeze.canonical_sha(research)
        category_map = {
            "category_map_id": "CDM-001", "research_id": "CR-001", "research_sha256": research_sha,
            "category": "B2B CRM/cloud", "source_creative_ids": ["AD-1", "AD-2", "AD-3"],
            "mature_category_signals": ["real UI/product evidence"], "dominant_patterns": ["copy-left product-right"],
            "hero_strategies": ["real product UI"], "trust_signals": ["partner/proof only when verified"],
            "category_cliches": ["generic cloud icon"], "generic_ai_risks": ["toy 3D cloud", "clipart workflow"],
            "design_opportunities": ["enterprise product realism"],
            "performance_interpretation": "No conversion inference from reference-only ads",
        }
        category_sha = self.freeze.canonical_sha(category_map)
        design_brief = {
            "design_brief_id": "DB-001", "competitive_research_id": "CR-001", "competitive_research_sha256": research_sha,
            "category_map_id": "CDM-001", "category_map_sha256": category_sha,
            "campaign": {"objective": "lead"},
            "commercial_message": {"primary_proposition": "Cloud CRM", "cta": "Получить консультацию"},
            "commercial_lock": {
                "primary_proposition": "Cloud CRM", "approved_ctas": ["Получить консультацию"], "product_variant": "cloud",
                "supporting_proof": None, "mandatory_qualifiers": [], "copy_change_requires_controller_reapproval": True,
            },
            "audience": {"primary": "B2B"},
            "brand_context": {"brand_id": "brand", "display_name": "BRAND"},
            "brand_identity_lock": {"brand_id": "brand", "display_name": "BRAND", "logo_asset_required": False, "alternate_names_allowed": []},
            "references": {},
            "idea_architecture": {
                "idea_architecture_id": "IDEA-001", "core_idea": "Real product is operational proof",
                "single_takeaway": "Cloud CRM becomes a controllable working system", "presentation_mode": "PRODUCT_PROOF",
                "secondary_presentation_mode": None,
                "emotional_target": {"primary": "CONTROL", "secondary": ["TRUST"], "avoid": ["PLAYFULNESS"], "intensity": "RESTRAINED"},
                "creative_tension": "generic cloud promise versus real operational product", "why_this_visual": "real UI proves operational reality",
                "disruption_level": "LOW",
            },
            "visual_character": {
                "signature_id": "VC-001", "primary_character": "clean commercial", "secondary_character": "factual technical",
                "order_to_virality": 0.1, "aesthetics_to_innovation": 0.55, "style_tags": ["enterprise", "precise", "product-real"],
                "rationale": "trust and control require restrained product truth",
            },
            "focus_budget": {
                "primary_idea_count": 1, "primary_hero_count": 1, "primary_emotion_count": 1,
                "primary_visual_language_count": 1, "accent_detail_max": 2, "deviation_rationale": None,
            },
            "forbidden_visuals": {
                "global": ["fake logos", "fabricated claims"], "brand": ["unapproved colors"],
                "concept": ["toy cloud", "generic AI clipart", "fake dashboard"],
            },
            "creative_chaos_audit": {
                "status": "PASS", "core_idea_clear": True, "single_takeaway_clear": True,
                "presentation_mode_resolved": True, "emotional_target_resolved": True, "visual_character_coherent": True,
                "lighting_supports_idea": True, "information_overload": False, "composition_intentional": True,
                "forbidden_list_present": True, "platform_adaptation_planned": True, "first_generation_is_final": False, "blockers": [],
            },
            "art_direction_strategy": {"mode": "ART_DIRECTION_PREVIEW_3", "candidate_count": 3, "representative_format": "300x250"},
            "visual_hierarchy": {"primary_aoi": "product UI", "primary_message": "offer", "intended_scan_path": ["product", "headline", "cta"], "brand_priority": 4},
            "image_strategy": {"hero_type": "product-led", "product_scale": "dominant", "copy_safe_area_required": True, "source_mode": "REAL_ASSET", "hero_generation_spec_required": False},
            "required_assets": [],
            "asset_quality_policy": {
                "reject_low_resolution_assets": True, "reject_generic_ai_clipart": True, "reject_unapproved_toy_clay_style": True,
                "reject_style_mismatch": True, "require_professional_category_fit": True,
            },
            "typography": {"character": "enterprise"}, "color": {"strategy": "brand-led"}, "layout": {"alignment": "deliberate"},
            "lighting": {"strategy": "restrained"},
            "lighting_intent": {
                "lighting_intent_id": "LIGHT-001", "relationship_to_idea": "preserve truthful UI and controlled hierarchy",
                "primary_aoi_role": "support real UI without theatrical effects", "emotional_function": "reinforce CONTROL and trust through restraint",
                "visual_character_alignment": "quiet technical separation supports clean commercial character",
                "scene_lighting": {"mode": "NOT_APPLICABLE", "candidate_scheme_ids": [], "rationale": "flat real UI has no scene to relight", "material_context": "real product UI"},
                "composition_lighting": {
                    "mode": "OPTIONAL", "allowed_primitives": ["copy_scrim"], "copy_safe_zone_strategy": "use tonal separation only where necessary",
                    "focal_priority": "real UI and proposition remain above any lighting treatment", "rationale": "restrained separation only",
                },
                "forbidden_behaviors": ["fake UI glow", "decorative hotspot becomes primary AOI"],
            },
            "information_density": {"policy": "glance-first"}, "small_format_policy": {"removal_order": ["support"]},
            "outputs": {"concept_count": 1, "variant_count": 1, "languages": ["ru"], "sizes": ["300x250", "320x50"], "expected_files": 2},
            "review_requirements": {
                "actual_size": True, "asset_quality": True, "professional_category_fit": True,
                "idea_fidelity": True, "emotional_fidelity": True, "lighting_intent_fidelity": True,
                "thumbnail": True, "grayscale": True, "squint": True,
            },
        }
        design_sha = self.freeze.canonical_sha(design_brief)
        art_approval = {
            "approval_id": "ADA-001", "status": "APPROVED", "approved_by": "USER",
            "design_brief_id": "DB-001", "design_brief_sha256": design_sha,
            "selected_direction": {
                "art_direction_id": "AD-ENTERPRISE-01", "label": "Enterprise Product Reality", "candidate_ids": ["A", "B", "C"],
                "idea_architecture_id": "IDEA-001", "visual_character_signature_id": "VC-001", "lighting_intent_id": "LIGHT-001",
                "presentation_mode": "PRODUCT_PROOF", "emotional_target": "CONTROL",
                "visual_thesis": "serious product-led B2B", "composition": "product proof integrated with operational copy system",
                "hero_strategy": "real product UI, no clipart", "typography": "restrained enterprise grotesk", "palette": "brand-led neutral",
                "lighting_image_treatment": "truthful UI plus restrained tonal separation", "graphic_device": "product interface aperture",
                "trust_signals": ["real UI"], "whitespace_character": "controlled", "anti_patterns": ["toy cloud", "generic AI clipart"],
            },
        }
        art_sha = self.freeze.canonical_sha(art_approval)
        preview = root / "representative.png"
        preview.write_bytes(b"high-fidelity-representative")
        representative = {
            "approval_id": "RDA-001", "status": "APPROVED", "approved_by": "USER",
            "art_direction_approval_id": "ADA-001", "art_direction_approval_sha256": art_sha,
            "art_direction_id": "AD-ENTERPRISE-01", "preview_id": "PREVIEW-300x250-01",
            "artifact_path": preview.as_posix(), "artifact_sha256": self.freeze.sha256_file(preview), "width": 300, "height": 250,
            "quality_checks": {key: "PASS" for key in (
                "idea_fidelity", "emotional_fidelity", "visual_character_fidelity", "lighting_intent_fidelity",
                "asset_quality", "professional_category_fit", "hierarchy", "typography", "brand_fidelity",
                "commercial_message_fidelity", "hero_crop", "lighting_contrast", "cta_clarity", "anti_generic_ai",
            )},
        }
        representative_sha = self.freeze.canonical_sha(representative)
        campaign_system = {
            "campaign_design_system_id": "CDS-001", "status": "APPROVED",
            "design_brief_id": "DB-001", "design_brief_sha256": design_sha,
            "art_direction_approval_id": "ADA-001", "art_direction_approval_sha256": art_sha,
            "representative_approval_id": "RDA-001", "representative_approval_sha256": representative_sha,
            "art_direction_id": "AD-ENTERPRISE-01", "idea_architecture_id": "IDEA-001",
            "visual_character_signature_id": "VC-001", "lighting_intent_id": "LIGHT-001",
            "grid_logic": "deliberate product-proof grid", "headline_behavior": "dominant concise proposition", "offer_behavior": "secondary commercial rail",
            "cta_behavior": "approved CTA treatment remains subordinate to offer", "brand_anchor_behavior": "quiet stable anchor",
            "hero_treatment": "real UI macro crop", "crop_language": "large coherent product fragment", "background_system": "light neutral",
            "accent_system": "controlled brand accent only",
            "lighting_system": {
                "scene_policy": "do not relight real UI", "composition_policy": "restrained separation only", "focal_priority": "UI and proposition first",
                "copy_safe_policy": "scrim only when readability needs it", "allowed_primitives": ["copy_scrim"],
                "forbidden_behaviors": ["fake UI glow", "decorative hotspot"],
            },
            "whitespace_character": "controlled premium",
            "format_adaptation_rules": {"rectangle": "keep UI proof large", "micro_horizontal": "remove UI if needed and preserve proposition/action/brand"},
            "forbidden_patterns": ["toy cloud", "generic AI clipart", "fake dashboard"],
        }
        paths = {}
        for name, value in (("research", research), ("category", category_map), ("brief", design_brief), ("art", art_approval), ("representative", representative), ("system", campaign_system)):
            path = root / f"{name}.json"
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
            paths[name] = path
        return matrix, research, category_map, design_brief, art_approval, representative, campaign_system, paths

    def call_freeze(self, root: Path, artifacts, **kwargs):
        matrix, research, category, brief, art, representative, system, paths = artifacts
        return self.freeze.freeze_preproduction(
            matrix, research, category, brief, art, representative, system, root / "preproduction-freeze.json",
            research_path=paths["research"], category_map_path=paths["category"], design_brief_path=paths["brief"],
            art_approval_path=paths["art"], representative_approval_path=paths["representative"],
            campaign_design_system_path=paths["system"], **kwargs,
        )

    def test_complete_chain_freezes_idea_character_lighting_and_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.call_freeze(root, self.artifacts(root))
            self.assertEqual(result["status"], "PREPRODUCTION_FROZEN")
            self.assertEqual(result["idea_architecture_id"], "IDEA-001")
            self.assertEqual(result["visual_character_signature_id"], "VC-001")
            self.assertEqual(result["lighting_intent_id"], "LIGHT-001")
            self.assertEqual(result["campaign_design_system"]["id"], "CDS-001")

    def test_degraded_research_requires_explicit_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            artifacts[1]["coverage_status"] = "DEGRADED"
            artifacts[1]["degradation_reason"] = "Only secondary category evidence available"
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "COMPETITIVE_RESEARCH_DEGRADED")

    def test_scene_lighting_required_needs_candidate_scheme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            brief = artifacts[3]
            brief["lighting_intent"]["scene_lighting"] = {"mode": "REQUIRED", "candidate_scheme_ids": [], "rationale": "product photo", "material_context": "glass"}
            self._rebind_after_brief_change(artifacts)
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "LIGHTING_INTENT_INVALID")

    def test_not_applicable_scene_lighting_rejects_scheme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            artifacts[3]["lighting_intent"]["scene_lighting"]["candidate_scheme_ids"] = [10]
            self._rebind_after_brief_change(artifacts)
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "LIGHTING_INTENT_INVALID")

    def test_art_direction_cannot_change_lighting_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            artifacts[4]["selected_direction"]["lighting_intent_id"] = "LIGHT-OTHER"
            self._rebind_after_art_change(artifacts)
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "ART_DIRECTION_LIGHTING_MISMATCH")

    def test_focus_budget_expansion_requires_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            artifacts[3]["focus_budget"]["primary_hero_count"] = 2
            artifacts[3]["focus_budget"]["deviation_rationale"] = None
            self._rebind_after_brief_change(artifacts)
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "FOCUS_BUDGET_UNJUSTIFIED")

    def test_campaign_system_must_cover_every_layout_family(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            del artifacts[6]["format_adaptation_rules"]["micro_horizontal"]
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "CAMPAIGN_DESIGN_SYSTEM_INCOMPLETE")

    def test_campaign_lighting_cannot_exceed_lighting_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = list(self.artifacts(root))
            artifacts[6]["lighting_system"]["allowed_primitives"].append("spotlight")
            with self.assertRaises(self.freeze.PreproductionFreezeError) as ctx:
                self.call_freeze(root, tuple(artifacts))
            self.assertEqual(ctx.exception.code, "CAMPAIGN_LIGHTING_SYSTEM_MISMATCH")

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

    def _rebind_after_brief_change(self, artifacts):
        brief, art = artifacts[3], artifacts[4]
        art["design_brief_sha256"] = self.freeze.canonical_sha(brief)
        self._rebind_after_art_change(artifacts)

    def _rebind_after_art_change(self, artifacts):
        art, representative, system = artifacts[4], artifacts[5], artifacts[6]
        art_sha = self.freeze.canonical_sha(art)
        representative["art_direction_approval_sha256"] = art_sha
        rep_sha = self.freeze.canonical_sha(representative)
        system["design_brief_sha256"] = self.freeze.canonical_sha(artifacts[3])
        system["art_direction_approval_sha256"] = art_sha
        system["representative_approval_sha256"] = rep_sha


if __name__ == "__main__":
    unittest.main()
