#!/usr/bin/env python3
"""Generate standalone SVG for simple directed acyclic GraphSpec diagrams."""
from __future__ import annotations
import argparse, json, re
from collections import defaultdict, deque
from html import escape
from pathlib import Path

THEMES = {
    "light": ("#FFFFFF", "#172033", "#64748B", "#EFF6FF", "#2563EB"),
    "dark": ("#0F172A", "#F8FAFC", "#CBD5E1", "#172554", "#60A5FA"),
    "paper": ("#FCFBF8", "#292524", "#78716C", "#F5F5F4", "#57534E"),
}
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
COLOR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}|[A-Za-z]{1,24}|rgba?\(\s*[0-9.% ,]+\))$")

def _color(value: str, field: str) -> str:
    if not isinstance(value, str) or not COLOR_RE.fullmatch(value.strip()):
        raise ValueError(f"Unsafe or unsupported color in {field}: {value!r}")
    return value.strip()

def _layout(spec):
    nodes, edges, layout = spec["nodes"], spec["edges"], spec["layout"]
    ids = [n["id"] for n in nodes]
    if len(set(ids)) != len(ids):
        raise ValueError("Node IDs must be unique.")
    if any(not ID_RE.fullmatch(i) for i in ids):
        raise ValueError("Node IDs must start with a letter and contain only letters, digits, _ or -.")
    if any(not isinstance(n.get("label"), str) or not n["label"].strip() for n in nodes):
        raise ValueError("Every node needs a non-empty label.")
    known = set(ids)
    if any(e.get("from") not in known or e.get("to") not in known for e in edges):
        raise ValueError("Every edge must reference existing nodes.")
    direction = layout.get("direction")
    if direction not in ("TB", "LR"):
        raise ValueError("layout.direction must be TB or LR.")
    w, h = layout.get("node_width", 190), layout.get("node_height", 76)
    rg, ng, margin = layout.get("rank_gap", 110), layout.get("node_gap", 42), layout.get("margin", 48)
    if not (80 <= w <= 500 and 40 <= h <= 300 and 30 <= rg <= 500 and 20 <= ng <= 500 and 10 <= margin <= 500):
        raise ValueError("Layout dimensions are outside supported bounds.")
    out, indegree = defaultdict(list), {i: 0 for i in ids}
    for e in edges:
        out[e["from"]].append(e["to"])
        indegree[e["to"]] += 1
    q = deque(i for i in ids if indegree[i] == 0)
    ranks = {i: 0 for i in q}
    visited = set()
    while q:
        cur = q.popleft()
        visited.add(cur)
        for nxt in out[cur]:
            ranks[nxt] = max(ranks.get(nxt, 0), ranks[cur] + 1)
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    if len(visited) != len(ids):
        raise ValueError("Native renderer requires an acyclic graph; use Graphviz for cyclic graphs.")
    groups = defaultdict(list)
    for n in nodes:
        groups[ranks[n["id"]]].append(n)
    title_width = sum(21 if ord(c) > 0x2E7F else (6 if c.isspace() else 12) for c in spec["title"]) + 8
    max_rank = max(groups)
    pos = {}
    if direction == "TB":
        max_count = max(map(len, groups.values()))
        cw = max(max_count*w + (max_count-1)*ng + 2*margin, title_width + 2*margin)
        ch = (max_rank+1)*h + max_rank*rg + 2*margin + 54
        for rank, group in groups.items():
            roww = len(group)*w + (len(group)-1)*ng
            for ix, node in enumerate(group):
                pos[node["id"]] = ((cw-roww)/2 + ix*(w+ng), margin+44+rank*(h+rg))
    else:
        max_count = max(map(len, groups.values()))
        cw = max((max_rank+1)*w + max_rank*rg + 2*margin, title_width + 2*margin)
        ch = max_count*h + (max_count-1)*ng + 2*margin + 54
        for rank, group in groups.items():
            colh = len(group)*h + (len(group)-1)*ng
            for ix, node in enumerate(group):
                pos[node["id"]] = (margin+rank*(w+rg), margin+44+(ch-2*margin-54-colh)/2+ix*(h+ng))
    return pos, (cw, ch), (w, h, margin), direction

