# mwb-api

## Mac Dependancy Installation

```bash
    brew install uv
    brew isntall node
```

## Run development server

```bash
    uv run mcp dev server.py
```

## Install for Claude Desktop

```bash
    uv run mcp install server.py
```

## Fix claude_desktop_config.json

Edit the file located at:

```bash
    /Users/username/Library/Application Support/Claude/claude_desktop_config.json
```

Replace:

`"mcp[cli]",`

With:

`"mcp[cli],requests",`

See example claude_desktop_config.json in this directory.