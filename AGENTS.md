# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Custom [FFXIVQuickLauncher](https://github.com/goaaats/FFXIVQuickLauncher) plugin repository. Hosts plugin manifests — the actual plugin code lives in separate repos. End users install via `/xlsettings` → "Experimental" → add `https://raw.githubusercontent.com/aethel-tail/DalamudPlugins/master/pluginmaster.json`.

## Repository Architecture

```
plugins/
  <PluginName>/
    <PluginName>.json    # Plugin manifest (author, version, description, download URLs, etc.)
    images/icon.png      # Plugin icon referenced by IconUrl in the manifest
pluginmaster.json         # AUTO-GENERATED — aggregated manifest served to Dalamud clients
generate_pluginmaster.py  # Python script that collects plugin/*.json → writes pluginmaster.json
.github/workflows/regenerate.yml  # CI: runs generate_pluginmaster.py on push + every 12h
```

- `generate_pluginmaster.py` walks `./plugins/`, reads each `<Name>/<Name>.json`, merges in download links (derived from `RepoUrl` + `AssemblyVersion`), download counts (from GitHub Releases API), and timestamps. Never edit `pluginmaster.json` by hand — it will be overwritten.
- CI regenerates `pluginmaster.json` on every push to master and on a 12-hour cron. Concurrency is limited to one workflow at a time.

## Adding a New Plugin

1. Create `plugins/<PluginName>/` with `<PluginName>.json` (follow existing manifest format) and `images/icon.png`
2. Run `pip install -r requirements.txt && python generate_pluginmaster.py`
3. Commit all new files + updated `pluginmaster.json`

## Manifest Format

Each `<PluginName>.json` must include: `Author`, `Name`, `InternalName`, `AssemblyVersion`, `Description`, `Punchline`, `RepoUrl`, `Tags`, `CategoryTags`, `DalamudApiLevel`, `IconUrl`, `ImageUrls`. Optional: `LoadRequiredState`, `LoadSync`, `CanUnloadAsync`, `LoadPriority`, `Changelog`, `AcceptsFeedback`.

Download links are not in the per-plugin JSON — the generator derives them from `RepoUrl`/`AssemblyVersion` using the pattern `{RepoUrl}/releases/download/v{AssemblyVersion}/latest.zip`.

The generator preserves `LastUpdate` across runs when `AssemblyVersion` hasn't changed, so repeated regeneration won't falsely bump update timestamps.

## Plugin JSON Fields in Chinese

By convention for this repo, `Name`, `Punchline`, and `Description` are written in Chinese. `Tags` includes both Chinese and English equivalents. `CategoryTags` uses English only.
