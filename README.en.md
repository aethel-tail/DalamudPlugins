# Dalamud Plugin Repository

[中文](README.md)

A custom [FFXIVQuickLauncher](https://github.com/goaaats/FFXIVQuickLauncher) plugin repository.

## Installation

Open `/xlsettings` in-game → "Experimental" tab → paste the following URL into the Custom Plugin Repositories box → click + → click Save.

```
https://raw.githubusercontent.com/aethel-tail/DalamudPlugins/master/pluginmaster.json
```

Plugins will then appear in the Plugin Installer (`/xlplugins`).

## Plugins

| Plugin | Description |
|--------|-------------|
| [Graphics Upscaler Toggle](https://github.com/aethel-tail/GraphicsUpscalerToggle) | Auto-toggle graphics upscaling to re-engage DLSS on login |

## Adding a Plugin

1. Create a plugin manifest JSON under `plugins/<PluginName>/`
2. Run `python generate_pluginmaster.py` to regenerate `pluginmaster.json`
3. Commit and push to `master` branch (GitHub Actions also regenerates automatically)

## License

Plugins are licensed individually.
