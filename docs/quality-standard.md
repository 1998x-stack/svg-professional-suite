# SVG Quality Standard

Blocking checks: UTF-8, XML parsing, SVG namespace, positive viewBox, unique IDs, no script/foreignObject, no event attributes, and no external href/CSS resources.

Warnings: missing title/description and absent physical dimensions. Static validation cannot prove that labels are unclipped, edges avoid text, or the composition is aesthetically effective. Visual review is a separate gate and must be reported as not run when no renderer is available.

The default profile is static, self-contained SVG. Interactive SVG requires a separate reviewed policy. Meaningful figures should include title and description, sufficient contrast, and non-color cues.
