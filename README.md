# How to connect Wanderlog to Claude Code, ChatGPT and any AI agent

**Yes, Claude, ChatGPT and other AI agents can work in your Wanderlog account.** Wanderlog has no public API and no official ChatGPT app. Cotlet.dev connects your own Wanderlog account to any AI agent, so the AI can build and edit your trips while you plan in plain words.

## What you can ask

> Make a 5-day Lisbon trip in Wanderlog with 3 places a day, close to each other.

> Add the restaurants from this list to day 2 of my Tokyo trip.

> Reorder my Rome itinerary so each day has the shortest walking route.

> What's still missing in my Iceland trip: hotels, transfers, opening hours?

> Copy my Paris trip and adapt it for a family with two kids.

## Connect in 2 minutes

Get your API key at https://cotlet.dev/app and export it as `COTLET_API_KEY`.

### Claude Code

```bash
claude mcp add --transport http cotlet https://cotlet.dev/mcp/v1 --header "Authorization: Bearer $COTLET_API_KEY"
```

### ChatGPT

Settings → Apps → add connector URL `https://cotlet.dev/mcp/v1`, then sign in with Cotlet.dev. No API key needed.

### Cursor

Copy `.cursor/mcp.json` from this repo into your project:

```json
{
  "mcpServers": {
    "cotlet": {
      "url": "https://cotlet.dev/mcp/v1",
      "headers": {
        "Authorization": "Bearer ${COTLET_API_KEY}"
      }
    }
  }
}
```

## Command line

Python 3.10+, nothing else to install. From PyPI:

```bash
pip install wanderlog-mcp        # or run it once: uvx wanderlog-mcp connect
wanderlog-mcp connect
```

Or straight from this repo:

```bash
export COTLET_API_KEY="your-key"
python3 wanderlog_agent.py connect   # ready config for Claude Code, Cursor, ChatGPT
python3 wanderlog_agent.py status    # is Wanderlog ready in your Cotlet.dev account
python3 wanderlog_agent.py guide     # Wanderlog screens and sign-in link
python3 wanderlog_agent.py read      # open Wanderlog, read the page, close the browser
python3 wanderlog_agent.py tools     # list Cotlet.dev tools
```

## Questions from Wanderlog users

**Does Wanderlog have an API?**

Wanderlog has no public, supported API. Cotlet.dev works in your own Wanderlog account through the Cloud Browser, so your AI agent can read and edit trips without one.

**How do I connect Wanderlog to ChatGPT?**

Add Cotlet.dev as an app in ChatGPT (Settings → Apps, connector URL `https://cotlet.dev/mcp/v1`), sign in to Wanderlog once in your Cotlet.dev Cloud Browser, and ask ChatGPT in plain words. No code and no Wanderlog API key.

**Is there a way to use Claude with Wanderlog?**

Yes. In Claude Code run the one-line `claude mcp add` command above; in the Claude app add `https://cotlet.dev/mcp/v1` as a custom connector. Claude then works in your own Wanderlog account.

**Is there a Wanderlog MCP server?**

Wanderlog has no official MCP server. Cotlet.dev is a hosted MCP server that works in Wanderlog for you, 24/7, with Claude, ChatGPT, Cursor, Codex, n8n, Make and Zapier.

## Also works with

- [All apps connected through Cotlet.dev](https://github.com/cotlet-connect)

---

More: https://cotlet.dev/integrations/wanderlog-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=wanderlog

Start free: https://cotlet.dev/signup?app=wanderlog&utm_source=github&utm_medium=readme&utm_campaign=wanderlog
