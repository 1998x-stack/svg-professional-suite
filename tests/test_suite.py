import json, tempfile, unittest
from pathlib import Path
from scripts.generate_svg import generate_svg
from scripts.validate_svg import validate_svg

ROOT=Path(__file__).resolve().parents[1]
SPEC=json.loads((ROOT/"examples/architecture/multi-agent-research.graph.json").read_text())

class SuiteTests(unittest.TestCase):
    def test_graph_generates_svg(self):
        svg=generate_svg(SPEC)
        self.assertIn("<title>Multi-Agent Research Workflow</title>",svg)
        self.assertIn("marker-end",svg)
    def test_cycles_are_rejected(self):
        spec={**SPEC,"edges":[*SPEC["edges"],{"from":"synthesizer","to":"planner"}]}
        with self.assertRaises(ValueError): generate_svg(spec)
    def test_unsafe_color_is_rejected(self):
        spec=json.loads(json.dumps(SPEC)); spec["nodes"][0]["fill"]='red" onload="alert(1)'
        with self.assertRaises(ValueError): generate_svg(spec)
    def test_svg_validator_accepts_safe_svg(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"safe.svg"
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><title>Safe</title><desc>Safe</desc><rect id="a" width="2" height="2"/></svg>')
            self.assertEqual(validate_svg(path)["status"],"passed")
    def test_svg_validator_rejects_script_and_events(self):
        for bad in ['<script>alert(1)</script>','<g onclick="alert(1)"/>','<image href="https://example.org/x"/>']:
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as d:
                path=Path(d)/"bad.svg"; path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'+bad+'</svg>')
                self.assertEqual(validate_svg(path)["status"],"failed")
    def test_schema_and_skill_inventory(self):
        schema=json.loads((ROOT/"core/schemas/graph-spec.schema.json").read_text())
        self.assertEqual(schema["title"],"GraphSpec")
        self.assertEqual(len(list((ROOT/"skills").glob("*/SKILL.md"))),6)

if __name__=="__main__": unittest.main()
