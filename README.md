# 牛牛互动（`niuniu_interact`）

Pallas-Bot **社区插件示范**：名片点赞、戳一戳回图、群主设置专属头衔。

本仓库为 **NoneBot 插件包根目录**（含 `__init__.py`），安装后位于 Bot 的 `local/plugins/niuniu_interact/`。

## 功能

| 触发 | 场景 | 说明 |
| --- | --- | --- |
| 牛牛赞我 / 赞我 / 牛牛点赞 | 群聊、私聊 | 后台调用 `send_like` 点赞 |
| 戳牛牛 | 群通知 | 在配置的群内随机回复图片（默认关闭） |
| `/群头衔@成员 头衔` | 群内 | 群主牛牛设置专属头衔 |

## 安装

### 插件商店（推荐）

1. 确保 Bot ≥ 4.0，且 `config/pallas.toml` 含 `extra_plugin_dirs = ["local/plugins"]`
2. 控制台 → **插件商店 → 社区插件** → 安装 **牛牛互动**
3. 重启 Bot

### 手工 clone

```bash
git clone --depth 1 https://github.com/TogetsuDo/pallas-community-plugin-niuniu-interact.git local/plugins/niuniu_interact
```

## 配置（WebUI → 插件）

| 键 | 默认 | 说明 |
| --- | --- | --- |
| enable_like | true | 是否响应赞我口令 |
| like_times | 10 | 每次点赞次数（1–50） |
| enable_poke_reply | false | 戳一戳是否回图 |
| poke_group_ids | [] | 启用回图的群号列表 |
| poke_image_dir | （空） | 自定义图片目录；默认 `data/niuniu_interact/poke_images/` |
| poke_fallback_resource_subdir | image/ginko | 插件目录无图时尝试 `resource/` 子路径 |
| enable_special_title | true | 是否启用 `/群头衔` |

戳一戳图片：将 jpg/png/webp 等放入 `data/niuniu_interact/poke_images/`，并在配置中填写群号。

## 命令权限

| 命令 ID | 默认等级 |
| --- | --- |
| `niuniu_interact.praise` | everyone |
| `niuniu_interact.set_title` | group_moderator |

## 依赖

- 运行于 [Pallas-Bot](https://github.com/PallasBot/Pallas-Bot) ≥ 4.0（使用 `plugin_sdk`、WebUI 热重载）
- OneBot V11 协议端
- 名片点赞需牛牛与目标用户为 **QQ 好友**

## 与 Cookbook「牛牛赞我」的区别

主仓 [Cookbook · praise_me](https://github.com/PallasBot/Pallas-Bot/blob/dev/docs/develop/plugin/cookbook.md) 演示 **群内计数赞榜**（`GroupPluginStorage`）。  
本插件调用 **QQ 原生点赞 API**，并含戳一戳、群头衔等站点向功能，适合作为 **社区插件上架范例**。

## 收录索引

条目见 [PallasBot/community-plugin-index](https://github.com/PallasBot/community-plugin-index) 的 `index.json`。

## 许可

AGPL-3.0（与 Pallas-Bot 一致）
