---
name: dremio
description: "dremio tools: ping and more."
version: 0.1.0
author: Your Name
license: MIT
platforms: [macos]
triggers:
  - "dremio"
  - "dremio"
---

# dremio Plugin

Provides tools for interacting with dremio.

## Setup

```bash
./setup.sh install
```

## Available Tools

### `dremio_ping`
Test connectivity and authentication.

## Credentials

| Key | Description |
|-----|-------------|
| `api_key` | API key for dremio |

## Common Patterns

```python
# Test connectivity
dremio_ping()
```

## Pitfalls

- **Credentials missing** — run `python setup.py credentials configure` to store them.
- **Plugin not appearing** — verify `dremio` in `plugins.enabled` in config.yaml; check symlink; restart Hermes.

## Notes

TODO: Add usage notes.
