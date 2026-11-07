"""Builds the ellmos marketplace from catalog.json.

- Skill plugins (kind "skills") are generated from a local clone of ellmos-ai/skills: the English SKILL.en.md becomes
  SKILL.md, the frontmatter is reduced to the Agent Skills fields (name, description, license, compatibility,
  metadata), banners and other language variants are left out. Nothing in plugins/ is edited by hand.
- External plugins (kind "external") are only listed with their source.
- .claude-plugin/marketplace.json is written from the same catalog.

Usage: python tools/build.py [--skills-repo PATH]   (default: $SKILLS_REPO or ../skills next to this repo)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKIP_NAMES = re.compile(r"^(banner\.(png|svg|jpg|webp)|SKILL\.md|SKILL\.[a-z-]+\.md|README_[a-z-]+\.md)$", re.I)
BANNER_LINE = re.compile(r"^\s*<img [^>]*banner[^>]*>\s*$", re.I)
COMPAT_LABELS = {"claude_code": "Claude Code", "claude_directory": "Claude directory (claude.ai, Cowork)",
                 "codex": "Codex", "gemini_antigravity": "Gemini / Antigravity", "kimi": "Kimi",
                 "bach": "BACH", "ocean": "Ocean"}
PAGE = "https://ellmos-ai.github.io/plugins.html"


def directory_fields(name: str, out: Path) -> dict:
    """Claude plugin directory fields; the icon is copied from assets/icons/<name>.png when present."""
    fields = {"documentationUrl": f"https://github.com/ellmos-ai/ellmos-plugins/tree/main/plugins/{name}",
              "supportUrl": f"{PAGE}#support", "privacyPolicyUrl": f"{PAGE}#privacy"}
    icon = ROOT / "assets" / "icons" / f"{name}.png"
    if icon.is_file():
        (out / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(icon, out / "assets" / "icon.png")
        fields = {"icon": "./assets/icon.png", **fields}
    return fields


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text.replace("\r\n", "\n"), re.S)
    if not match:
        raise ValueError("no frontmatter")
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def convert_skill(src: Path, dst: Path, name: str, compat_note: str, source_ref: str,
                  exclude: tuple[str, ...] = ()) -> None:
    main = src / "SKILL.en.md" if (src / "SKILL.en.md").exists() else src / "SKILL.md"
    meta, body = split_frontmatter(main.read_text(encoding="utf-8"))
    description = " ".join(str(meta.get("description", "")).split())
    if not description or len(description) > 1024:
        raise ValueError(f"{src}: description missing or longer than 1024 characters ({len(description)})")
    metadata = {"ellmos-source": source_ref, "ellmos-version": str(meta.get("version", ""))}
    for key in ("category", "anthropic_compatible", "bach_compatible", "standalone"):
        if key in meta:
            metadata[f"ellmos-{key.replace('_', '-')}"] = str(meta[key]).lower()
    if meta.get("dependencies"):
        metadata["ellmos-dependencies"] = json.dumps(meta["dependencies"], ensure_ascii=False)
    front = {"name": name, "description": description, "license": "MIT",
             "compatibility": compat_note[:500], "metadata": metadata}
    body = "\n".join(line for line in body.split("\n") if not BANNER_LINE.match(line)).lstrip("\n")
    if dst.exists():
        shutil.rmtree(dst)
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        if (item.is_dir() or SKIP_NAMES.match(item.name) or "__pycache__" in rel.parts or "node_modules" in rel.parts
                or rel.parts[0] in exclude):
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
    write(dst / "SKILL.md", "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000)
          + "---\n\n" + body)


def compat_section(entry: dict) -> str:
    rows = "\n".join(f"| {COMPAT_LABELS[k]} | {v} |" for k, v in entry.get("compatibility", {}).items())
    return f"## Compatibility\n\n| Platform | Status |\n|---|---|\n{rows}\n\n{entry.get('compatibility_note', '')}\n"


def build_skill_plugin(entry: dict, skills_repo: Path, commit: str) -> None:
    out = ROOT / "plugins" / entry["name"]
    skills_out = out / "skills"
    if skills_out.exists():
        shutil.rmtree(skills_out)
    names = []
    for skill in entry["skills"]:
        src = skills_repo / skill["src"]
        name = skill.get("name") or src.name
        convert_skill(src, skills_out / name, name, entry["compatibility_note"],
                      f"ellmos-ai/skills@{commit}:{skill['src']}", tuple(skill.get("exclude", ())))
        names.append(name)
    manifest = {"name": entry["name"], "description": entry["description"], "version": entry["version"],
                "author": {"name": "ellmos-ai"}, "license": "MIT",
                "homepage": "https://github.com/ellmos-ai/ellmos-plugins",
                "repository": "https://github.com/ellmos-ai/ellmos-plugins", "keywords": entry["keywords"],
                **directory_fields(entry["name"], out)}
    write(out / ".claude-plugin" / "plugin.json", json.dumps(manifest, indent=2) + "\n")
    skill_list = "\n".join(f"- `{n}`" for n in names)
    examples = "".join(f"{i}. {text}\n" for i, text in enumerate(entry.get("examples", []), 1))
    write(out / "README.md", f"""# {entry['name']}

