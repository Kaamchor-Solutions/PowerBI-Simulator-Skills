# Report design protocol

1. Tie each page to a user question and an intended decision. State audience, grain, time range, and default filter state.
2. For every proposed visual, specify purpose, visual type, fields/measure, aggregation, sorting, units/format, and meaningful interactions. Avoid decorative charts without a question.
3. Propose an overview page only when useful: concise KPI cards, a trend, one or two explanatory breakdowns, and clear slicers. Add drill-through/detail pages only for a user task.
4. Check visual encoding: appropriate axis baseline, date granularity, category count, units, color contrast, color-blind accessibility, labels, tooltip content, and mobile/readability constraints.
5. Separate facts computed by the helper from values proposed in DAX or conceptual mock data. If values are unknown, use placeholders rather than plausible invented figures.
6. Present a wireframe in Markdown/text with page title, layout regions, visual specs, slicers, interactions, accessibility notes, and DAX dependencies. Call it a **report simulation/wireframe**, not a rendered Power BI page.
7. For a real deliverable, the user must implement and verify the design in an authorized Power BI environment. This repository cannot create or publish a `.pbix` report.
