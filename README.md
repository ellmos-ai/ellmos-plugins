# ellmos-plugins

The **ellmos** Claude Code plugin marketplace: plugins from the ellmos ecosystem for mixed agent teams, workflow
gates and reusable skills.

```
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install <plugin>@ellmos
```

| Plugin | What it does | Where it lives |
|---|---|---|
| `ellmos-lock-master` | File-based locks for mixed agent teams; hooks block edits and pushes a foreign lock covers | [ellmos-ai/lock-master](https://github.com/ellmos-ai/lock-master) |
| `workflowhooker` | Closing gate with one rework round, drift and scope warnings | [ellmos-ai/workflowhooker](https://github.com/ellmos-ai/workflowhooker) |
| `ellmos-dev-quality` | Bug sweeps, bug-fix protocol, zipper merges, pre-publication checks, renames, dev cycle | `plugins/ellmos-dev-quality` (generated) |
| `ellmos-mermaid-lint` | Mermaid blocks checked with the real parser and confirmed on the GitHub page (installs npm packages, so marketplace only) | `plugins/ellmos-mermaid-lint` (generated) |
| `ellmos-decision-kit` | Decide, decision briefings, decision shots, dependency paths, one-piece drafts | `plugins/ellmos-decision-kit` (generated) |

## How this repository is built

- `catalog.json` is the single source: every plugin, its description, keywords and compatibility.
- `tools/build.py` generates the skill plugins from [ellmos-ai/skills](https://github.com/ellmos-ai/skills)
  (English `SKILL.en.md` → `SKILL.md`, frontmatter reduced to the Agent Skills fields, banners left out) and writes
  `.claude-plugin/marketplace.json`. Plugins with their own code stay in their own repository and are only listed
  here. Do not edit `plugins/` by hand; change the skills repository or the catalog and run
  `python tools/build.py --skills-repo <path>`.
- Each generated plugin records its source commit in `SOURCE.json`.
- A plugin submitted to the Claude directory may only hold Markdown, text, JSON, YAML, images and its LICENSE
  (rule for organizations that are not Verified). `tools/build.py` stops when such a plugin contains anything else;
  a skill entry in `catalog.json` can leave folders out with `"exclude": ["scripts"]`.
- Eval suites live in `evals/<plugin>/`, not inside the plugin, because their scaffold scripts are shell files. To run
  them, copy the suite in, run, and remove the copy (`plugins/*/evals/` is ignored by git):
  `cp -r evals/ellmos-dev-quality plugins/ellmos-dev-quality/evals && claude plugin eval plugins/ellmos-dev-quality --scaffold; rm -r plugins/ellmos-dev-quality/evals`.

## Compatibility

Every plugin README carries a compatibility table (Claude Code, Claude directory, Codex, Gemini/Antigravity, Kimi,
BACH, Ocean) generated from `catalog.json`.

## License

MIT
