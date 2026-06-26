# AGENTS.md

## 项目

- **名称**：牛牛互动 interact
- **类型**：Pallas-Bot 4.0 社区插件（NoneBot 插件包，社区开发示范）
- **插件 ID**：`interact`（与安装目录 `local/plugins/interact/` 一致）
- **依赖**：运行时依赖 [Pallas-Bot](https://github.com/PallasBot/Pallas-Bot) `>=4.0`

## 目录

扁平 NoneBot 插件包（克隆到 `local/plugins/interact/` 即可加载）：

```text
interact/
├── __init__.py   # PluginMetadata + 口令/通知注册
├── config.py     # 插件配置
├── handlers.py   # 点赞、群头衔、戳一戳回图
├── notices.py    # 戳一戳通知与 /群头衔 规则
├── service.py    # 点赞调用与图片目录解析
├── README.md     # 商店详情页展示
├── CHANGELOG.md  # 更新日志（商店「更新日志」分栏展示）
└── community-index.entry.json  # 社区索引条目
```

## 约定

- **仅允许 `pallas.api.*`**（社区插件 L1 规则）：勿 import `pallas.core.*` / `pallas.console.*` / `pallas.product.*` / `src.*`。
- 命令权限走 [cmd_perm](https://github.com/PallasBot/Pallas-Bot/blob/dev/docs/common/cmd_perm/README.md) 的 `command_permissions`；`usage` 不写死权限角色，帮助图自动展示「何人可用」。
- 在本体仓校验：`uv run python tools/community_plugin_author.py check <本仓路径> --profile L1`。
- **版本与更新日志**：遵循[语义化版本](https://semver.org/lang/zh-CN/)；维护 `CHANGELOG.md`（[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)），日常改动记入 `## [Unreleased]`，发布时归档到 `## [X.Y.Z]` 并打 `vX.Y.Z` git tag；同步 `community-index.entry.json` 的 `version`。
- 改 `community-index.entry.json` 后，记得在 [community-plugin-index](https://github.com/PallasBot/community-plugin-index) 同步条目。

详见 [社区插件开发者指南](https://github.com/PallasBot/Pallas-Bot/blob/dev/docs/guide/community-plugin-author.md)。
