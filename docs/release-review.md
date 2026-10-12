# Release status

**Status: public release, distributed under the MIT License.** The package is published at [Kaamchor-Solutions/PowerBI-Simulator-Skills](https://github.com/Kaamchor-Solutions/PowerBI-Simulator-Skills).

- Companion/reference repository: [Kaamchor-Solutions/SPSS-Simulator-Skills](https://github.com/Kaamchor-Solutions/SPSS-Simulator-Skills)
- License: [MIT License](../LICENSE), copyright © 2026 Kaamchor Solutions.
- Citation metadata: [`CITATION.cff`](../CITATION.cff) identifies version 0.1.0 and the repository URL.
- Package scope and limitations are documented in the README and [`docs/methods-and-limitations.md`](methods-and-limitations.md). This independent project is not affiliated with or endorsed by Microsoft.

The repository contains the published source and tests. The local deterministic ZIP is a separate source archive; its checksum and integrity are verified during release validation. No claim is made that this package executes general DAX or Power Query M, integrates with a Power BI tenant, or matches Microsoft's products.

The archive builder reads the root [`release-manifest.txt`](../release-manifest.txt) as an explicit file allowlist and includes that manifest in the ZIP. Git is not required to build an archive from a source checkout, and a missing or invalid manifest is an error—there is no recursive or Git-based fallback. Unlisted files, including ignored local data, credentials, generated reports, and unrelated files, are not packaged. Review this list whenever release contents change; only add files approved for public distribution.
