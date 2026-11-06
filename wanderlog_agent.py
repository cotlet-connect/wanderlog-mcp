#!/usr/bin/env python3
"""Wanderlog through Cotlet.dev: small CLI over the Cotlet.dev MCP server (stdlib only)."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

START_URL = "https://wanderlog.com"
SLUG = "wanderlog"
URL = "https://cotlet.dev/mcp/v1"
GUIDE_FIELD = "app"
KEY_HELP = "Set COTLET_API_KEY. Get a key at https://cotlet.dev/app"

CONFIG = {"mcpServers": {"cotlet": {"url": URL, "headers": {"Authorization": "Bearer ${COTLET_API_KEY}"}}}}


class Client:
    def __init__(self, key):
        self.key = key
        self.session = None
        self.next_id = 0

    def _post(self, payload):
        headers = {
            "Authorization": "Bearer " + self.key,
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(URL, json.dumps(payload).encode(), headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                self.session = resp.headers.get("Mcp-Session-Id") or self.session
                return resp.read().decode(), resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode(errors="replace")[:300]))

    @staticmethod
    def _parse(body, ctype, rid):
        if "text/event-stream" in ctype:
            for line in body.splitlines():
                if line.startswith("data:"):
                    try:
                        msg = json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if msg.get("id") == rid:
                        return msg
            raise RuntimeError("No JSON-RPC answer in stream")
        return json.loads(body)

    def rpc(self, method, params=None):
        self.next_id += 1
        rid = self.next_id
        body, ctype = self._post({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}})
        msg = self._parse(body, ctype, rid)
        if "error" in msg:
            raise RuntimeError(msg["error"].get("message", str(msg["error"])))
        return msg.get("result", {})

    def start(self):
        self.rpc("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": SLUG + "-mcp", "version": "1.0.0"},
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def call(self, tool, args):
        res = self.rpc("tools/call", {"name": tool, "arguments": args})
        text = "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise RuntimeError(text or "tool error")
        return text


def connect():
    print("Claude Code:\n  claude mcp add --transport http cotlet %s --header \"Authorization: Bearer $COTLET_API_KEY\"\n" % URL)
    print("Cursor (.cursor/mcp.json):\n" + json.dumps(CONFIG, indent=2) + "\n")
    print("ChatGPT:\n  Settings -> Apps -> add connector URL %s, sign in with Cotlet.dev (no API key)." % URL)


def main():
    p = argparse.ArgumentParser(description="Wanderlog through Cotlet.dev")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("connect", "status", "guide", "tools"):
        sub.add_parser(name)
    r = sub.add_parser("read")
    r.add_argument("url", nargs="?")
    args = p.parse_args()
    if args.cmd == "connect":
        return connect()
    key = os.environ.get("COTLET_API_KEY")
    if not key:
        print(KEY_HELP)
        sys.exit(2)
    try:
        c = Client(key)
        c.start()
        if args.cmd == "tools":
            print("\n".join(t["name"] for t in c.rpc("tools/list").get("tools", [])))
        elif args.cmd == "status":
            print(c.call("cotlet_apps", {"app": SLUG}))
        elif args.cmd == "guide":
            print(c.call("cotlet_app_guide", {GUIDE_FIELD: SLUG}))
        elif args.cmd == "read":
            # Works in the user's Web browser, where they sign in to the app once.
            c.call("cotlet_browser_open", {"url": args.url or START_URL})
            try:
                print(c.call("cotlet_browser_read", {}))
            finally:
                c.call("cotlet_browser_close", {})
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
