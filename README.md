<p align="center">
  <img src="./assets/brand-avatar.png" width="220" height="220" alt="牛牛互动">
</p>

<h1 align="center">牛牛互动 interact</h1>

<p align="center">名片点赞、戳一戳回图与群头衔互动示范插件。</p>

<p align="center">
  <img alt="社区插件" src="https://img.shields.io/badge/%E7%A4%BE%E5%8C%BA%E6%8F%92%E4%BB%B6-4B5563">
  <img alt="示范插件" src="https://img.shields.io/badge/%E7%A4%BA%E8%8C%83%E6%8F%92%E4%BB%B6-4EA94B">
  <img alt="版本" src="https://img.shields.io/badge/%E7%89%88%E6%9C%AC-v0.1.2-2563EB">
</p>

## 安装方式

可在控制台插件商店安装，也可按社区插件目录放入 `local/plugins/interact/`。

## 怎么使用

- `牛牛赞我`、`赞我`、`牛牛点赞`：让牛牛给你点名片赞。
- `/群头衔@成员 头衔` 或 `/群头衔 头衔`：给指定成员或自己设置群专属头衔。
- `群内戳一戳牛牛`：在已启用的群里随机回一张图。

> 详细用法、限制条件和可用范围以帮助为主。

## 命令权限

| 功能 | 默认等级 |
| --- | --- |
| `牛牛赞我` | 所有人 |
| `/群头衔` | 群管/群主 |

补充条件：

- `牛牛赞我` 需要牛牛和目标用户已经互为好友。
- `/群头衔` 只有当处理消息的牛牛本身是该群群主时才会真正生效。

## 配置项

> 可在控制台对应插件页中修改。

常用配置：

| 配置项 | 说明 |
| --- | --- |
| `enable_like` | 是否响应点赞口令 |
| `like_times` | 每次口令触发的点赞次数 |
| `enable_poke_reply` | 是否启用戳一戳回图 |
| `poke_group_ids` | 允许戳一戳回图的群号列表 |
| `poke_image_dir` | 自定义回图目录 |
| `poke_fallback_resource_subdir` | 自定义目录为空时的资源回退路径，默认留空（不回退） |
| `enable_special_title` | 是否启用 `/群头衔` |

## 排障

| 现象 | 处理 |
| --- | --- |
| `牛牛赞我` 没反应 | 检查 `enable_like` 是否开启，以及牛牛是否和目标用户互为好友。 |
| 戳一戳没有回图 | 检查 `enable_poke_reply`、`poke_group_ids` 和图片目录里是否真的有图。 |
| `/群头衔` 执行了但没改成功 | 这个功能要求牛牛自己是该群群主，不是群管理员。 |
| 回图提示没找到图片文件 | 补充 `poke_image_dir`，或确认 `resource/` 下的回退目录里存在图片。 |

## 实现

源码位置：

- 插件入口：[`__init__.py`](./__init__.py)
- 配置定义：[`config.py`](./config.py)
- 命令与通知处理：[`handlers.py`](./handlers.py)、[`notices.py`](./notices.py)
- 点赞与图片目录逻辑：[`service.py`](./service.py)

关键文件：

- [`__init__.py`](./__init__.py)：注册插件元数据、点赞口令和帮助菜单条目。
- [`handlers.py`](./handlers.py)：实现点赞、戳一戳回图、群头衔设置三类核心行为。
- [`notices.py`](./notices.py)：挂载戳一戳通知与 `/群头衔` 消息规则。
- [`service.py`](./service.py)：负责点赞调用、图片目录解析和图片候选收集。

实现要点：

- 点赞功能通过 OneBot `send_like` 异步调用 QQ 名片点赞接口。
- 戳一戳回图只在配置允许的群内触发，并且会先查自定义图片目录，再回退到 `resource/` 里的默认素材目录。
- `/群头衔` 不直接写死权限文案，真正执行时还会额外检查牛牛自己是否是群主。

## 更新日志

版本变更见 [`CHANGELOG.md`](./CHANGELOG.md)；也可在控制台插件商店弹窗的「更新日志」分栏查看。

## 相关链接

- [社区插件索引](https://github.com/PallasBot/Pallas-Bot-Community-Plugin-Index)
- [社区插件商店说明](https://github.com/PallasBot/Pallas-Bot/blob/dev/docs/guide/community-plugin-store.md)
