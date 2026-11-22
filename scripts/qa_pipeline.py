#!/usr/bin/env python3
"""Run deterministic SVG validation and write a QA report and manifest."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from validate_svg import validate_svg

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--input",required=True,type=Path); p.add_argument("--output-dir",required=True,type=Path); p.add_argument("--task-type",default="unknown"); p.add_argument("--renderer",default="unknown"); a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True); result=validate_svg(a.input)
    (a.output_dir/"validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    status=result["status"]; now=datetime.now(timezone.utc).isoformat()
    report={"schema_version":"1.0","input":str(a.input),"created_at":now,"overall_status":status,"steps":{"static_validation":status,"visual_review":"not_run","optimization":"not_run"}}
    (a.output_dir/"qa-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest={"schema_version":"1.0","artifact":str(a.input),"task_type":a.task_type,"created_at":now,"renderer":{"name":a.renderer},"qa":{"status":status,"report":str(a.output_dir/"qa-report.json")},"notes":["Visual review and optimization were not run by this dependency-free pipeline."]}
    (a.output_dir/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if status=="passed" else 1)
if __name__=="__main__": main()
