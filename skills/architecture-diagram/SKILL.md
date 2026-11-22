---
name: architecture-diagram
description: Create accurate system architecture, Agent workflow, data pipeline, deployment, sequence, and dependency diagrams as editable SVG.
---
# Architecture Diagram

Inventory system boundaries, actors, components, interfaces, stores, protocols, directionality, and trust boundaries. Mark proposed elements as proposals.

Choose context, container, component, deployment, sequence, data-flow, ER, state, or dependency view. Build explicit node and edge inventories; every edge must represent a real relationship and should be labeled when ambiguous. Group by layer, service, owner, or trust boundary. Use TB for layered systems and LR for pipelines.

Renderer choices: D2 for rich architecture, Mermaid for compact documentation, Graphviz for graph-heavy layouts, PlantUML for UML, native renderer for supported acyclic GraphSpec. Only native GraphSpec rendering is implemented here; external tools must be detected and tested before use.

Avoid invented services, protocols, dependencies, or decorative arrows. Deliver SVG, source specification, and QA report.
