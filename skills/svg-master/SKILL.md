---
name: svg-master
description: Route diagram, chart, infographic, scientific figure, and illustration requests to specialist workflows and enforce reproducible SVG quality.
---
# SVG Master

1. Identify purpose, audience, destination, language, dimensions, and required formats.
2. Route to architecture-diagram, scientific-figure, infographic, business-visualization, or vector-illustration. For mixed requests, define separate sub-artifacts.
3. Extract facts, labels, relationships, units, formulas, uncertainty, and provenance before drawing. Never invent missing content.
4. Create a domain specification using the schemas in core/schemas.
5. Select the simplest suitable renderer. Consult the renderer matrix in docs/renderer-matrix.md when available; external tools are optional unless installed and tested.
6. Plan hierarchy, reading order, canvas, spacing, typography, color, and layers before rendering.
7. Generate editable SVG and preserve source specification.
8. Run scripts/qa_pipeline.py. Security and XML failures block delivery.
9. Inspect a rendered preview when an actual renderer is available. Otherwise state that visual review was skipped.
10. Deliver SVG, source, manifest, and QA report.

Routing: system/service/Agent/data flow -> architecture; research/method/equation -> scientific; timeline/knowledge graph/concept map -> infographic; KPI/finance/strategy -> business; logo/icon/illustration -> vector illustration.

Rules: SVG is the primary artifact; PNG is only a preview. Keep text editable where possible. Never claim a renderer, visual inspection, or journal compliance that was not performed.
