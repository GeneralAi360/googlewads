#!/usr/bin/env python3
"""Render and validate a complete banner matrix from one render spec per job."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent

class PackError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message); self.code = code

def load_script(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None: raise PackError("FAIL_RUNTIME", f"cannot load {path}")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def load_json(path: Path) -> dict[str, Any]:
    try: return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc: raise PackError("FAIL_INPUT", f"file not found: {path}") from exc
    except json.JSONDecodeError as exc: raise PackError("FAIL_INPUT", f"invalid JSON {path}: {exc}") from exc

def validate_matrix(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    rows = matrix.get("banner_matrix")
    if not isinstance(rows, list) or not rows: raise PackError("FAIL_MATRIX", "banner_matrix must be a non-empty list")
    expected = matrix.get("expected_output_files", len(rows))
    if int(expected) != len(rows): raise PackError("FAIL_MATRIX", f"expected_output_files={expected} but matrix has {len(rows)} rows")
    ids=[row.get("job_id") for row in rows]
    if any(not x for x in ids) or len(ids)!=len(set(ids)): raise PackError("FAIL_MATRIX", "job IDs must be non-empty and unique")
    return rows

def assert_spec_matches_row(spec: dict[str, Any], row: dict[str, Any]) -> None:
    checks = {"job_id": row.get("job_id"), "width": row.get("width"), "height": row.get("height"), "layout_family": row.get("layout_family")}
    mismatches=[]
    for key, expected in checks.items():
        if spec.get(key) != expected: mismatches.append(f"{key}: spec={spec.get(key)!r} matrix={expected!r}")
    if mismatches: raise PackError("FAIL_SPEC_MATRIX_MISMATCH", "; ".join(mismatches))

def render_pack(matrix: dict[str, Any], spec_dir: Path, *, mode: str="demand_gen_uploaded_display", pack: str="core", contact_sheet: Path|None=None, technical_validator: Callable[[Path,str,str],dict[str,Any]]|None=None) -> dict[str, Any]:
    rows=validate_matrix(matrix); renderer=load_script("render_banner"); sheet=load_script("build_contact_sheet")
    validator_module=None; google_config=None
    if technical_validator is None:
        validator_module=load_script("validate_google_banner"); google_config=validator_module.load_config()
        if mode not in google_config["modes"]: raise PackError("FAIL_MODE", f"unknown validation mode: {mode}")
        if pack not in google_config["packs"]: raise PackError("FAIL_PACK", f"unknown Google pack: {pack}")
        def technical_validator(path: Path, mode_name: str, pack_name: str):
            return validator_module.validate(path, mode_name, pack_name, google_config)
    jobs=[]; passed_files=[]
    for row in rows:
        job_id=row["job_id"]; spec_path=spec_dir/f"{job_id}.json"
        job={"job_id":job_id,"spec_path":spec_path.as_posix(),"status":"FAIL","render":None,"validation":None,"error":None}
        try:
            spec=load_json(spec_path); assert_spec_matches_row(spec,row)
            out=dict(spec.get("output") or {}); out["path"]=str(row["output_path"]); out["format"]=row.get("output_format",out.get("format","png"))
            if google_config is not None: out.setdefault("target_max_bytes",int(google_config["modes"][mode]["max_file_size_bytes_conservative"]))
            spec["output"]=out
            render_report=renderer.render_banner(spec); path=Path(render_report["output_path"])
            validation=technical_validator(path,mode,pack)
            job["render"]=render_report; job["validation"]=validation
            if validation.get("status")!="PASS": raise PackError("FAIL_TECHNICAL_PREFLIGHT", "; ".join(validation.get("errors") or ["technical validation failed"]))
            job["status"]="PASS"; passed_files.append(path)
        except (OSError, PackError, getattr(renderer,"RenderError",ValueError)) as exc:
            job["error"]={"code":getattr(exc,"code","FAIL_JOB"),"message":str(exc)}
        jobs.append(job)
    passed=sum(1 for job in jobs if job["status"]=="PASS"); expected=len(rows); contact=None
    if passed_files and contact_sheet is not None:
        sheet.build_contact_sheet(passed_files,contact_sheet); contact=contact_sheet.as_posix()
    failures=[{"job_id":j["job_id"],**(j["error"] or {"code":"FAIL_JOB","message":"unknown failure"})} for j in jobs if j["status"]!="PASS"]
    return {"status":"PASS" if passed==expected else "FAIL","run_id":matrix.get("run_id"),"expected_output_files":expected,"passed_output_files":passed,"failed_output_files":expected-passed,"contact_sheet":contact,"jobs":jobs,"failures":failures}

def main() -> int:
    p=argparse.ArgumentParser(description="Render every row in a banner matrix from per-job render specs")
    p.add_argument("--matrix",required=True,type=Path); p.add_argument("--spec-dir",required=True,type=Path); p.add_argument("--mode",default="demand_gen_uploaded_display"); p.add_argument("--pack",default="core"); p.add_argument("--contact-sheet",type=Path); p.add_argument("--report",required=True,type=Path); a=p.parse_args()
    try: result=render_pack(load_json(a.matrix),a.spec_dir,mode=a.mode,pack=a.pack,contact_sheet=a.contact_sheet)
    except PackError as exc: result={"status":"FAIL","failures":[{"code":exc.code,"message":str(exc)}]}
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"report":a.report.as_posix()},ensure_ascii=False))
    return 0 if result["status"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
