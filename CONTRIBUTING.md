# Contributing

Thank you for helping keep this package transparent, reproducible, privacy-conscious, and clear about what it does not implement.

## Development setup

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r scripts/requirements.txt
python -m pip install -r tests/requirements.txt
python -m unittest discover -s tests -v
```

## Contribution expectations

Keep changes focused and document user-facing changes in `SKILL.md`, relevant protocols/references, `docs/methods-and-limitations.md`, examples, and `CHANGELOG.md`. Add tests for changed behavior, edge cases, and input validation. For new calculations, document assumptions, blank behavior, numeric precision, and independent fixture checks. Tests must use fabricated data; never attach private customer, financial, or other sensitive source files to public issues or pull requests.

Do not describe the project as Microsoft Power BI or a replacement. Label DAX/M as unexecuted unless tested in Power BI, identify helper scope precisely, and document unsupported behavior rather than asserting parity. Do not commit credentials, private data, local environments, generated reports containing personal data, or machine-specific paths.

## Pull requests

Explain the user problem, changes, tests run, limitations, and any effect on the JSON contract. Preserve backward compatibility where practical; if a field or behavior changes, update the runtime reference and sample output. This project is distributed under the MIT License; see [`LICENSE`](LICENSE) and [`docs/release-review.md`](docs/release-review.md) for the release status.