def generate_svg(spec):
    if spec.get("schema_version") != "1.0" or not isinstance(spec.get("title"), str) or not spec["title"].strip():
        raise ValueError("schema_version 1.0 and non-empty title are required.")
    if not isinstance(spec.get("nodes"), list) or not spec["nodes"] or not isinstance(spec.get("edges"), list):
        raise ValueError("nodes must be non-empty and edges must be an array.")
    theme = spec.get("theme", "light")
    if theme not in THEMES:
        raise ValueError(f"Unsupported theme: {theme}")
    bg, fg, muted, node_fill, node_stroke = THEMES[theme]
    pos, (cw,ch), (w,h,margin), direction = _layout(spec)
    esc = escape
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(cw)}" height="{int(ch)}" viewBox="0 0 {int(cw)} {int(ch)}" role="img">',
           f"<title>{esc(spec['title'])}</title>", f"<desc>{esc(spec.get('description','Generated directed graph diagram.'))}</desc>",
           '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="'+muted+'"/></marker></defs>',
           f'<rect width="{int(cw)}" height="{int(ch)}" fill="{bg}"/>',
           f'<text x="{margin}" y="{margin+12}" font-family="Inter,Arial,sans-serif" font-size="22" font-weight="700" fill="{fg}">{esc(spec["title"])}</text>']
    for edge in spec["edges"]:
        sx,sy = pos[edge["from"]]; tx,ty = pos[edge["to"]]
        if direction == "TB":
            x1,y1,x2,y2 = sx+w/2,sy+h,tx+w/2,ty
            mid=(y1+y2)/2; path=f"M {x1:.1f} {y1:.1f} V {mid:.1f} H {x2:.1f} V {y2-5:.1f}"
            lx,ly=(x1+x2)/2,mid-7
        else:
            x1,y1,x2,y2 = sx+w,sy+h/2,tx,ty+h/2
            mid=(x1+x2)/2; path=f"M {x1:.1f} {y1:.1f} H {mid:.1f} V {y2:.1f} H {x2-5:.1f}"
            lx,ly=mid,(y1+y2)/2-7
        out.append(f'<path d="{path}" fill="none" stroke="{muted}" stroke-width="2" marker-end="url(#arrow)"/>')
        if edge.get("label"):
            out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="11" fill="{muted}" stroke="{bg}" stroke-width="4" paint-order="stroke fill">{esc(edge["label"])}</text>')
    for node in spec["nodes"]:
        x,y=pos[node["id"]]; fill=_color(node.get("fill",node_fill),node["id"]+".fill"); stroke=_color(node.get("stroke",node_stroke),node["id"]+".stroke")
        out.append(f'<g id="node-{esc(node["id"])}"><rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        if node.get("subtitle"):
            out.append(f'<text x="{x+w/2:.1f}" y="{y+h/2-4:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="14" font-weight="700" fill="{fg}">{esc(node["label"])}</text>')
            out.append(f'<text x="{x+w/2:.1f}" y="{y+h/2+17:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="11" fill="{muted}">{esc(node["subtitle"])}</text>')
        else:
            out.append(f'<text x="{x+w/2:.1f}" y="{y+h/2+5:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="14" font-weight="700" fill="{fg}">{esc(node["label"])}</text>')
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)+"\n"

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--spec",required=True,type=Path); p.add_argument("--output",required=True,type=Path); a=p.parse_args()
    try:
        spec=json.loads(a.spec.read_text(encoding="utf-8")); svg=generate_svg(spec)
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(svg,encoding="utf-8")
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        p.error(str(exc))
    print(f"Generated {a.output}")
if __name__=="__main__": main()
