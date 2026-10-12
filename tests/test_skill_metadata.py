"""Regression tests for installable Agent Skill metadata."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEGACY_DESCRIPTION = (
    "Guide Power BI-style analytics tasks with an LLM: inspect accessible tabular data, "
    "shape a semantic model, draft DAX and Power Query M, plan report pages and visuals, "
    "compute a constrained subset with the bundled helper, and interpret results. Use "
    "for Power BI learning, modeling, DAX/Power Query drafting, report planning, or "
    "uploaded CSV/TSV/XLSX analysis. This is a simulation, not Microsoft's Power BI "
    "engine or desktop/service app."
)


class SkillMetadataTests(unittest.TestCase):
    def test_skill_frontmatter_is_valid_yaml_with_required_fields(self):
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill_text.startswith("---\n"), "SKILL.md must begin with YAML frontmatter")
        frontmatter, separator, _ = skill_text[4:].partition("\n---\n")
        self.assertTrue(separator, "SKILL.md frontmatter must have a closing delimiter")

        metadata = yaml.safe_load(frontmatter)
        self.assertIsInstance(metadata, dict)
        self.assertIsInstance(metadata.get("name"), str)
        self.assertTrue(metadata["name"].strip())
        self.assertIsInstance(metadata.get("description"), str)
        self.assertTrue(metadata["description"].strip())
        self.assertEqual(metadata["description"], LEGACY_DESCRIPTION)

    def test_legacy_unquoted_colon_description_is_rejected(self):
        legacy_frontmatter = f"name: powerbi-simulator\ndescription: {LEGACY_DESCRIPTION}\n"
        with self.assertRaises(yaml.YAMLError):
            yaml.safe_load(legacy_frontmatter)


if __name__ == "__main__":
    unittest.main()
