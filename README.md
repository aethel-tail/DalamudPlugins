# Dalamud 插件仓库

[English](README.en.md)

自定义 [FFXIVQuickLauncher](https://github.com/goaaats/FFXIVQuickLauncher) 插件仓库。

## 安装

在游戏中打开 `/xlsettings` → "实验性" 标签 → 将以下 URL 粘贴到"自定义插件仓库"输入框 → 点击 + → 点击保存。

```
https://raw.githubusercontent.com/aethel-tail/DalamudPlugins/master/pluginmaster.json
```

插件将出现在插件安装器（`/xlplugins`）中。

## 插件列表

| 插件 | 描述 |
|------|------|
| [Graphics Upscaler Toggle](https://github.com/aethel-tail/GraphicsUpscalerToggle) | 登录时自动切换图形上采样，重新启用 DLSS |

## 添加插件

1. 在 `plugins/<PluginName>/` 下创建插件清单 JSON 文件
2. 运行 `python generate_pluginmaster.py` 重新生成 `pluginmaster.json`
3. 提交并推送到 `master` 分支（GitHub Actions 也会自动生成）

## 许可

各插件使用各自的许可证。
