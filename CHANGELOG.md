# Changelog

All notable changes to this repository will be documented in this file.

## [Unreleased]

### Added
- Path B discoverability & visual assets (2026-11-24):
  - Dark-mode vector workflow preview `assets/terminal-workflow.svg` illustrating Claude Code marketplace installation, `claude plugin validate .`, contract test verification, and the 5-plugin / 12-skill catalog.
  - Bilingual 10-section README architecture (`README.md` and `README_de.md`) with reciprocal navigation anchors (`sec-01`–`sec-10`), target audiences, high-intent search queries, comparison matrix, multi-platform compatibility matrix, and concise public editorial/AI attribution (`Geiger`).
  - Mermaid `flowchart LR` marketplace topology and `sequenceDiagram` 5-step security pin governance lifecycle in both `README.md` and `README_de.md`.
  - 7 new contract & metadata parity tests in `tests/test_metadata.py` (19 tests total).
- Multi-OS CI matrix workflow (`.github/workflows/ci.yml`) covering `ubuntu-latest`, `windows-latest`, and `macos-latest` across Python `3.10`–`3.13`.
- Weekly Dependabot configuration (`.github/dependabot.yml`) for `pip` and `github-actions`.
- Bilingual GitHub issue templates (`.github/ISSUE_TEMPLATE/config.yml`, `bug_report.md`, `feature_request.md`).
- Governance and LLM entrypoint files: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`, `SKILL.md`, `llms.txt`, `llm.txt`, and `README_de.md`.
- PEP 621/639 `pyproject.toml` configuration (build metadata, PyYAML dependency, Ruff lint config, and Pytest config without relative `--basetemp`).
- Automated contract and build-helper test suite in `tests/test_marketplace_contracts.py` and `tests/test_metadata.py`.

### Changed
- Updated `llms.txt` (`Last-checked: 2026-11-24`, `## Quick Install & Verification`), `SKILL.md`, and `pyproject.toml` (`Documentation`, `Product Skill`, `LLM Entrypoint` URLs and discovery keywords; package version `0.1.0` preserved).
- Hardened `.gitignore` against Python/Ruff/Pytest caches, multi-host sync conflict copies, lock files, agent state folders, and internal `*MARKETING-LOG.txt` logs, while un-ignoring tracked `plugins/ellmos-decision-kit/evals/` Markdown fixtures.
- Updated `README.md` with language switcher, status badges, LLM install/usage guidance, and links to governance docs (preserving the existing `assets/banner.svg` header and plugin tables).
