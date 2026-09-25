# 更新日志

本文件记录牛牛互动 interact 的版本变更，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.9] - 2026-09-25

### Fixed

- 修复多个牛牛同时在线时刷屏消息分散接收导致的漏判。
- 修复同一条消息被多个牛牛转发时可能重复计数的问题。

## [0.1.8] - 2026-09-23

### Added

- 新增可配置的刷屏管理：达到消息阈值后，对普通成员随机禁言。

### Changed

- 刷屏管理默认改为 5 秒内达到 4 条消息后触发。

## [0.1.7] - 2026-08-11

- feat(logging): 补充点赞、戳一戳回图与群头衔设置业务事件日志

## [0.1.6] - 2026-07-26

- feat(llm_tools): 为口令工具补充口语 hints

## [0.1.5] - 2026-07-25

### Added

- 声明 `interact.praise` LLM 工具，供闲聊触发名片点赞。

## [0.1.4] - 2026-07-25

### Added

- `metadata.extra.help_tag`：帮助图分组为「聊天」(chat)。

## [0.1.3] - 2026-07-21

### Fixed

- 修复 `from __future__ import annotations` 下 `Bot`/`T_State` 仅 TYPE_CHECKING 导入导致 NoneBot DI 解析失败的启动告警。

## [0.1.2] - 2026-06-27
- docs(readme): 命令权限表头统一为「默认等级」

## [0.1.1] - 2026-06-27
- docs(readme): 「怎么使用」口令统一加行内代码标记

## [0.1.0] - 2026-06-26

社区插件正式开始版本控制的首个发布版本。

### Added

- 名片点赞：`牛牛赞我` / `赞我` / `牛牛点赞`，调用 OneBot `send_like` 为发送者点赞。
- 群头衔：`/群头衔@成员 头衔` 或 `/群头衔 头衔`，群主牛牛为成员设置专属头衔。
- 戳一戳回图：在已启用的群内戳牛牛随机回图，支持自定义目录与资源回退。
- 知识源 `interact.faq`：向 LLM 注入名片点赞、群头衔、戳一戳的说明。
- 插件商店头像、图标与封面资源。

[0.1.9]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.8...v0.1.9
[0.1.8]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.7...v0.1.8
[Unreleased]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.9...HEAD
[0.1.4]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/TogetsuDo/pallas-community-plugin-interact/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/TogetsuDo/pallas-community-plugin-interact/releases/tag/v0.1.0
