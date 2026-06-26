from nonebot.plugin import PluginMetadata

from pallas.api.commands import (
    bind_alias_handlers,
    command_perm_list,
    command_perm_row,
    message_command,
)
from pallas.api.metadata import (
    PLUGIN_EXTRA_VERSION,
    PLUGIN_HOMEPAGE,
    PLUGIN_MENU_TEMPLATE,
    SCENE_AUTO,
    SCENE_BOTH,
    SCENE_GROUP,
    join_usage,
    knowledge_source_row,
    usage_line,
)

from . import notices as _notices  # noqa: F401
from .handlers import handle_praise

PLUGIN_ID = "interact"

__plugin_meta__ = PluginMetadata(
    name="牛牛互动",
    description="名片点赞、戳一戳回图与群主设置专属头衔。",
    usage=join_usage(
        usage_line("牛牛赞我 / 赞我 / 牛牛点赞", "给发送者名片点赞"),
        usage_line("/群头衔@成员 头衔", "群主牛牛设置专属头衔"),
    ),
    type="application",
    homepage=PLUGIN_HOMEPAGE,
    supported_adapters={"~onebot.v11"},
    extra={
        "version": PLUGIN_EXTRA_VERSION,
        "menu_template": PLUGIN_MENU_TEMPLATE,
        "command_permissions": command_perm_list(
            command_perm_row(f"{PLUGIN_ID}.praise", "牛牛赞我", "everyone"),
            command_perm_row(f"{PLUGIN_ID}.set_title", "/群头衔", "group_moderator"),
        ),
        "menu_data": [
            {
                "func": "名片点赞",
                "trigger_method": "on_command",
                "trigger_scene": SCENE_BOTH,
                "trigger_condition": "牛牛赞我、赞我、牛牛点赞",
                "command_permission": f"{PLUGIN_ID}.praise",
                "brief_des": "调用 QQ 名片点赞",
                "detail_des": "需牛牛与发送者为好友；次数可在插件配置中调整。",
            },
            {
                "func": "设置群头衔",
                "trigger_method": "on_message",
                "trigger_scene": SCENE_GROUP,
                "trigger_condition": "/群头衔@某人 头衔 或 /群头衔 头衔",
                "command_permission": f"{PLUGIN_ID}.set_title",
                "brief_des": "设置专属头衔",
                "detail_des": "仅当牛牛为该群群主时生效；发送者须为群管或群主。",
            },
            {
                "func": "戳一戳回图",
                "trigger_method": "on_notice",
                "trigger_scene": SCENE_AUTO,
                "trigger_condition": "群内戳牛牛",
                "brief_des": "随机回复图片",
                "detail_des": "需在插件配置中启用并填写群号；图片放 `data/interact/poke_images/`。",
            },
        ],
        "knowledge_sources": [
            knowledge_source_row(
                source_id="interact.faq",
                title="牛牛互动说明",
                description="名片点赞、戳一戳与群头衔",
                chunks=[
                    {
                        "title": "名片点赞",
                        "content": (
                            "发送「牛牛赞我」「赞我」或「牛牛点赞」"
                            "可为发送者 QQ 名片点赞；须牛牛与发送者为好友。"
                        ),
                        "keywords": "赞我,点赞,名片,牛牛赞我",
                    },
                    {
                        "title": "设置群头衔",
                        "content": (
                            "群内发送「/群头衔@某人 头衔」或「/群头衔 头衔」设置专属头衔；"
                            "仅当牛牛为该群群主且发送者为群管或群主时生效。"
                        ),
                        "keywords": "群头衔,头衔,专属,设置",
                    },
                    {
                        "title": "戳一戳回图",
                        "content": (
                            "在群内戳牛牛可能随机回复图片；"
                            "需在插件配置中启用并填写群号，图片目录为 data/interact/poke_images/。"
                        ),
                        "keywords": "戳一戳,回图,戳牛牛,图片",
                    },
                ],
            ),
        ],
    },
)

praise_cmd = message_command(
    f"{PLUGIN_ID}.praise",
    "牛牛赞我",
    aliases=("赞我", "牛牛点赞"),
    scene="both",
    cd_sec=0,
    priority=5,
    block=True,
)

bind_alias_handlers(praise_cmd, handle_praise)
