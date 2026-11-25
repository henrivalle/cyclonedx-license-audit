# CycloneDX License Audit

[English](README.md)

Identifique componentes sem metadados úteis de licença em SBOMs CycloneDX JSON 1.5, 1.6 e 1.7. O relatório inclui o caminho de cada componente, inclusive os aninhados. `--include-root` inclui o componente principal. `--fail-on-missing` retorna 1 para lacunas. A checagem avalia a presença dos metadados.

Na raiz do repositório, use Python 3.9 ou posterior.

```bash
python3 -m cyclonedx_license_audit examples/bom.json --fail-on-missing
```

[Como contribuir](CONTRIBUTING.md) · [Licença MIT](LICENSE)
