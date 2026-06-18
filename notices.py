from __future__ import annotations

from typing import TYPE_CHECKING

from nonebot import on_message, on_notice
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, PokeNotifyEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import Rule

from pallas.api.perm import group_message_permission_for_command

from .handlers import handle_poke_reply, handle_set_special_title

if TYPE_CHECKING:
    from nonebot.adapters import Bot
    from nonebot.typing import T_State


def poke_target_is_self(event: PokeNotifyEvent) -> bool:
    return event.target_id == event.self_id


poke = on_notice(rule=Rule(poke_target_is_self), priority=100, block=False)


@poke.handle()
async def on_poke(bot: Bot, event: PokeNotifyEvent) -> None:
    await handle_poke_reply(bot, event)


async def is_set_special_title_msg(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupMessageEvent) and event.get_plaintext().strip().startswith("/群头衔")


set_special_title_msg = on_message(
    rule=Rule(is_set_special_title_msg),
    priority=5,
    block=True,
    permission=group_message_permission_for_command("interact.set_title") | SUPERUSER,
)


@set_special_title_msg.handle()
async def on_set_special_title(bot: Bot, event: GroupMessageEvent) -> None:
    from pallas.api.commands import PluginHandlerContext

    ctx = PluginHandlerContext(
        bot=bot,
        event=event,
        command_id="interact.set_title",
        matcher=set_special_title_msg,
        plugin_tag="interact",
    )
    await handle_set_special_title(ctx)
