# CycloneDX License Audit

[Português](README.pt-BR.md)

Find components with missing or placeholder license metadata in a CycloneDX JSON software bill of materials. The report keeps each component's path, so a repeated name in a nested component stays distinguishable.

## Quick start

Run from the repository root with Python 3.9 or later.

```bash
python3 -m cyclonedx_license_audit examples/bom.json --fail-on-missing
```

Give the CLI a CycloneDX 1.5, 1.6, or 1.7 JSON file. It walks the component inventory and nested components. Add `--include-root` to audit `metadata.component`. Missing lists, empty lists, and strings such as `NOASSERTION` are reported. A supplied SPDX identifier, license name, or expression is shown as recorded metadata.

The default run reports findings with status 0. With `--fail-on-missing`, missing or placeholder-only metadata exits 1, as in the example. Invalid input exits 2. This is a metadata coverage check. Use a full schema validator for document validation and a separate analysis for licensing decisions.

## Contributing

Choose a [beginner task](https://github.com/henrivalle/cyclonedx-license-audit/contribute) and use a small synthetic file to show the expected result. [Contributing guide](CONTRIBUTING.md) · [MIT license](LICENSE)

## References

[CycloneDX JSON reference](https://cyclonedx.org/docs/1.7/json/) · [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli)
