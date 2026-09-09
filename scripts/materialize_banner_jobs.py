#!/usr/bin/env python3
"""Materialize one narrow task brief and render-spec shell per banner matrix row."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

class MaterializeError(ValueError): pass

def load_json(path: Path) -> dict[str, Any]:
    try: return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc: raise MaterializeError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc: raise MaterializeError(f"invalid JSON {path}: {exc}") from exc

def validate_matrix(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    rows=matrix.get("banner_matrix")
    if not isinstance(rows,list) or not rows: raise MaterializeError("banner_matrix must be a non-empty list")
    if int(matrix.get("expected_output_files",len(rows)))!=len(rows): raise MaterializeError("expected_output_files does not match row count")
    ids=[row.get("job_id") for row in rows]
    if any(not x for x in ids) or len(ids)!=len(set(ids)): raise MaterializeError("job IDs must be non-empty and unique")
    required=("width","height","layout_family","output_path")
    for row in rows:
        missing=[key for key in required if key not in row]
        if missing: raise MaterializeError(f"{row.get('job_id')}: missing {', '.join(missing)}")
    return rows

def render_spec_shell(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version":"0.2.0",
        "job_id":row["job_id"],
        "width":row["width"],
        "height":row["height"],
        "layout_family":row["layout_family"],
        "hero":None,
        "logo":None,
        "copy":{"headline":row.get("headline"),"support":row.get("support"),"offer":row.get("offer"),"cta":row.get("cta")},
        "brand":{},
        "lighting":{},
        "qa":{},
        "output":{"path":row["output_path"],"format":row.get("output_format","png")},
    }

def task_brief(row: dict[str, Any], spec_path: Path) -> str:
    return f"""# Banner job {row['job_id']}

## Frozen routing

- Concept: `{row.get('concept_id','UNRESOLVED')}`
- Variant: `{row.get('variant_id','UNRESOLVED')}`
- Language: `{row.get('language','UNRESOLVED')}`
- Dimension: `{row['width']}x{row['height']}`
- Layout family: `{row['layout_family']}`
- Output: `{row['output_path']}`
- Render spec owned by this job: `{spec_path.as_posix()}`

## Worker contract

Produce exactly this banner job. Do not create child agents. Do not edit another job's render spec or output. Do not change the frozen job ID, dimensions, layout family, language, output path, offer, price, CTA, legal copy, brand identity, or creative contract unless the controller explicitly reconciles a change.

The render-spec shell may contain `null`/empty copy, brand, hero, logo, or lighting fields because the materializer is intentionally fact-preserving. Fill them only from the controller-provided `CREATIVE_CONTRACT`, `BRAND/DESIGN_CONTEXT_SET`, `REFERENCE_DNA`, approved assets, and lighting directive. Never invent missing business facts.

Before returning the job, run the deterministic renderer for this spec and report explicit failure states such as `FAIL_COPY_OVERFLOW`, `FAIL_LAYOUT`, `FAIL_CONTRAST`, `FAIL_FILE_SIZE`, or `FAIL_ASSET` rather than silently changing the creative.

## Stop conditions

- `NEEDS_CONTEXT` — required approved copy/brand/asset fact was not supplied.
- `DESIGN_CHANGED` — the frozen creative contract genuinely needs controller reconciliation.
- `DESIGN_DRIFT` — the produced banner diverges from the frozen contract.
- `TECHNICAL_BLOCKED` — the exact required render cannot be produced/validated.
"""

def materialize(matrix: dict[str, Any], out_dir: Path, *, force: bool=False) -> dict[str, Any]:
    rows=validate_matrix(matrix); specs=out_dir/"render-specs"; briefs=out_dir/"task-briefs"; specs.mkdir(parents=True,exist_ok=True); briefs.mkdir(parents=True,exist_ok=True)
    jobs=[]
    for row in rows:
        spec_path=specs/f"{row['job_id']}.json"; brief_path=briefs/f"{row['job_id']}.md"
        if not force and (spec_path.exists() or brief_path.exists()): raise MaterializeError(f"refusing to overwrite existing job files for {row['job_id']}")
        spec_path.write_text(json.dumps(render_spec_shell(row),ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); brief_path.write_text(task_brief(row,spec_path),encoding="utf-8")
        jobs.append({"job_id":row["job_id"],"render_spec_path":spec_path.as_posix(),"task_brief_path":brief_path.as_posix(),"output_path":row["output_path"]})
    index={"run_id":matrix.get("run_id"),"expected_output_files":len(rows),"jobs":jobs}; index_path=out_dir/"dispatch-index.json"; index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return index

def main() -> int:
    p=argparse.ArgumentParser(description="Create one render-spec shell and narrow task brief per banner-matrix row")
    p.add_argument("--matrix",required=True,type=Path); p.add_argument("--out-dir",required=True,type=Path); p.add_argument("--force",action="store_true"); a=p.parse_args()
    try: result=materialize(load_json(a.matrix),a.out_dir,force=a.force)
    except MaterializeError as exc: print(f"ERROR: {exc}"); return 2
    print(json.dumps({"run_id":result.get("run_id"),"jobs":len(result["jobs"]),"index":(a.out_dir/"dispatch-index.json").as_posix()},ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())
