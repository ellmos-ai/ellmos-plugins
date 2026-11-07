# ellmos-dev-quality

Skills for systematic bug work, section-by-section merges, safe renames and pre-publication checks.

This plugin bundles skills that are maintained in [ellmos-ai/skills](https://github.com/ellmos-ai/skills) and
generated into this folder by `tools/build.py` (source commit `1a4e610`). Edit the skills there, not here.

## Skills

- `bugsweep`
- `bugfix-protocol`
- `zipper-merge`
- `repo-publish-check`
- `migrate-rename`
- `dev-cycle`

## Examples

1. "Run a systematic bug sweep over this repository and list the findings by area." (bugsweep)
2. "main and my feature branch both changed the parser; merge them without dropping either side's work." (zipper-merge)
3. "Customers are charged too much when a coupon is applied - find the cause and fix it." (bugfix-protocol)

## Install

```
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install ellmos-dev-quality@ellmos
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

Agent Skills format, usable by any Agent Skills client. No package installs.

## License

MIT
