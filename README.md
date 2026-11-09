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

## Pin Governance (Security Plugins)

Security-critical plugins that intercept file edits and git commands (such as `ellmos-lock-master`) MUST NOT float on unpinned branches or mutable heads. In `catalog.json` and `.claude-plugin/marketplace.json`, these plugins are pinned to both an explicit tag reference and the exact commit SHA:

- **Current Pin:** `ellmos-lock-master` is pinned to `ref: "v1.9.0"` (`sha: "d11333eaba683a84491d29018b31ef7cfe966ed9"`).

### Mandatory Process for Bumping a Pin

Bumping a pin for a security plugin requires a strict 5-step gate before adoption:

1. **Verify Annotated Tag:** Inspect the upstream tag object (e.g. `git cat-file -t <tag>`). The tag must be annotated and point to the exact target commit SHA.
2. **Adversarial Probe & Live Acceptance Stage A (`--plugin-dir`):** Check out the tag in an isolated directory and validate its hooks using fresh `claude -p` runs with `--plugin-dir <checkout>` against the full adversarial test matrix (e.g. foreign lock denial on push/edit across all syntax forms, own lock allowance, worker-owner subagent ID resolution, and differential comparison against the previous version). Never execute marketplace updates during Stage A.
3. **Catalog Update & Manifest Regeneration:** Update `ref` and `sha` for the plugin in `catalog.json`, run `python tools/build.py`, and run `claude plugin validate .` to verify that the generated `.claude-plugin/marketplace.json` is valid.
4. **Pull Request & Independent Review:** Submit a pull request on `ellmos-ai/ellmos-plugins`. Review must be performed by an independent model instance or operator.
5. **Live Acceptance Stage B (Live Marketplace Path):** Only after merge and user sign-off, execute the real update path (`claude plugin marketplace update ellmos` followed by `claude plugin update ellmos-lock-master@ellmos`). Verify the runtime status and cache path in a clean session.

## Compatibility

Every plugin README carries a compatibility table (Claude Code, Claude directory, Codex, Gemini/Antigravity, Kimi,
BACH, Ocean) generated from `catalog.json`.

## License

MIT
