from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools import build

ROOT = Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_catalog_and_marketplace_json_parity() -> None:
    catalog = _load_json(ROOT / "catalog.json")
    marketplace = _load_json(ROOT / ".claude-plugin" / "marketplace.json")

    assert marketplace["name"] == catalog["marketplace"]["name"]
    assert marketplace["description"] == catalog["marketplace"]["description"]
    assert marketplace["owner"] == catalog["marketplace"]["owner"]

    cat_plugins = catalog["plugins"]
    mkt_plugins = marketplace["plugins"]
    assert [p["name"] for p in mkt_plugins] == [p["name"] for p in cat_plugins]

    for cat_entry, mkt_entry in zip(cat_plugins, mkt_plugins, strict=True):
        assert mkt_entry["description"] == cat_entry["description"]
        if cat_entry["kind"] in {"skills", "mcp"}:
            assert mkt_entry["source"] == f"./plugins/{cat_entry['name']}"
        else:
            assert mkt_entry["source"] == cat_entry["source"]


def test_security_pin_governance_ellmos_lock_master() -> None:
    catalog = _load_json(ROOT / "catalog.json")
    marketplace = _load_json(ROOT / ".claude-plugin" / "marketplace.json")

    cat_lock = next(p for p in catalog["plugins"] if p["name"] == "ellmos-lock-master")
    mkt_lock = next(p for p in marketplace["plugins"] if p["name"] == "ellmos-lock-master")

    for entry in (cat_lock, mkt_lock):
        src = entry["source"]
        assert src["source"] == "github"
        assert src["repo"] == "ellmos-ai/lock-master"
        assert src["ref"].startswith("v")
        assert re.fullmatch(r"[0-9a-f]{40}", src["sha"])


def test_generated_skill_plugins_integrity() -> None:
    catalog = _load_json(ROOT / "catalog.json")
    skill_entries = [p for p in catalog["plugins"] if p["kind"] == "skills"]
    assert skill_entries

    for entry in skill_entries:
        plugin_dir = ROOT / "plugins" / entry["name"]
        assert plugin_dir.is_dir(), f"missing plugin dir: {plugin_dir}"

        manifest = _load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        assert manifest["name"] == entry["name"]
        assert manifest["version"] == entry["version"]
        assert manifest["license"] == "MIT"

        assert (plugin_dir / "README.md").is_file()
        assert (plugin_dir / "LICENSE").is_file()

        source_meta = _load_json(plugin_dir / "SOURCE.json")
        assert source_meta["skills_repo"] == catalog["skills_repo"]
        assert source_meta["skills"] == entry["skills"]

        for skill in entry["skills"]:
            skill_name = skill.get("name") or Path(skill["src"]).name
            skill_md = plugin_dir / "skills" / skill_name / "SKILL.md"
            assert skill_md.is_file(), f"missing SKILL.md: {skill_md}"
            meta, _body = build.split_frontmatter(skill_md.read_text(encoding="utf-8"))
            assert meta["name"] == skill_name
            assert 1 <= len(str(meta["description"])) <= 1024
            assert meta["license"] == "MIT"


def test_claude_directory_plugins_file_types() -> None:
    catalog = _load_json(ROOT / "catalog.json")
    for entry in catalog["plugins"]:
        if entry["kind"] != "skills":
            continue
        compat_dir = str(entry.get("compatibility", {}).get("claude_directory", ""))
        if compat_dir.startswith("not submitted"):
            continue
        build.check_directory_types(ROOT / "plugins" / entry["name"])


def test_build_helpers_split_frontmatter_and_directory_types(tmp_path: Path) -> None:
    meta, body = build.split_frontmatter("---\nname: demo\ndescription: test\n---\n\n# Body\n")
    assert meta == {"name": "demo", "description": "test"}
    assert body.strip() == "# Body"

    with pytest.raises(ValueError, match="no frontmatter"):
        build.split_frontmatter("# Plain markdown without frontmatter\n")

    clean_plugin = tmp_path / "clean-plugin"
    clean_plugin.mkdir()
    (clean_plugin / "README.md").write_text("# Clean\n", encoding="utf-8")
    (clean_plugin / "LICENSE").write_text("MIT\n", encoding="utf-8")
    build.check_directory_types(clean_plugin)

    bad_plugin = tmp_path / "bad-plugin"
    bad_plugin.mkdir()
    (bad_plugin / "run.sh").write_text("#!/bin/sh\necho hi\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="files the Claude directory refuses"):
        build.check_directory_types(bad_plugin)
