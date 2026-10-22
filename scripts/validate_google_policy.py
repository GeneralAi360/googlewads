#!/usr/bin/env python3
"""Fail-closed local Google Ads policy preflight for final banner + destination evidence.

This is a risk-reduction gate, not a guarantee of Google approval. It deliberately
avoids OCR/semantic image inference: visual-policy judgments must be supplied by a
GOOGLE_POLICY_REVIEWER and are hash-bound to the exact artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image


class PolicyPreflightError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PolicyPreflightError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PolicyPreflightError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finding(code: str, scope: str, message: str, policy_family: str | None = None) -> dict[str, Any]:
    return {"code": code, "scope": scope, "message": message, "policy_family": policy_family}


def image_has_transparency(path: Path) -> bool:
    with Image.open(path) as image:
        if image.mode in {"RGBA", "LA"}:
            alpha = image.getchannel("A")
            extrema = alpha.getextrema()
            return bool(extrema and extrema[0] < 255)
        if image.mode == "P" and "transparency" in image.info:
            return True
    return False


def inspect_artifact(context: dict[str, Any], blockers: list[dict[str, Any]], incomplete: list[dict[str, Any]]) -> None:
    creative = context["creative"]
    path = Path(creative["file_path"])
    if not path.is_file():
        incomplete.append(finding("POLICY_ARTIFACT_MISSING", "CREATIVE_POLICY", f"creative file does not exist: {path}", "POL_IMAGE_AD_REQUIREMENTS"))
        return

    actual_sha = sha256_file(path)
    if actual_sha != creative["file_sha256"]:
        blockers.append(finding("POLICY_ARTIFACT_SHA_MISMATCH", "CREATIVE_POLICY", "policy context is stale: creative SHA does not match final bytes", "POL_IMAGE_AD_REQUIREMENTS"))
        return

    try:
        with Image.open(path) as image:
            actual_size = image.size
            actual_format = (image.format or "").upper()
    except Exception as exc:  # Pillow exception types vary by codec
        blockers.append(finding("POLICY_ARTIFACT_UNREADABLE", "CREATIVE_POLICY", f"creative cannot be decoded: {exc}", "POL_IMAGE_QUALITY"))
        return

    if actual_size != (creative["width"], creative["height"]):
        blockers.append(finding("POLICY_ARTIFACT_DIMENSION_MISMATCH", "CREATIVE_POLICY", f"declared {creative['width']}x{creative['height']} but file is {actual_size[0]}x{actual_size[1]}", "POL_IMAGE_AD_REQUIREMENTS"))

    declared = creative["format"].upper()
    normalized_declared = "JPEG" if declared in {"JPG", "JPEG"} else declared
    normalized_actual = "JPEG" if actual_format in {"JPG", "JPEG"} else actual_format
    if normalized_declared != normalized_actual:
        blockers.append(finding("POLICY_ARTIFACT_FORMAT_MISMATCH", "CREATIVE_POLICY", f"declared format {declared} but decoded format is {actual_format}", "POL_IMAGE_AD_REQUIREMENTS"))

    if normalized_actual == "PNG" and image_has_transparency(path):
        blockers.append(finding("MISLEADING_DESIGN_TRANSPARENT_BACKGROUND", "CREATIVE_POLICY", "image ad contains transparent pixels; current misleading-ad-design examples disallow transparent-background image ads", "POL_MISLEADING_AD_DESIGN"))


def check_copy(context: dict[str, Any], blockers: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    copy = context["copy"]
    text_fields = [copy.get("headline") or "", copy.get("support") or "", copy.get("offer") or "", copy.get("cta") or "", copy.get("legal_or_qualifier") or ""]
    combined = " ".join(text_fields)
    if re.search(r"([!?])\1+", combined):
        blockers.append(finding("EDITORIAL_REPEATED_PUNCTUATION", "CREATIVE_POLICY", "copy contains repeated attention-seeking punctuation such as !! or ??", "POL_IMAGE_QUALITY"))
    alpha = "".join(ch for ch in combined if ch.isalpha())
    if len(alpha) >= 12:
        uppercase = sum(1 for ch in alpha if ch.isupper())
        if uppercase / len(alpha) > 0.72:
            warnings.append(finding("EDITORIAL_EXCESSIVE_CAPS_REVIEW", "CREATIVE_POLICY", "copy is predominantly uppercase; review editorial/professional presentation and brand necessity", "POL_IMAGE_QUALITY"))


def check_semantic_visual(context: dict[str, Any], blockers: list[dict[str, Any]], incomplete: list[dict[str, Any]]) -> None:
    creative = context["creative"]
    review = context["semantic_visual_review"]
    if review.get("reviewed_artifact_sha256") != creative["file_sha256"]:
        blockers.append(finding("POLICY_VISUAL_REVIEW_STALE", "CREATIVE_POLICY", "GOOGLE_POLICY_REVIEWER report is not bound to the final artifact SHA", "POL_MISLEADING_AD_DESIGN"))
        return

    pass_checks = {
        "image_quality": "POL_IMAGE_QUALITY",
        "essential_text_legible": "POL_IMAGE_QUALITY",
        "fills_canvas": "POL_IMAGE_QUALITY",
    }
    for key, family in pass_checks.items():
        value = review.get(key)
        if value == "FAIL":
            blockers.append(finding(f"POLICY_{key.upper()}_FAIL", "CREATIVE_POLICY", f"semantic visual review failed: {key}", family))
        elif value == "UNCHECKABLE":
            incomplete.append(finding(f"POLICY_{key.upper()}_UNCHECKABLE", "CREATIVE_POLICY", f"semantic visual review could not verify: {key}", family))

    absent_checks = {
        "system_warning_or_dialog_mimic": "POL_MISLEADING_AD_DESIGN",
        "nonfunctional_controls": "POL_MISLEADING_AD_DESIGN",
        "download_install_ui": "POL_MISLEADING_AD_DESIGN",
        "misleading_arrows_or_interactions": "POL_MISLEADING_AD_DESIGN",
        "segmented_or_multi_ad_appearance": "POL_MISLEADING_AD_DESIGN",
        "contextless_or_disproportionate_button": "POL_MISLEADING_AD_DESIGN",
        "distracting_or_flashing": "POL_IMAGE_QUALITY",
        "inappropriate_content": "POL_INAPPROPRIATE_CONTENT",
        "manipulated_media_deceptive": "POL_MISREPRESENTATION",
    }
    for key, family in absent_checks.items():
        value = review.get(key)
        if value == "PRESENT":
            blockers.append(finding(f"POLICY_{key.upper()}_PRESENT", "CREATIVE_POLICY", f"prohibited/risky visual condition present: {key}", family))
        elif value == "UNCHECKABLE":
            incomplete.append(finding(f"POLICY_{key.upper()}_UNCHECKABLE", "CREATIVE_POLICY", f"semantic visual review could not verify absence of: {key}", family))


def check_identity_and_claims(context: dict[str, Any], blockers: list[dict[str, Any]], incomplete: list[dict[str, Any]]) -> None:
    identity = context["business_identity"]
    if not identity["banner_business_name_matches"]:
        blockers.append(finding("MISLEADING_BUSINESS_IDENTITY", "CREATIVE_POLICY", "banner business identity does not match the advertiser identity", "POL_MISREPRESENTATION"))
    if identity["affiliation_claimed"] and not identity["affiliation_verified"]:
        blockers.append(finding("UNVERIFIED_AFFILIATION_CLAIM", "CREATIVE_POLICY", "ad implies an affiliation/endorsement that is not verified", "POL_MISREPRESENTATION"))

    for idx, claim in enumerate(context.get("claims") or []):
        prefix = f"claim[{idx}] {claim.get('text')!r}"
        if claim["material"] and claim["verification_status"] != "VERIFIED":
            blockers.append(finding("UNVERIFIED_MATERIAL_CLAIM", "CREATIVE_POLICY", f"{prefix} is material but not verified", "POL_UNRELIABLE_CLAIMS"))
        if claim["destination_support"] == "FAIL":
            blockers.append(finding("CLAIM_DESTINATION_MISMATCH", "DESTINATION_POLICY", f"{prefix} is not supported by the landing page", "POL_UNCLEAR_RELEVANCE"))
        elif claim["destination_support"] == "UNKNOWN" and claim["material"]:
            incomplete.append(finding("CLAIM_DESTINATION_SUPPORT_UNKNOWN", "DESTINATION_POLICY", f"{prefix} has not been verified on the landing page", "POL_UNCLEAR_RELEVANCE"))
        if claim["offer_available"] == "FAIL":
            blockers.append(finding("ADVERTISED_OFFER_UNAVAILABLE", "DESTINATION_POLICY", f"{prefix} is unavailable or not easily found", "POL_UNAVAILABLE_OFFERS"))
        elif claim["offer_available"] == "UNKNOWN" and claim["material"]:
            incomplete.append(finding("ADVERTISED_OFFER_AVAILABILITY_UNKNOWN", "DESTINATION_POLICY", f"availability is unknown for {prefix}", "POL_UNAVAILABLE_OFFERS"))


def check_destination(context: dict[str, Any], blockers: list[dict[str, Any]], incomplete: list[dict[str, Any]]) -> None:
    destination = context["destination"]
    fields = {
        "working": "DESTINATION_NOT_WORKING",
        "domain_match": "DESTINATION_MISMATCH",
        "google_adsbot_crawlable": "DESTINATION_NOT_CRAWLABLE",
        "target_geo_accessible": "DESTINATION_NOT_ACCESSIBLE",
        "offer_easy_to_find": "UNAVAILABLE_OFFER_DESTINATION",
        "cta_action_available": "CTA_NOT_AVAILABLE_AT_DESTINATION",
        "advertiser_identity_matches": "DESTINATION_ADVERTISER_MISMATCH",
        "original_useful_content": "INSUFFICIENT_ORIGINAL_CONTENT",
    }
    for key, code in fields.items():
        value = destination.get(key)
        family = "POL_UNAVAILABLE_OFFERS" if key in {"offer_easy_to_find", "cta_action_available"} else ("POL_UNCLEAR_RELEVANCE" if key == "advertiser_identity_matches" else "POL_DESTINATION_REQUIREMENTS")
        if value == "FAIL":
            blockers.append(finding(code, "DESTINATION_POLICY", f"destination check failed: {key}", family))
        elif value == "UNKNOWN":
            incomplete.append(finding(f"{code}_UNKNOWN", "DESTINATION_POLICY", f"destination check is unresolved: {key}", family))


def check_contextual_policies(context: dict[str, Any], blockers: list[dict[str, Any]], incomplete: list[dict[str, Any]], review_required: list[dict[str, Any]]) -> None:
    trademark = context["trademark_review"]
    if trademark["status"] == "FAIL":
        blockers.append(finding("TRADEMARK_REVIEW_FAIL", "TRADEMARK_POLICY", "third-party trademark review failed", "POL_TRADEMARKS"))
    elif trademark["status"] == "REVIEW_REQUIRED":
        review_required.append(finding("TRADEMARK_REVIEW_REQUIRED", "TRADEMARK_POLICY", "third-party trademark use requires contextual review", "POL_TRADEMARKS"))

    vertical = context["vertical_review"]
    if vertical["status"] == "BLOCKED":
        blockers.append(finding("RESTRICTED_VERTICAL_BLOCKED", "VERTICAL_CERTIFICATION", "advertised vertical is blocked in the supplied policy context", "POL_RESTRICTED_VERTICAL"))
    elif vertical["status"] == "REVIEW_REQUIRED":
        review_required.append(finding("RESTRICTED_VERTICAL_REVIEW_REQUIRED", "VERTICAL_CERTIFICATION", "restricted/sensitive vertical requires live current-policy review", "POL_RESTRICTED_VERTICAL"))

    if vertical.get("certification_required") is True and vertical.get("certification_verified") is not True:
        review_required.append(finding("VERTICAL_CERTIFICATION_UNVERIFIED", "VERTICAL_CERTIFICATION", "required advertiser/product certification has not been verified", "POL_RESTRICTED_VERTICAL"))

    targeting = vertical.get("targeting_policy_status", "NOT_APPLICABLE")
    if targeting == "BLOCKED":
        blockers.append(finding("TARGETING_POLICY_BLOCKED", "TARGETING_POLICY", "campaign targeting/personalization is blocked by supplied policy review", "POL_PERSONALIZED_ADVERTISING"))
    elif targeting == "REVIEW_REQUIRED":
        review_required.append(finding("TARGETING_POLICY_REVIEW_REQUIRED", "TARGETING_POLICY", "targeting/personalization requires separate sensitive-interest policy review", "POL_PERSONALIZED_ADVERTISING"))

    ai = context.get("ai_asset_review")
    if ai and ai.get("ai_generated_or_edited") and ai.get("label_or_disclosure_review") == "REVIEW_REQUIRED":
        review_required.append(finding("AI_LABEL_DISCLOSURE_REVIEW_REQUIRED", "CREATIVE_POLICY", "AI-generated/edited asset may require jurisdiction/platform disclosure review", None))


def scope_status(scope: str, blockers: list[dict[str, Any]], incomplete: list[dict[str, Any]], review_required: list[dict[str, Any]], *, na: bool = False) -> str:
    if any(item["scope"] == scope for item in blockers):
        return "FAIL"
    if any(item["scope"] == scope for item in review_required):
        return "REVIEW_REQUIRED"
    if any(item["scope"] == scope for item in incomplete):
        return "INCOMPLETE"
    return "NOT_APPLICABLE" if na else "PASS"


def validate(context: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    incomplete: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    review_required: list[dict[str, Any]] = []

    if context.get("policy_snapshot_date") != snapshot.get("snapshot_date"):
        incomplete.append(finding("POLICY_SNAPSHOT_MISMATCH", "CREATIVE_POLICY", "context policy snapshot date does not match local policy snapshot", None))

    try:
        age = (date.today() - date.fromisoformat(snapshot["snapshot_date"])).days
        max_age = int((snapshot.get("freshness") or {}).get("max_age_days_for_general_delivery", 45))
        if age > max_age:
            incomplete.append(finding("POLICY_SNAPSHOT_STALE", "CREATIVE_POLICY", f"local Google policy snapshot is {age} days old; refresh current official policy before delivery", None))
    except Exception:
        incomplete.append(finding("POLICY_SNAPSHOT_DATE_INVALID", "CREATIVE_POLICY", "policy snapshot date could not be validated", None))

    inspect_artifact(context, blockers, incomplete)
    check_copy(context, blockers, warnings)
    check_semantic_visual(context, blockers, incomplete)
    check_identity_and_claims(context, blockers, incomplete)
    check_destination(context, blockers, incomplete)
    check_contextual_policies(context, blockers, incomplete, review_required)

    vertical = context["vertical_review"]
    if vertical["restricted_or_sensitive"] and snapshot.get("freshness", {}).get("restricted_vertical_requires_live_refresh", False):
        if vertical["status"] not in {"PASS", "BLOCKED"}:
            # Already represented by contextual review; keep the reason explicit.
            pass

    if blockers:
        status = "GOOGLE_POLICY_PREFLIGHT_BLOCKED"
    elif review_required:
        status = "POLICY_REVIEW_REQUIRED"
    elif incomplete:
        status = "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE"
    else:
        status = "GOOGLE_POLICY_PREFLIGHT_PASS"

    scopes = {
        "creative_policy": scope_status("CREATIVE_POLICY", blockers, incomplete, review_required),
        "destination_policy": scope_status("DESTINATION_POLICY", blockers, incomplete, review_required),
        "vertical_certification": scope_status("VERTICAL_CERTIFICATION", blockers, incomplete, review_required, na=vertical["status"] == "NOT_APPLICABLE"),
        "targeting_policy": scope_status("TARGETING_POLICY", blockers, incomplete, review_required, na=vertical.get("targeting_policy_status") == "NOT_APPLICABLE"),
        "trademark_policy": scope_status("TRADEMARK_POLICY", blockers, incomplete, review_required, na=context["trademark_review"]["status"] == "NOT_APPLICABLE"),
    }

    if review_required:
        warnings.extend(review_required)

    statement = (
        "No blocking issue found in the current Google Ads policy preflight; final Google review still applies."
        if status == "GOOGLE_POLICY_PREFLIGHT_PASS"
        else "The creative is not locally cleared as Google-ready; resolve blockers, missing evidence, or required contextual review before delivery."
    )
    return {
        "status": status,
        "policy_context_id": context["policy_context_id"],
        "policy_snapshot_date": snapshot["snapshot_date"],
        "creative_sha256": context["creative"]["file_sha256"],
        "approval_guaranteed": False,
        "blockers": blockers,
        "incomplete_checks": incomplete,
        "warnings": warnings,
        "policy_scopes": scopes,
        "final_statement": statement,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate final banner and supplied evidence against Google Ads policy preflight")
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, default=Path("config/google-ads-policy-snapshot.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.context), load_json(args.snapshot))
    except (PolicyPreflightError, KeyError, TypeError, ValueError) as exc:
        result = {
            "status": "GOOGLE_POLICY_PREFLIGHT_INCOMPLETE",
            "policy_context_id": "UNKNOWN",
            "policy_snapshot_date": "1970-01-01",
            "creative_sha256": "0" * 64,
            "approval_guaranteed": False,
            "blockers": [],
            "incomplete_checks": [finding("POLICY_PREFLIGHT_INPUT_ERROR", "CREATIVE_POLICY", str(exc), None)],
            "warnings": [],
            "policy_scopes": {
                "creative_policy": "INCOMPLETE",
                "destination_policy": "INCOMPLETE",
                "vertical_certification": "INCOMPLETE",
                "targeting_policy": "INCOMPLETE",
                "trademark_policy": "INCOMPLETE"
            },
            "final_statement": "The policy preflight input is incomplete or invalid; do not claim Google-ready status."
        }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "out": args.out.as_posix()}, ensure_ascii=False))
    return 0 if result["status"] == "GOOGLE_POLICY_PREFLIGHT_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
