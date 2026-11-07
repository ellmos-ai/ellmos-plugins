# ellmos-mermaid-lint

Checks Mermaid blocks in Markdown with the real Mermaid parser and confirms on the GitHub page that they render.

This plugin bundles skills that are maintained in [ellmos-ai/skills](https://github.com/ellmos-ai/skills) and
generated into this folder by `tools/build.py` (source commit `1a4e610`). Edit the skills there, not here.

## Skills

- `mermaid-lint`

## Examples

1. "GitHub shows 'Unable to render rich display' in docs/ - find and fix the broken Mermaid diagrams." (mermaid-lint)

## Install

```
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install ellmos-mermaid-lint@ellmos
```

## Data flow

The plugin consists of instructions (skills) only and runs no hooks or servers. A skill may tell Claude to run a
command it describes; nothing is sent anywhere by the plugin itself. Privacy and support: https://ellmos-ai.github.io/plugins.html.

## Compatibility

| Platform | Status |
|---|---|
| Claude Code | yes |
| Claude directory (claude.ai, Cowork) | not submitted (installs npm packages) |
| Codex | yes |
| Gemini / Antigravity | untested |
| Kimi | untested |
| BACH | yes |
| Ocean | yes |

Agent Skills format, usable by any Agent Skills client. Needs node and git and installs its npm dependencies (mermaid, jsdom, playwright-core) when run, so it is offered in this marketplace only and not in the Claude directory.

## License

MIT
