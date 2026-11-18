# Sicherheitsrichtlinie / Security Policy

## Deutsch

### Sicherheitslücken melden

Wenn du eine Sicherheitslücke findest, melde sie bitte verantwortungsvoll:

1. **Kein öffentliches Issue eröffnen**
2. **GitHub Private Vulnerability Reporting verwenden**
3. Beschreibung, Reproduktionsschritte und potenzielle Auswirkungen angeben

### So meldest du ein Problem

1. Öffne im Repository: `Security` → `Advisories` → `New` (oder über das Issue-Template-Kontaktmenü)
2. Trage Titel, Beschreibung, Schweregrad und betroffene Plugins bzw. Versionen ein
3. Reiche die Meldung privat ein

Falls Private Vulnerability Reporting im Repository nicht verfügbar sein sollte,
kontaktiere die Maintainer direkt über GitHub und veröffentliche keine
Exploit-Details in einem öffentlichen Issue.

### Geltungsbereich & Pin-Governance

Dieses Repository ist ein Plugin-Marktplatz und enthält sowohl generierte
Skill-Plugins als auch Verweise auf externe sicherheitskritische Plugins:

- **Pin-Governance (`ellmos-lock-master`):** Sicherheitskritische Plugins, die
  Dateizugriffe oder Git-Befehle abfangen, müssen auf einem annotierten Tag (`ref`)
  und dem exakten Commit-SHA (`sha`) gepinnt sein. Pin-Updates erfordern den
  5-stufigen Prüfprozess aus `README.md` / `README_de.md`.
- **Claude-Directory-Dateitypprüfung:** `tools/build.py` prüft vor dem Build,
  dass für das Claude Directory vorgesehene Plugins keine ausführbaren Skripte
  oder unzulässigen Dateitypen enthalten.
- **Keine Secrets oder lokalen Systemdaten:** Keine API-Keys, Tokens oder
  hostspezifischen Pfade committen.

### Reaktionszeit

Wir bemühen uns um eine erste Rückmeldung innerhalb von 48 Stunden. Kritische
Probleme (insbesondere Hook-Bypasses oder unsichere Pin-Änderungen) werden
priorisiert. Bitte gib ausreichend Zeit zur Behebung vor einer Veröffentlichung.

---

## English

### Reporting a Vulnerability

If you find a security vulnerability, please report it responsibly:

1. **Do not open a public issue**
2. **Use GitHub Private Vulnerability Reporting**
3. Include a description, reproduction steps, and potential impact

### How to Report

1. Open: `Security` → `Advisories` → `New` (or use the issue chooser security link)
2. Fill in the title, description, severity, and affected plugins or versions
3. Submit the report privately

If private vulnerability reporting is unavailable, contact the maintainers
directly via GitHub and do not publish exploit details in a public issue.

### Scope & Pin Governance

This repository is a plugin marketplace containing generated skill plugins as
well as references to external security-critical plugins:

- **Pin Governance (`ellmos-lock-master`):** Security-critical plugins that
  intercept file edits or git commands must remain pinned to both an annotated
  tag (`ref`) and the exact commit SHA (`sha`). Pin bumps require the 5-step
  gate documented in `README.md`.
- **Claude directory file-type enforcement:** `tools/build.py` blocks unsupported
  file types or `#!` scripts in plugins submitted to the Claude directory.
- **No secrets or host paths:** Do not commit API keys, tokens, or local host paths.

### Response Time

We aim to acknowledge reports within 48 hours. Critical issues (especially hook
bypasses or unsafe pin changes) are prioritized. Please allow reasonable time
for remediation before public disclosure.
