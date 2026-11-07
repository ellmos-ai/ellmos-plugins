---
type: regex
pattern: '- 1'
match: not_contains
target:
  source: file
  path: stats.py
---

The faulty "- 1" branch is gone.
