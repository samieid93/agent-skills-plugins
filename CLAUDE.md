# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

This project uses Nix flakes for reproducible development environments, managed with `direnv`.

```bash
# Enter the dev shell (automatically via direnv, or manually)
nix develop

# Reload the direnv environment after flake changes
nix-direnv-reload   # or: direnv reload
```

Environment variables are loaded from `.env` (via `.envrc`; `.env` is gitignored).

## Project Structure

This is an early-stage repository intended for agent skills/plugins. The `flake.nix` defines the dev shell — add required packages there under `devShells.default.packages`.
