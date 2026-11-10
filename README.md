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

## Run it locally (stdio)

This repo is a real MCP server. It speaks MCP over stdio, lists its Wanderlog tools without any key, and forwards every tool call to the hosted Cotlet.dev server. The hosted URL above stays the recommended way. Use this when your client only starts local servers.

```json
{"mcpServers":{"wanderlog":{"command":"uvx","args":["wanderlog-mcp"],"env":{"COTLET_API_KEY":"your-key"}}}}
```

Or with Docker:

```bash
docker build -t wanderlog-mcp .
docker run -i --rm -e COTLET_API_KEY wanderlog-mcp
```

Tools: `wanderlog_guide`, `wanderlog_status`, `wanderlog_open`, `wanderlog_read`, `wanderlog_click`, `wanderlog_type`, `wanderlog_close`. Without `COTLET_API_KEY` a tool call answers: "Set COTLET_API_KEY. Get a key at https://cotlet.dev/app".

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
python3 wanderlog_agent.py serve     # start the stdio MCP server (same as no argument)
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

## Find it on

- [Wanderlog on Cotlet.dev](https://cotlet.dev/integrations/wanderlog-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=wanderlog&utm_content=find)
- [PyPI package wanderlog-mcp](https://pypi.org/project/wanderlog-mcp/)
- [Glama](https://glama.ai/mcp/servers/cotlet-connect/wanderlog-mcp)
- [Odel](https://odel.app/modules/cotlet/wanderlog)
- [mcpbeat](https://mcpbeat.com/mcp-servers/cotlet/wanderlog/)
- [Step-by-step guide (PDF) on Internet Archive](https://archive.org/details/cotlet-connect-wanderlog-to-ai-agents-guide)

## Also works with

- [Mangomint MCP](https://github.com/cotlet-connect/mangomint-mcp)
- [SmugMug MCP](https://github.com/cotlet-connect/smugmug-mcp)
- [Garmin Connect MCP](https://github.com/cotlet-connect/garmin-mcp)
- [Housecall Pro MCP](https://github.com/cotlet-connect/housecall-pro-mcp)
- [Medium MCP](https://github.com/cotlet-connect/medium-mcp)
- [Crexi MCP](https://github.com/cotlet-connect/crexi-mcp)
- [DistroKid MCP](https://github.com/cotlet-connect/distrokid-mcp)
- [LinkedIn MCP](https://github.com/cotlet-connect/linkedin-mcp)
- [EstimateOne MCP](https://github.com/cotlet-connect/estimateone-mcp)
- [All apps connected through Cotlet.dev](https://github.com/cotlet-connect)

---

More: https://cotlet.dev/integrations/wanderlog-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=wanderlog

Start free: https://cotlet.dev/signup?app=wanderlog&utm_source=github&utm_medium=readme&utm_campaign=wanderlog
