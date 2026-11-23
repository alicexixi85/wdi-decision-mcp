# WDI — Women's Decision Intelligence MCP

An open-source [Model Context Protocol](https://modelcontextprotocol.io) server that helps Claude, ChatGPT, Cursor, Windsurf, or any MCP client structure **high-stakes career and life decisions** with deterministic math and evidence grading instead of generic reassurance: quitting a "golden handcuffs" job, taking a career break for caregiving, relocating, or weighing a verbal promise against what you actually control.

Zero dependencies, Python 3.10+, 100% local execution (`stdio`): **no API keys, no network calls — your personal numbers never leave your machine.**

---

## Option 1: Zero-Install Chat Prompt (No Python or MCP Needed)

Copy and paste [`wdi_lite_prompt.md`](wdi_lite_prompt.md) directly into Claude, ChatGPT, or any assistant to run the 6-dimension constraint checklist and 4-tier evidence grading immediately in your browser.

---

## Option 2: Local Python `stdio` MCP / Docker (100% Offline Privacy)

```bash
git clone https://github.com/alicexixi85/wdi-decision-mcp.git
```

**Claude Desktop (`claude_desktop_config.json`) / Cursor (`~/.cursor/mcp.json`) / Windsurf:**

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

**Docker:**

```bash
docker build -t wdi-decision-mcp . && docker run -i --rm wdi-decision-mcp
```

Listed in the [official MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=wdi-decision-mcp) as `io.github.alicexixi85/wdi-decision-mcp` and on [Glama](https://glama.ai/mcp/servers/alicexixi85/wdi-decision-mcp).

---

## Tools

| Tool | What it does |
|---|---|
| `six_dimension_checklist` | The six questions to answer for every option: cash runway, irreversible time windows, care load, safety floor (health insurance, housing), actual control rights, institutional bridges (leave, severance, part-time). |
| `calculate_runway` | Months of runway after a change, the cash needed for a safety floor (default 6 months of essentials), and how long you can experiment before touching it. |
| `grade_evidence` | Tags each claim behind the decision as `KNOWN`, `ASSUMED`, `UNKNOWN`, or `SYNTHETIC` (hope or verbal promise) with a concrete verification step for each. |
| `compare_options` | Ranks 2+ options scored 1-5 on the six dimensions with optional weights. An option with a redline (score 1, e.g. losing health insurance) is ranked last regardless of its average. |

## Example prompts

- "I have $40k in savings, $3,500 of essential costs a month and would earn $1,000 freelancing. If I quit, how long is my runway with a 6-month safety floor?"
- "Grade the evidence: my manager promised a promotion next year; the offer letter says $120k; I don't know the severance policy."
- "Compare staying, a 4-day week, and quitting across the six dimensions."

## Limits

This is a decision-structuring aid. It is **not** legal, tax, financial, medical, or mental-health advice. For contracts, prenups or divorce, taxes, benefits, or safety concerns, talk to a qualified professional. If you are in danger, contact local emergency services.

## Full WDI 2.4.3 Toolkit

This repository is complete and free (MIT). The separate paid WDI 2.4.3 toolkit ($35 one-time, [Gumroad](https://dejunchen770231.gumroad.com/l/wdi-womens-decision-intelligence)) is a 75-file bilingual (EN/ZH) skill package for AI agents: a root SKILL file, research profiles, frameworks and playbooks, synthetic decision-card examples, and jurisdiction-sensitive research cards (marked as needing verification).

- **Support**: `support@usethelever.com`

## License

MIT

<!-- mcp-name: io.github.alicexixi85/wdi-decision-mcp -->

## Sister Zero-Install Remote MCP Servers (`usethelever.com`)

- **AI Search & GEO Readiness Remote MCP**: `https://mcp.usethelever.com/geo-audit/mcp` ([Catalog & Docs](https://mcp.usethelever.com/ai-tools))
- **U.S. Market Regime & Prop-Firm Drawdown Remote MCP**: `https://mcp.usethelever.com/market-regime/mcp`
