# Changelog

All notable changes to this repository will be documented in this file.

## [Unreleased]

### Added
- Multi-OS CI matrix workflow (`.github/workflows/ci.yml`) covering `ubuntu-latest`, `windows-latest`, and `macos-latest` across Python `3.10`–`3.13`.
- Weekly Dependabot configuration (`.github/dependabot.yml`) for `pip` and `github-actions`.
- Bilingual GitHub issue templates (`.github/ISSUE_TEMPLATE/config.yml`, `bug_report.md`, `feature_request.md`).
- Governance and LLM entrypoint files: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`, `SKILL.md`, `llms.txt`, `llm.txt`, and `README_de.md`.
- PEP 621/639 `pyproject.toml` configuration (build metadata, PyYAML dependency, Ruff lint config, and Pytest config without relative `--basetemp`).
- Automated contract and build-helper test suite in `tests/test_marketplace_contracts.py` and `tests/test_metadata.py`.

### Changed
- Hardened `.gitignore` against Python/Ruff/Pytest caches, multi-host sync conflict copies, lock files, agent state folders, and internal `*MARKETING-LOG.txt` logs, while un-ignoring tracked `plugins/ellmos-decision-kit/evals/` Markdown fixtures.
- Updated `README.md` with language switcher, status badges, LLM install/usage guidance, and links to governance docs (preserving the existing `assets/banner.svg` header and plugin tables).
