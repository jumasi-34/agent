---
id: skill.understand.shell
title: "[Skill] Shell"
type: reference
status: active

summary: >
  Shell 참조 및 가이드 명세서.

parent: "[skills/understand/SKILL.md](../SKILL.md)"

updated: 2026-06-28
---

# Shell Language Prompt Snippet

* **Parent (상위 스킬)**: [skills/understand/SKILL.md](../SKILL.md)

---


## Key Concepts

- **Shebang Line**: `#!/bin/bash` or `#!/usr/bin/env bash` specifying the interpreter
- **Variables**: `VAR=value` assignment, `$VAR` or `${VAR}` expansion, no spaces around `=`
- **Functions**: `function name()` or `name()` for reusable command groups
- **Conditionals**: `if [[ condition ]]; then ... fi` with `[[ ]]` for extended tests
- **Loops**: `for item in list`, `while condition`, `until condition` iteration patterns
- **Pipes and Redirection**: `|` for chaining commands, `>` / `>>` / `2>&1` for output redirection
- **Exit Codes**: `$?` captures last command status; `set -e` exits on any failure
- **Strict Mode**: `set -euo pipefail` for robust error handling (exit on error, undefined vars, pipe failures)
- **Command Substitution**: `$(command)` captures command output as a string
- **Here Documents**: `<<EOF ... EOF` for multi-line string input to commands

## Notable File Patterns

- `*.sh` / `*.bash` — Shell script files
- `scripts/*.sh` — Project automation scripts (build, deploy, setup)
- `entrypoint.sh` — Docker container entry point script
- `install.sh` / `setup.sh` — Environment setup scripts
- `.bashrc` / `.bash_profile` / `.zshrc` — Shell configuration files

## Edge Patterns

- Shell scripts `triggers` other scripts or build processes they invoke
- Entry point scripts `deploys` the application they start
- Setup scripts `configures` the development environment
- Build scripts `depends_on` the source files they compile or package

## Summary Style

> "Build automation script compiling TypeScript, running tests, and packaging the release artifact."
> "Docker entry point script handling signal forwarding and graceful shutdown."
> "Environment setup script installing dependencies and configuring development tools."
