# WDI — Women's Decision Intelligence MCP

An open-source [Model Context Protocol](https://modelcontextprotocol.io) server that helps Claude, Cursor or any MCP client structure **high-stakes career and life decisions** with numbers and evidence instead of generic reassurance: quitting a "golden handcuffs" job, taking a career break for caregiving, relocating, or weighing a family promise against what you actually control.

Zero dependencies, Python 3.10+, everything runs locally.

## Tools

| Tool | What it does |
|---|---|
| `six_dimension_checklist` | The six questions to answer for every option: cash runway, irreversible time windows, care load, safety floor (health insurance, housing), actual control rights, institutional bridges (leave, severance, part-time). |
| `calculate_runway` | Months of runway after a change, the cash needed for a safety floor (default 6 months of essentials), and how long you can experiment before touching it. |
| `grade_evidence` | Tags each claim behind the decision as `KNOWN`, `ASSUMED`, `UNKNOWN` or `SYNTHETIC` (hope or verbal promise) with a next step for each. |
| `compare_options` | Ranks 2+ options scored 1-5 on the six dimensions with optional weights. An option with a redline (score 1, e.g. losing health insurance) is ranked last regardless of its average. |

## Install

```bash
git clone https://github.com/alicexixi85/wdi-decision-mcp.git
```

```json
{
  "mcpServers": {
    "wdi": {
      "command": "python3",
      "args": ["/absolute/path/to/wdi-decision-mcp/server.py"]
    }
  }
}
```

Docker: `docker build -t wdi-decision-mcp . && docker run -i --rm wdi-decision-mcp`

## Example prompts

- "I have $40k in savings, $3,500 of essential costs a month and would earn $1,000 freelancing. If I quit, how long is my runway with a 6-month safety floor?"
- "Grade the evidence: my manager promised a promotion next year; the offer letter says $120k; I don't know the severance policy."
- "Compare staying, a 4-day week, and quitting across the six dimensions."

There is also a no-install version of the method in [`wdi_lite_prompt.md`](wdi_lite_prompt.md) that you can paste into any chat assistant.

## Limits

This is a decision-structuring aid. It is **not** legal, tax, financial, medical or mental-health advice. For contracts, prenups or divorce, taxes, benefits or safety concerns, talk to a qualified professional. If you are in danger, contact local emergency services.

## Full WDI toolkit

This repository is complete and free (MIT). The separate paid WDI 2.4.3 toolkit ($35, [Gumroad](https://dejunchen770231.gumroad.com/l/wdi-womens-decision-intelligence)) is a 75-file bilingual (EN/ZH) skill package for AI agents: a root SKILL file, research profiles, frameworks and playbooks, synthetic decision-card examples and jurisdiction-sensitive research cards (marked as needing verification).

## License

MIT

<!-- mcp-name: io.github.alicexixi85/wdi-decision-mcp -->
