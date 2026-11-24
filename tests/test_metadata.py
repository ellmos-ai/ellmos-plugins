from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

ROOT = Path(__file__).resolve().parent.parent


def _read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_pep621_and_pep639_metadata_no_duplicate_license_classifier() -> None:
    pyproject = tomllib.loads(_read_text("pyproject.toml"))
    project = pyproject["project"]

    assert project["name"] == "ellmos-plugins"
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]
    assert project["requires-python"] == ">=3.10"

    classifiers = project.get("classifiers", [])
    assert not any(c.startswith("License :: OSI Approved ::") for c in classifiers)
    for py_ver in ("3.10", "3.11", "3.12", "3.13"):
        assert f"Programming Language :: Python :: {py_ver}" in classifiers

    urls = project.get("urls", {})
    for key in ("Homepage", "Repository", "Issues", "Changelog", "Contributing", "Code of Conduct", "Security"):
        assert key in urls and urls[key].startswith("https://")


def test_pytest_config_has_no_relative_basetemp() -> None:
    pyproject = tomllib.loads(_read_text("pyproject.toml"))
    pytest_opts = pyproject["tool"]["pytest"]["ini_options"]
    addopts = pytest_opts.get("addopts", "")

    assert "--basetemp" not in addopts
    assert "--strict-markers" in addopts
    assert pytest_opts.get("xfail_strict") is True
    assert ".pytest_temp" in pytest_opts.get("norecursedirs", [])


def test_ci_workflow_matrix_and_permissions() -> None:
    ci = yaml.safe_load(_read_text(".github/workflows/ci.yml"))
    assert "workflow_dispatch" in ci[True]
    assert ci["permissions"] == {"contents": "read"}

    test_job = ci["jobs"]["test"]
    assert test_job["timeout-minutes"] <= 15
    matrix = test_job["strategy"]["matrix"]
    assert set(matrix["os"]) == {"ubuntu-latest", "windows-latest", "macos-latest"}
    assert set(matrix["python-version"]) == {"3.10", "3.11", "3.12", "3.13"}

    step_runs = "\n".join(str(step.get("run", "")) for step in test_job["steps"])
    for expected in ("git diff --check", "ruff check .", "pytest -ra -v", "pip check"):
        assert expected in step_runs


def test_dependabot_and_issue_templates_present() -> None:
    dep = yaml.safe_load(_read_text(".github/dependabot.yml"))
    ecosystems = {u["package-ecosystem"] for u in dep["updates"]}
    assert {"pip", "github-actions"} <= ecosystems

    cfg = yaml.safe_load(_read_text(".github/ISSUE_TEMPLATE/config.yml"))
    assert cfg["blank_issues_enabled"] is False
    assert (ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").is_file()
    assert (ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").is_file()


def test_gitignore_hardening_and_evals_exception() -> None:
    gi = _read_text(".gitignore")
    for pattern in (
        "__pycache__/",
        ".pytest_temp/",
        "*MARKETING-LOG.txt",
        "LOCK*.txt",
        "LOCK-CACHE.*",
        "*-ASUS-GEI*",
        "*-WORKSTATION*",
        "*-IDEAPAD*",
        ".claude/",
        ".codex/",
        ".gemini/",
        "!plugins/ellmos-decision-kit/evals/",
    ):
        assert pattern in gi


def test_governance_and_p022_files_present() -> None:
    assert (ROOT / "LICENSE").is_file()

    coc = _read_text("CODE_OF_CONDUCT.md")
    assert "## Deutsch" in coc and "## English" in coc

    sec = _read_text("SECURITY.md")
    assert "## Deutsch" in sec and "## English" in sec
    assert "ellmos-lock-master" in sec

    contrib = _read_text("CONTRIBUTING.md")
    assert "## Deutsch" in contrib and "## English" in contrib
    assert "tools/build.py" in contrib

    changelog = _read_text("CHANGELOG.md")
    assert "## [Unreleased]" in changelog

    skill = _read_text("SKILL.md")
    assert skill.startswith("---") and "name: ellmos-plugins" in skill

    llms = _read_text("llms.txt")
    assert "catalog.json" in llms and "tools/build.py" in llms
    assert "llms.txt" in _read_text("llm.txt")


def test_readme_bilingual_parity_and_banner_preserved() -> None:
    en = _read_text("README.md")
    de = _read_text("README_de.md")

    for content in (en, de):
        assert '<img src="assets/banner.svg"' in content
        for plugin in (
            "ellmos-lock-master",
            "workflowhooker",
            "ellmos-dev-quality",
            "ellmos-mermaid-lint",
            "ellmos-decision-kit",
        ):
            assert plugin in content
        assert "SKILL.md" in content
        assert "llms.txt" in content
        assert not re.search(r"C:\\\\?Users\\\\", content)

    assert "README_de.md" in en
    assert "README.md" in de
    assert "### Install with your LLM" in en or "## 6. Install with Your LLM" in en
    assert "### Mit deinem LLM installieren" in de or "## 6. Mit deinem LLM installieren" in de


def test_terminal_workflow_svg_asset_valid_and_embedded() -> None:
    svg_path = ROOT / "assets" / "terminal-workflow.svg"
    assert svg_path.is_file()
    tree = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    assert tree.tag.endswith("svg")

    for doc in ("README.md", "README_de.md"):
        content = _read_text(doc)
        assert '<img src="assets/banner.svg"' in content
        assert '<img src="assets/terminal-workflow.svg"' in content


def test_readme_mermaid_architecture_and_sequence_diagrams() -> None:
    for doc in ("README.md", "README_de.md"):
        content = _read_text(doc)
        assert "```mermaid\nflowchart LR" in content
        assert "```mermaid\nsequenceDiagram" in content
        seq_blocks = re.findall(r"```mermaid\n(sequenceDiagram.*?)```", content, flags=re.S)
        assert seq_blocks
        for block in seq_blocks:
            assert ";" not in block


def test_readme_ten_section_navigation_and_badges_parity() -> None:
    for doc in ("README.md", "README_de.md"):
        content = _read_text(doc)
        for idx in range(1, 11):
            anchor = f"sec-{idx:02d}"
            assert f'<a id="{anchor}"></a>' in content
            assert f"(#{anchor})" in content
        assert "2026--11--24" in content
        assert "https://ellmos-ai.github.io/plugins.html" in content


def test_readme_public_ai_attribution_geiger() -> None:
    en = _read_text("README.md")
    de = _read_text("README_de.md")
    assert "Concept & Sign-off: Geiger" in en
    assert "Idee & Abnahme: Geiger" in de
    assert "Sign-off: LG" not in en
    assert "Abnahme: LG" not in de


def test_p022_llms_txt_quick_install_and_last_checked() -> None:
    llms = _read_text("llms.txt")
    assert "Last-checked: 2026-11-24" in llms
    assert "## Quick Install & Verification" in llms
    for required in ("Prerequisites", "Installation", "Verification", "Minimal Example", "claude plugin validate ."):
        assert required in llms


def test_pyproject_version_frozen_and_discoverability_urls() -> None:
    pyproject = tomllib.loads(_read_text("pyproject.toml"))
    project = pyproject["project"]
    assert project["version"] == "0.1.0"

    urls = project["urls"]
    for key in ("Documentation", "Product Skill", "LLM Entrypoint"):
        assert key in urls and urls[key].startswith("https://")


def test_changelog_unreleased_path_b_entry() -> None:
    changelog = _read_text("CHANGELOG.md")
    assert "## [Unreleased]" in changelog
    for token in ("2026-11-24", "assets/terminal-workflow.svg", "sequenceDiagram", "sec-01"):
        assert token in changelog
