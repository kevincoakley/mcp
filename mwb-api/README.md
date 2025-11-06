# mwb-api

A small MCP (Model Context Protocol) wrapper for the Metabolomics Workbench REST API.
This program exposes a set of MCP tools (in `server.py`) that let an LLM or MCP-capable client query the Metabolomics Workbench REST service.

## Environment variables

The server reads these environment variables (defaults shown):

- `MCP_HOST` — host for streamable HTTP transport (default `0.0.0.0`)
- `MCP_PORT` — port for streamable HTTP transport (default `8080`)
- `MCP_TRANSPORT` — transport used when running the script directly (`stdio` or `streamable-http`, default `stdio`)

## stdio vs streamable-http

By default this runs the server with the `stdio` transport (good for pairing with a local LLM client).

When using `streamable-http` the server will bind to `MCP_HOST:MCP_PORT`. Use your MCP client or reverse proxy (e.g. nginx) to forward requests from a public address if needed.

## Install for Claude Desktop

Update your Claude Desktop configuration (macOS):

`~/Library/Application Support/Claude/claude_desktop_config.json`

Replace `username` with your macOS account and follow the example `claude_desktop_config.json` in this directory.
