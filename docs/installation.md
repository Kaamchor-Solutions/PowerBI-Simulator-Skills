# Installation and use with LLMs

This repository contains two separate parts: `SKILL.md` tells an LLM how to follow the workflow, while `scripts/` performs only the explicitly supported data checks and aggregates. Installing instructions does not grant an LLM file access, Python, connectors, persistent memory, Microsoft Power BI, or DAX/M execution. Provider behavior and project features can vary by plan and change over time.

## Use a local checkout

The public repository is distributed under the MIT License. Clone it and install the optional helper dependency as follows:

```bash
git clone https://github.com/Kaamchor-Solutions/PowerBI-Simulator-Skills.git
cd PowerBI-Simulator-Skills
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r scripts/requirements.txt
python scripts/analyze.py --config examples/demo_sales/net-sales-by-category-request.json
python -m unittest discover -s tests -v
```

Use `python3` instead of `python` where needed. The helper is pure Python apart from `openpyxl`, which is required only for `.xlsx`. For CSV/TSV-only use, the standard library is sufficient. Preserve the entire repository layout so relative protocol and script links work.

## Skills-aware coding harness

If your coding agent supports the open Agent Skills folder convention, install the whole repository under a skill directory named `powerbi-simulator` in the location documented by that harness. Keep `SKILL.md`, `protocols/`, `references/`, `scripts/`, and templates together. Some tools expose slash-command invocation; others select skills automatically from the prompt. The exact folder and invocation are host-specific—follow current provider documentation.

When the agent can run Python, install the helper dependency in the same environment it will use. Tell the agent to run only the supported helper actions and inspect `valid` before interpretation. A host sandbox may not be able to reach your local files, even if a local terminal can.

## ChatGPT, Claude, or another chat-only LLM

Use the provider's current project/custom-instructions feature, if available:

1. Paste `SYSTEM_PROMPT.md` into the project's instructions.
2. Add `SKILL.md` and the relevant protocol/reference files as project knowledge or attachments. For a single task, attach just the relevant data and instructions instead of every repository file.
3. Upload source data only if you are authorized and the provider's data handling is suitable.
4. If the host has a real code/data-analysis tool, it may perform work independently; do not assume that it has this repository's helper. To run the bundled helper, install/run it in an environment that can access both the repository and data.
5. If the LLM has no code execution or file access, it can explain concepts, draft DAX/M, design a model/report, and interpret pasted output—but it cannot profile inaccessible files or compute large datasets.

A prompt pasted into ChatGPT, Claude, or another model is not the same as a native skill installation. Linked files are not automatically loaded unless the host can access them. Re-check the provider's current documentation for project, file, and code-tool behavior.

## Portability check

From the repository root, run the example requests and unit tests. For consistent host-to-host checks, follow [`../tests/llm_conformance/README.md`](../tests/llm_conformance/README.md) to run the same fabricated prompts in each target LLM and score responses locally. No Windows or macOS execution is claimed by the current CI artifact; the helper is written with portable Python paths and encodings, but should be tested on each target platform before promising support.
