---
name: ellmos-plugins
description: "Use when installing, validating, or building plugins from the ellmos Claude Code plugin marketplace (ellmos-ai/ellmos-plugins), including ellmos-lock-master, workflowhooker, ellmos-dev-quality, ellmos-mermaid-lint, and ellmos-decision-kit."
---

# ellmos-plugins

Product skill for working with the **ellmos** Claude Code plugin marketplace (`ellmos-ai/ellmos-plugins`).

## Marketplace Plugins

1. `ellmos-lock-master` (`external`, `ellmos-ai/lock-master`, pinned `ref: v1.9.0`, `sha: d11333eaba683a84491d29018b31ef7cfe966ed9`) — File-based locks (`LOCK*.txt`) for mixed agent teams; hooks block edits and pushes covered by a foreign lock.
2. `workflowhooker` (`external`, `ellmos-ai/workflowhooker`) — Closing workflow gate with rework round, drift, and scope warnings.
3. `ellmos-dev-quality` (`skills`, `v0.3.1`, `./plugins/ellmos-dev-quality`) — `bugsweep`, `bugfix-protocol`, `zipper-merge`, `repo-publish-check`, `migrate-rename`, `dev-cycle`.
4. `ellmos-mermaid-lint` (`skills`, `v0.1.0`, `./plugins/ellmos-mermaid-lint`) — `mermaid-lint` (marketplace only, installs npm packages at runtime).
5. `ellmos-decision-kit` (`skills`, `v0.2.0`, `./plugins/ellmos-decision-kit`) — `decide`, `decision-briefing`, `decision-shot`, `decision-path`, `decision-draw`.

## Usage (Claude Code CLI)

```text
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install <plugin>@ellmos
```

## Build & Validation Workflow (Contributors)

- Single source of truth: `catalog.json` (never edit `plugins/` manually).
- Regenerate skill plugins and `.claude-plugin/marketplace.json`:
  `python tools/build.py --skills-repo <path-to-ellmos-ai-skills>`
- Validate marketplace manifest:
  `claude plugin validate .`
- Run contract & build tests:
  `pytest -ra -v`
- Run linter:
  `ruff check .`

## Security Pin Governance

Security-critical plugins such as `ellmos-lock-master` are pinned by both annotated tag (`ref`) and commit SHA (`sha`) in `catalog.json` and `.claude-plugin/marketplace.json`. Any pin update must follow the 5-step process documented in `README.md`.
