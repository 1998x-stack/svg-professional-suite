#!/usr/bin/env python3
"""Validate static SVG structure and enforce the safe SVG profile."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

NS="http://www.w3.org/2000/svg"
URL_RE=re.compile(r"url\(\s*['\"]?(?!#)[^)]+\)",re.I)

def validate_svg(path: Path, max_bytes: int=5_000_000):
    errors=[]; warnings=[]
    report={"file":str(path),"status":"failed","errors":errors,"warnings":warnings,"checks":{}}
    if not path.is_file():
        errors.append("Input file does not exist."); return report
    size=path.stat().st_size; report["size_bytes"]=size
    if size>max_bytes:
        errors.append(f"File exceeds {max_bytes} bytes."); return report
    try:
        raw=path.read_bytes(); raw.decode("utf-8")
    except UnicodeDecodeError:
        errors.append("SVG must be UTF-8."); return report
    except OSError as exc:
        errors.append(f"Read error: {exc}"); return report
    if re.search(br"<!DOCTYPE|<!ENTITY",raw,re.I):
        errors.append("DOCTYPE and ENTITY declarations are forbidden."); return report
    try: root=ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"XML parse error: {exc}"); return report
    local=lambda tag: tag.rsplit("}",1)[-1]
    if local(root.tag)!="svg" or not root.tag.startswith("{"+NS+"}"):
        errors.append("Root must be SVG in the standard SVG namespace.")
    report["checks"]["xml_parse"]=True
    vb=root.attrib.get("viewBox","")
    try:
        x,y,w,h=map(float,re.split(r"[ ,]+",vb.strip()))
        if w<=0 or h<=0: raise ValueError()
        report["view_box"]=vb
    except (ValueError,TypeError):
        errors.append("A valid positive-width and positive-height viewBox is required.")
    ids=set(); count=0
    for el in root.iter():
        count+=1; name=local(el.tag)
        if name in {"script","foreignObject"}: errors.append(f"Forbidden element <{name}>.")
        for key,value in el.attrib.items():
            k=local(key).lower()
            if k.startswith("on"): errors.append(f"Event handler {key} is forbidden.")
            if k=="id":
                if value in ids: errors.append(f"Duplicate id {value!r}.")
                ids.add(value)
            if k=="href" and value and not value.startswith("#"): errors.append(f"External href is forbidden: {value[:80]}")
            if URL_RE.search(value): errors.append("External CSS url() reference is forbidden.")
        if name=="style":
            css="".join(el.itertext())
            if URL_RE.search(css) or re.search(r"@import",css,re.I): errors.append("External CSS resources are forbidden.")
    if root.find(f"{{{NS}}}title") is None: warnings.append("Missing <title>.")
    if root.find(f"{{{NS}}}desc") is None: warnings.append("Missing <desc>.")
    report["element_count"]=count; report["checks"]["safe_static_profile"]=not errors
    report["status"]="passed" if not errors else "failed"
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("svg",type=Path); p.add_argument("--report",type=Path); p.add_argument("--max-bytes",type=int,default=5_000_000); a=p.parse_args()
    result=validate_svg(a.svg,a.max_bytes); text=json.dumps(result,ensure_ascii=False,indent=2); print(text)
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(text+"\n",encoding="utf-8")
    raise SystemExit(0 if result["status"]=="passed" else 1)
if __name__=="__main__": main()
