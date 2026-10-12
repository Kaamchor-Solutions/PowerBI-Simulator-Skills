# Power BI-Style Analysis Helper

Use this project with ChatGPT, Claude, or another chat AI to explore spreadsheet data and plan a report inspired by Microsoft Power BI. You do **not** need to know how to code to try the included example.

> **Important:** This is not Microsoft Power BI. It does not open or create real Power BI reports, connect to your Power BI account, or publish dashboards. It provides instructions an AI can follow and an optional, limited helper for some simple data checks.

## Try the included example

The example uses made-up sales information. It is safe to use for learning and does not describe real people or sales.

1. Open [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md) and copy its text. In your AI chat app, paste it into the first message, or into the app's project/custom instructions if it has that feature. If your app cannot keep project instructions, paste the text at the beginning of the chat.
2. Open the [example sales files](examples/demo_sales/). Download these three files and attach them to your chat: `customers.csv`, `products.csv`, and `orders.csv`. On GitHub, open each file and choose **Download raw**.
3. Paste this request into the chat:

   > Please look at the three example files I attached. In everyday language, explain what each file contains, how the information might fit together, and suggest a simple one-page sales dashboard. Tell me what you were actually able to inspect. Clearly label suggestions and estimates, and do not make up results.

4. Ask follow-up questions in ordinary language—for example, “What does each row represent?” or “What should I check before trusting these totals?”

The AI app must be able to read the attached files for this to work. Its file and analysis features vary. If it cannot open the files, ask it to explain what it needs, or paste a small, non-sensitive sample instead.

## Use your own data

You can try the same approach with a spreadsheet or data file your AI app accepts:

- Paste the instructions from [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md), then attach only the files needed for your question.
- Ask the AI to explain the tables, suggest how they may relate, draft formulas, or sketch a report layout.
- Ask it to say which files it could actually read and to separate checked results from suggestions or assumptions.

**Protect your information.** Only share data you are allowed to share. Check your AI app's privacy and file-handling settings before uploading anything. Remove or disguise names, account numbers, and other sensitive details when possible. A summary can still contain sensitive information, even if it does not show the original rows.

## What it can—and cannot—do

It can help you understand accessible tables, suggest how tables could fit together, draft formulas used in Power BI, and describe a report layout. If the optional helper is set up and run, it can also perform a limited set of clearly defined checks and calculations on supported files.

It **cannot** act as Power BI itself. It does not open `.pbix` or `.pbip` reports, connect to a Power BI account, create real interactive charts, refresh or publish a report, or run and verify general Power BI formulas. Suggested formulas and dashboard layouts are drafts—not tested Power BI results. The AI's ability to read files or calculate anything depends on the app and features you are using; instructions alone do not give it access.

## Want more detail?

- [What the helper supports and its limitations](docs/methods-and-limitations.md)
- [Using the project with different AI apps](docs/using-with-llms.md)
- [Optional setup and helper instructions](docs/installation.md) — this section is for people comfortable installing software; it is not needed to try the chat example.
- [Example files and their notes](examples/demo_sales/README.md)

This is an independent community project. It is not affiliated with or endorsed by Microsoft. “Power BI” is a Microsoft trademark. The project is shared under the [MIT License](LICENSE).
