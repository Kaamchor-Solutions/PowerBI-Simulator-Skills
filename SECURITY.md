# Security policy

## Scope

Security reports are welcome for the Python helper, documentation, and repository configuration. The helper is intended to read local files and emit summaries/reports; it is not designed to upload or transmit datasets. The selected LLM host may have separate data handling, retention, and execution behavior.

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities in a public issue. Use GitHub's private vulnerability reporting/security advisory feature if enabled for the repository. Otherwise contact maintainers privately through a method listed on the organization profile. Include the affected version/commit, impact, safe reproduction steps, and a proof of concept that contains no real private data or credentials. No response-time SLA is promised.

## Safe data handling

Use fabricated, minimal fixtures in tests and bug reports. Do not commit source data, credentials, or personal identifiers. Do not upload sensitive files to an LLM or external service unless authorized and covered by an appropriate review. Review generated reports and small-group summaries before sharing; aggregation does not guarantee anonymity.

The CLI refuses output paths that resolve to the request or a declared source file, and checks existing file identity to catch hard-link aliases. This guard reduces accidental overwrite risk but is not a race-proof sandbox and does not make use on a hostile shared filesystem safe.
