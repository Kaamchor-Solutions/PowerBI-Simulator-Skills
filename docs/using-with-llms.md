# Using the simulator with different LLMs

The repository separates an LLM workflow skill from a deterministic helper. Providers accept different combinations of project instructions, file attachments, skill folders, and code tools; no single import format or tool capability is universal.

## ChatGPT, Claude, or another chat product

Use `SYSTEM_PROMPT.md` as the starting instruction in the product's current custom-instructions/project-instructions feature, if available. Attach `SKILL.md` and only the relevant files under `protocols/` and `references/`. Upload source data separately using the host's supported file workflow and only when authorized. Ask the model to state what it can actually access and distinguish data it inspected from assumptions.

A project prompt does not automatically run this repository's Python code. To obtain exact supported helper results, use a runtime that can read both the repository and data and execute `scripts/analyze.py`; otherwise run it locally and paste the resulting JSON/Markdown into the LLM. A chat-only model can still draft DAX/M, explain a schema, plan visuals, or interpret pasted output, but cannot truthfully profile inaccessible files or calculate large datasets.

For continuity across chats/providers, save the current state with [`../templates/workspace-state.md`](../templates/workspace-state.md), then provide it with the data/schema the next conversation can access. State remains a text note, not a native model file.

## Skills-aware coding harness

If a coding harness supports the Agent Skills convention, install the complete repository in a skill folder named `powerbi-simulator`, following the host's current personal/project directory rules. Keep `SKILL.md`, `protocols/`, `references/`, and `scripts/` together. Some harnesses expose slash commands; others load skills based on description or a tool call. Do not assume a specific path or command without checking the provider's current documentation.

The harness also needs permission to access the user's files and execute Python. Install the dependency from `scripts/requirements.txt` in the interpreter it will use. A cloud-hosted model's runtime may not be able to see a local file or skill checkout.

## Any other LLM

Paste `SYSTEM_PROMPT.md` as an instruction, then supply only the task-relevant schema, fabricated sample, or authorized data. If the LLM cannot load linked files, also provide the relevant protocol/reference text; if it cannot execute code, ask it for a plan or runnable code rather than results. Provider features and data-handling rules vary and can change, so verify them in the host's current documentation.


## Check behavior in multiple hosts

Use the portable [LLM conformance suite](../tests/llm_conformance/README.md) to compare response behavior across ChatGPT, Claude, coding harnesses, or other hosts. It uses the same fabricated prompts, records outputs locally, and applies simple regex checks; it is not a benchmark or proof of semantic correctness. Keep each host's file/code/tool availability consistent with the scenario in each prompt and manually review the full responses.
