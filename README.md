# SVG Professional Suite

A composable Agent Skills toolkit for professional, editable, and testable SVG graphics.

## Included
- SVG Master plus five specialist Skills: architecture, scientific figures, infographics, business visualization, and vector illustration.
- Versioned GraphSpec JSON schema and shared design tokens.
- Dependency-free native SVG graph renderer.
- Static SVG safety validator and QA pipeline.
- Unit tests and GitHub Actions CI.

## Quick start
Requires Python 3.10+; core functionality uses only the standard library.

```bash
python scripts/generate_svg.py --spec examples/architecture/multi-agent-research.graph.json --output /tmp/research.svg
python scripts/validate_svg.py /tmp/research.svg --report /tmp/qa.json
python scripts/qa_pipeline.py --input /tmp/research.svg --output-dir /tmp/svg-qa
python -m unittest discover -s tests -v
```

Optional specialist tools include D2, Mermaid, Graphviz, PlantUML, Matplotlib, TikZ/PGF, D3.js, Cytoscape.js, Vega-Lite, ECharts, Inkscape, resvg, and SVGO. They are documented choices, not bundled integrations. Only the native graph renderer and static validator are implemented in this release.

## Principles
1. Content accuracy before decoration; never invent facts, relationships, data, or citations.
2. SVG is the primary artifact; raster files are previews only.
3. Preserve source specifications and provenance.
4. Reject scripts, event attributes, foreign content, and external resource references in static SVG.
5. Distinguish deterministic checks from visual review; never claim an unrun check passed.

## Layout
- `skills/`: six Agent Skills.
- `core/`: schemas and design tokens.
- `scripts/`: generation, validation, and QA.
- `examples/`: reusable source specifications.
- `tests/`: unit and integration tests.

See `AGENTS.md` for contribution and engineering rules. MIT License.
