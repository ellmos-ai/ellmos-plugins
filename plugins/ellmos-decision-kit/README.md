# ellmos-decision-kit

Skills to prepare, compare, sequence and sign off decisions: options with a clear recommendation, dependency maps and one-piece drafts.

This plugin bundles skills that are maintained in [ellmos-ai/skills](https://github.com/ellmos-ai/skills) and
generated into this folder by `tools/build.py` (source commit `1a4e610`). Edit the skills there, not here.

## Skills

- `decide`
- `decision-briefing`
- `decision-shot`
- `decision-path`
- `decision-draw`

## Examples

1. "Our clinic app needs authentication: build our own, Auth0 or self-hosted Keycloak? GDPR and EU hosting, about 300 EUR a month, little ops capacity. Decide." (decide)
2. "We have collected six open decisions for the release - list them with options and a clear recommendation each." (decision-briefing)
3. "Show how these pending decisions depend on each other and which one to settle first." (decision-path)

## Install

```
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install ellmos-decision-kit@ellmos
```

## Data flow

The plugin consists of instructions (skills) only and runs no hooks or servers. A skill may tell Claude to run a
command it describes; nothing is sent anywhere by the plugin itself. Privacy and support: https://ellmos-ai.github.io/plugins.html.

## Compatibility

| Platform | Status |
|---|---|
| Claude Code | yes |
| Claude directory (claude.ai, Cowork) | untested |
| Codex | yes |
| Gemini / Antigravity | untested |
| Kimi | untested |
| BACH | yes |
| Ocean | yes |

Agent Skills format, text only, no scripts or network access.

## License

MIT
