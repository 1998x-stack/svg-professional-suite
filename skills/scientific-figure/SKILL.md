---
name: scientific-figure
description: Design accurate scientific figures, research-method diagrams, neural-network schematics, mathematical illustrations, and publication-aware plots.
---
# Scientific Figure

Preserve supplied data, methods, equations, units, sample sizes, uncertainty, and missingness. Label conceptual diagrams as conceptual; never present them as experimental results. Quantitative figures must retain source data and transformation provenance.

Classify the task as data plot, method/workflow, mechanism schematic, mathematical illustration, experimental setup, or multi-panel figure. Identify target venue and consult its current figure requirements. Define panel order, axes, units, annotations, legends, scale bars, and physical size before rendering.

Renderer choices: Matplotlib for data plots, TikZ/PGF for LaTeX-native math, SVG for custom schematics, Inkscape for vector composition, BioRender only when licensing is confirmed. These are optional external tools, not bundled integrations.

Keep labels editable when possible and preserve source code/data with SVG/PDF.