{entry['description']}

This plugin bundles skills that are maintained in [ellmos-ai/skills](https://github.com/ellmos-ai/skills) and
generated into this folder by `tools/build.py` (source commit `{commit}`). Edit the skills there, not here.

## Skills

{skill_list}

## Examples

{examples}
## Install

```
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install {entry['name']}@ellmos
```

## Data flow

The plugin consists of instructions (skills) only and runs no hooks or servers. A skill may tell Claude to run a
command it describes; nothing is sent anywhere by the plugin itself. Privacy and support: {PAGE}.

{compat_section(entry)}
## License

MIT
""")
    shutil.copy2(ROOT / "LICENSE", out / "LICENSE")
    write(out / "SOURCE.json", json.dumps({"skills_repo": "ellmos-ai/skills", "commit": commit,
                                           "skills": entry["skills"]}, indent=2) + "\n")
    if not str(entry.get("compatibility", {}).get("claude_directory", "")).startswith("not submitted"):
        check_directory_types(out)


# What the Claude directory accepts from organizations that are not Verified (refusal of 07.11.2026):
# Markdown, text, JSON, YAML and these images; LICENSE as license text; nothing that starts with #!.
DIRECTORY_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}


def check_directory_types(out: Path) -> None:
    """Fail the build when a plugin meant for the Claude directory contains a file the directory refuses."""
    bad = [p.relative_to(out).as_posix() for p in sorted(out.rglob("*")) if p.is_file()
           and ((p.suffix.lower() not in DIRECTORY_SUFFIXES and p.name != "LICENSE")
                or p.read_bytes()[:2] == b"#!")]
    if bad:
        raise SystemExit(f"{out.name}: files the Claude directory refuses: {', '.join(bad)}. Exclude them in "
                         "catalog.json (skill 'exclude') or mark the plugin 'not submitted'.")


def build_mcp_plugin(entry: dict) -> None:
    """MCP plugin: server started from its pinned upstream source; skills/commands authored in authored/<name>/."""
    out = ROOT / "plugins" / entry["name"]
    if out.exists():
        shutil.rmtree(out)
    authored = ROOT / "authored" / entry["name"]
    if authored.exists():
        shutil.copytree(authored, out)
    manifest = {"name": entry["name"], "description": entry["description"], "version": entry["version"],
                "author": {"name": "ellmos-ai"}, "license": "MIT", "homepage": entry["homepage"],
                "repository": entry["homepage"], "keywords": entry["keywords"], "userConfig": entry["userConfig"]}
    write(out / ".claude-plugin" / "plugin.json", json.dumps(manifest, indent=2) + "\n")
    write(out / ".mcp.json", json.dumps({"mcpServers": entry["mcpServers"]}, indent=2) + "\n")
    write(out / "README.md", f"""# {entry['name']}

{entry['description']}

{entry['readme']}

## Install

```
/plugin marketplace add ellmos-ai/ellmos-plugins
/plugin install {entry['name']}@ellmos
```

## Data flow

{entry['data_flow']}

{compat_section(entry)}
## License

MIT (plugin files). The server is [{entry['homepage'].split('github.com/')[-1]}]({entry['homepage']}), MIT.
""")
    shutil.copy2(ROOT / "LICENSE", out / "LICENSE")
    write(out / "SOURCE.json", json.dumps({"server": entry["mcpServers"], "authored": f"authored/{entry['name']}"},
                                          indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    default = os.environ.get("SKILLS_REPO") or str(ROOT.parent / "skills")
    parser.add_argument("--skills-repo", default=default)
    args = parser.parse_args()
    skills_repo = Path(args.skills_repo).resolve()
    commit = subprocess.run(["git", "-C", str(skills_repo), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    plugins = []
    for entry in catalog["plugins"]:
        if entry["kind"] == "skills":
            build_skill_plugin(entry, skills_repo, commit)
            source = f"./plugins/{entry['name']}"
        elif entry["kind"] == "mcp":
            build_mcp_plugin(entry)
            source = f"./plugins/{entry['name']}"
        else:
            source = entry["source"]
        plugins.append({"name": entry["name"], "source": source, "description": entry["description"]})
    market = dict(catalog["marketplace"])
    market["plugins"] = plugins
    write(ROOT / ".claude-plugin" / "marketplace.json", json.dumps(market, indent=2) + "\n")
    print(f"built {len(plugins)} plugin entries from skills commit {commit}")


if __name__ == "__main__":
    main()
