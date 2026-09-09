#!/usr/bin/env python3
"""Score fresh visual-review reports against hidden expected findings."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALS = ROOT / "evals" / "visual-review-evals.json"


class EvalScoreError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvalScoreError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvalScoreError(f"invalid JSON {path}: {exc}") from exc


def normalized_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    findings = report.get("findings")
    if not isinstance(findings, list):
        raise EvalScoreError("review report must contain findings[]")
    out = []
    for item in findings:
        if not isinstance(item, dict):
            raise EvalScoreError("every finding must be an object")
        code = item.get("code")
        severity = item.get("severity")
        evidence = item.get("evidence")
        if not isinstance(code, str) or not code:
            raise EvalScoreError("finding code is required")
        if severity not in {"CRITICAL", "IMPORTANT", "MINOR"}:
            raise EvalScoreError(f"invalid finding severity: {severity!r}")
        if not isinstance(evidence, str) or not evidence.strip():
            raise EvalScoreError(f"visible evidence is required for finding {code}")
        out.append(item)
    return out


def expected_codes(case: dict[str, Any], severity: str) -> set[str]:
    return {
        item["code"]
        for item in case.get("expected_findings", [])
        if item.get("severity") == severity
    }


def score_case(case: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    case_id = case["id"]
    if report.get("case_id") != case_id:
        raise EvalScoreError(f"report case_id {report.get('case_id')!r} does not match {case_id}")
    findings = normalized_findings(report)
    reported_codes = {item["code"] for item in findings}
    reported_critical = {item["code"] for item in findings if item["severity"] == "CRITICAL"}
    expected_critical = expected_codes(case, "CRITICAL")
    expected_important = expected_codes(case, "IMPORTANT")
    detected_critical = expected_critical & reported_codes
    detected_important = expected_important & reported_codes
    false_critical = reported_critical - expected_critical

    prose_parts = [str(report.get("summary") or "")]
    for finding in findings:
        prose_parts.extend(
            [
                str(finding.get("evidence") or ""),
                str(finding.get("why_it_matters") or ""),
                str(finding.get("recommended_fix") or ""),
            ]
        )
    prose = " ".join(prose_parts).casefold()
    prohibited_claims = [claim for claim in case.get("must_not_claim", []) if claim.casefold() in prose]

    return {
        "case_id": case_id,
        "expected_critical": sorted(expected_critical),
        "detected_critical": sorted(detected_critical),
        "expected_important": sorted(expected_important),
        "detected_important": sorted(detected_important),
        "false_critical": sorted(false_critical),
        "prohibited_claims": prohibited_claims,
        "finding_count": len(findings),
    }


def ratio(found: int, total: int) -> float:
    return 1.0 if total == 0 else found / total


def score_suite(evals: dict[str, Any], reports_dir: Path) -> dict[str, Any]:
    cases = evals.get("cases")
    if not isinstance(cases, list) or not cases:
        raise EvalScoreError("eval suite has no cases")
    case_results = []
    missing_reports = []
    for case in cases:
        case_id = case["id"]
        report_path = reports_dir / f"{case_id}.review.json"
        if not report_path.is_file():
            missing_reports.append(case_id)
            continue
        case_results.append(score_case(case, load_json(report_path)))

    total_critical = sum(len(item["expected_critical"]) for item in case_results)
    found_critical = sum(len(item["detected_critical"]) for item in case_results)
    total_important = sum(len(item["expected_important"]) for item in case_results)
    found_important = sum(len(item["detected_important"]) for item in case_results)
    false_critical = sum(len(item["false_critical"]) for item in case_results)
    prohibited_claims = sum(len(item["prohibited_claims"]) for item in case_results)

    scoring = evals["evaluation_protocol"]["scoring"]
    critical_recall = ratio(found_critical, total_critical)
    important_recall = ratio(found_important, total_important)
    pass_gate = (
        not missing_reports
        and critical_recall >= float(scoring["critical_expected_finding_recall"])
        and important_recall >= float(scoring["important_expected_finding_recall_min"])
        and false_critical <= int(scoring["false_critical_findings_max"])
        and prohibited_claims == 0
    )

    return {
        "status": "PASS" if pass_gate else "FAIL",
        "case_count": len(cases),
        "scored_case_count": len(case_results),
        "missing_reports": missing_reports,
        "critical_recall": round(critical_recall, 4),
        "important_recall": round(important_recall, 4),
        "false_critical_count": false_critical,
        "prohibited_claim_count": prohibited_claims,
        "cases": case_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score fresh banner visual-review reports")
    parser.add_argument("--reports-dir", required=True, type=Path)
    parser.add_argument("--evals", type=Path, default=DEFAULT_EVALS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = score_suite(load_json(args.evals), args.reports_dir)
    except EvalScoreError as exc:
        result = {"status": "FAIL", "error": str(exc)}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if result.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
