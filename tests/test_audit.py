import unittest

from cyclonedx_license_audit import audit


def bom(components=(), **fields):
    return {"bomFormat": "CycloneDX", "specVersion": "1.7", "components": list(components), **fields}


class AuditTests(unittest.TestCase):
    def test_nested_components_remain_distinct(self):
        result = audit(bom([{
            "name": "component",
            "licenses": [{"license": {"id": "MIT"}}],
            "components": [{"name": "component", "version": "1.0"}],
        }]))
        self.assertEqual([(row["path"], row["status"]) for row in result], [
            ("components[0]", "recorded"),
            ("components[0].components[0]", "missing"),
        ])

    def test_expression_and_custom_name_are_recorded(self):
        result = audit(bom([
            {"name": "a", "licenses": [{"expression": "MIT OR Apache-2.0"}]},
            {"name": "b", "licenses": [{"license": {"name": "Custom License"}}]},
        ]))
        self.assertEqual([row["licenses"] for row in result],
                         [["MIT OR Apache-2.0"], ["Custom License"]])

    def test_empty_and_placeholder_are_distinguished(self):
        result = audit(bom([
            {"name": "empty", "licenses": []},
            {"name": "unknown", "licenses": [{"license": {"name": "NOASSERTION"}}]},
        ]))
        self.assertEqual([row["status"] for row in result], ["missing", "placeholder"])

    def test_bom_root_is_opt_in(self):
        document = bom(metadata={"component": {"name": "application"}})
        self.assertEqual(audit(document), [])
        self.assertEqual(audit(document, include_root=True)[0]["path"], "metadata.component")

    def test_rejects_wrong_format_and_malformed_license_entries(self):
        documents = [
            {"bomFormat": "SPDX", "specVersion": "1.7"},
            {"bomFormat": "CycloneDX", "specVersion": "2.0"},
            bom([{"name": "bad", "licenses": "MIT"}]),
            bom([{"name": "bad", "licenses": [{"license": {}}]}]),
            bom([{"name": "bad", "licenses": [{"license": {"id": "MIT"}, "expression": "MIT"}]}]),
        ]
        for doc in documents:
            with self.subTest(doc=doc), self.assertRaises(ValueError):
                audit(doc)
