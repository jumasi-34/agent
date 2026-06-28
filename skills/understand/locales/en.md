---
id: skill.understand.en
type: reference
status: active

summary: >
  En 참조 및 가이드 명세서.

parent: "[[skills/understand/SKILL]]"

updated: 2026-06-28
---

# English Output Guidelines

* **Parent (상위 스킬)**: [[skills/understand/SKILL]]

---


This file provides language-specific guidance for generating knowledge graph content in English.

## Tag Conventions

Use lowercase, hyphenated tags in English:

| Pattern | Recommended Tags |
|---------|--------------
---
|
| Entry point file | `entry-point`, `barrel`, `exports` |
| Utility functions | `utility`, `helpers`, `common` |
| API handlers | `api-handler`, `controller`, `endpoint` |
| Data models | `data-model`, `entity`, `schema` |
| Test files | `test`, `spec`, `unit-test` |
| Configuration | `configuration`, `build-system`, `settings` |
| Infrastructure | `infrastructure`, `deployment`, `containerization` |
| Documentation | `documentation`, `guide`, `reference` |

## Summary Style

Write 1-2 sentence summaries that:
- Describe **purpose** and **role** in the project
- Use active voice ("Provides...", "Handles...", "Manages...")
- Avoid restating the filename

**Examples:**
- Good: "Provides date formatting and string sanitization helpers used across the API layer."
- Bad: "The utils file contains utility functions."

## Technical Terms

Keep these terms in English (no translation needed):
- `middleware`, `hook`, `barrel`, `entry-point`
- `ORM`, `REST API`, `CI/CD`, `CRUD`
- `singleton`, `factory`, `observer`
- `middleware`, `interceptor`, `guard`

## Layer Names

Use standard English layer names:
- `API Layer`, `Service Layer`, `Data Layer`, `UI Layer`
- `Infrastructure`, `Configuration`, `Documentation`
- `Utility Layer`, `Middleware Layer`, `Test Layer`