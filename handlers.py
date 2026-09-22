from __future__ import annotations

import asyncio
from collections import deque
from random import choice, randint
from time import monotonic
from typing import TYPE_CHECKING

from nonebot import logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, PokeNotifyEvent
from nonebot.exception import ActionFailed

from pallas.api.logging import format_plugin_event
from pallas.api.platform import resolve_group_admin_capability

from .config import get_config
from .service import poke_image_candidates, schedule_user_likes
from .spam import record_spam_message

if TYPE_CHECKING:
    from nonebot.adapters import Bot

    from pallas.api.commands import PluginHandlerContext


_spam_windows: dict[tuple[int, int, int], deque[float]] = {}
_spam_mute_inflight: set[tuple[int, int, int]] = set()


async def handle_praise(ctx: PluginHandlerContext) -> None:
    cfg = get_config()
    if not cfg.enable_like:
        return
    user_id = ctx.event.user_id
    if not isinstance(user_id, int) or user_id <= 0:
        return
    schedule_user_likes(ctx.bot, user_id, times=cfg.like_times)


async def handle_spam_moderation(bot: Bot, event: GroupMessageEvent) -> None:
    cfg = get_config()
    if not cfg.enable_spam_moderation:
        return

    bot_id = int(bot.self_id)
    group_id = int(event.group_id)
    user_id = int(event.user_id)
    if user_id == bot_id:
        return

    key = (bot_id, group_id, user_id)
    if key in _spam_mute_inflight:
        return
    try:
        if await resolve_group_admin_capability(group_id, bot_id, bot=bot) is not True:
            return
    except Exception as e:
        logger.debug("spam moderation bot role check failed group_id={} bot_id={}: {}", group_id, bot_id, e)
        return

    timestamps = _spam_windows.setdefault(key, deque())
    if not record_spam_message(
        timestamps,
        now=monotonic(),
        threshold=cfg.spam_message_threshold,
        window_sec=cfg.spam_window_sec,
    ):
        return

    _spam_windows.pop(key, None)
    _spam_mute_inflight.add(key)
    try:
        await mute_spammer(bot, group_id, user_id, cfg)
    finally:
        _spam_mute_inflight.discard(key)


async def mute_spammer(bot: Bot, group_id: int, user_id: int, cfg) -> None:
    try:
        target_info = await bot.call_api(
            "get_group_member_info",
            group_id=group_id,
            user_id=user_id,
            no_cache=True,
        )
        if not isinstance(target_info, dict) or target_info.get("role") != "member":
            return

        min_sec, max_sec = sorted((cfg.spam_mute_min_sec, cfg.spam_mute_max_sec))
        duration = randint(min_sec, max_sec)
        await bot.call_api(
            "set_group_ban",
            group_id=group_id,
            user_id=user_id,
            duration=duration,
        )
    except Exception as e:
        logger.warning("spam moderation failed in group [{}] for user [{}]: {}", group_id, user_id, e)
        return

    logger.info(
        format_plugin_event(
            "spam_moderation",
            f"Bot [{bot.self_id}] muted spammer [{user_id}] in group [{group_id}] for [{duration}s]",
        )
    )


async def handle_poke_reply(bot: Bot, event: PokeNotifyEvent) -> None:
    cfg = get_config()
    if not cfg.enable_poke_reply:
        return
    if event.target_id != event.self_id:
        return
    group_id = event.group_id
    if group_id is None:
        return
    allowed = {int(gid) for gid in cfg.poke_group_ids}
    if not allowed or int(group_id) not in allowed:
        return

    image_files = poke_image_candidates()
    if not image_files:
        await bot.send(event, "没有找到图片文件")
        logger.warning("poke image dir empty for group_id={}", group_id)
        return

    img = choice(image_files)
    try:
        await bot.send(event, MessageSegment.image(f"file://{img.absolute()}"))
        logger.info(
            format_plugin_event(
                "poke_reply",
                f"Bot [{bot.self_id}] replied a poke image in group [{group_id}]",
            )
        )
        return
    except Exception as e:
        logger.debug("poke image file:// failed: {}", e)

    try:
        image_bytes = await asyncio.to_thread(img.read_bytes)
        await bot.send(event, MessageSegment.image(image_bytes))
        logger.info(
            format_plugin_event(
                "poke_reply",
                f"Bot [{bot.self_id}] replied a poke image in group [{group_id}]",
            )
        )
    except Exception as e:
        logger.debug("poke image bytes failed: {}", e)
        await bot.send(event, "图片发送失败")


async def handle_set_special_title(ctx: PluginHandlerContext) -> None:
    cfg = get_config()
    if not cfg.enable_special_title:
        return
    event = ctx.event
    if not isinstance(event, GroupMessageEvent):
        return

    at_list = [seg.data["qq"] for seg in event.message if seg.type == "at" and seg.data.get("qq") != "all"]
    target_user_id = event.user_id
    if at_list:
        try:
            target_user_id = int(at_list[0])
        except (TypeError, ValueError):
            await ctx.finish("未识别到有效的目标成员，请重试")

    title_parts: list[str] = []
    command_consumed = False
    for seg in event.message:
        if seg.type == "at":
            continue
        if seg.type != "text":
            continue
        text = seg.data.get("text", "")
        if not command_consumed:
            command_idx = text.find("/群头衔")
            if command_idx == -1:
                continue
            text = text[command_idx + len("/群头衔") :]
            command_consumed = True
        title_parts.append(text)

    special_title = "".join(title_parts).strip()
    if not special_title:
        await ctx.finish("请输入头衔内容，格式：/群头衔@某人 头衔 或 /群头衔 头衔")

    try:
        bot_member_info = await ctx.bot.call_api(
            "get_group_member_info",
            group_id=event.group_id,
            user_id=int(ctx.bot.self_id),
            no_cache=True,
        )
        if bot_member_info.get("role") != "owner":
            return

        await ctx.bot.call_api(
            "set_group_special_title",
            group_id=event.group_id,
            user_id=target_user_id,
            special_title=special_title,
        )
    except ActionFailed as e:
        logger.error("设置群头衔失败: {}", e)
        await ctx.finish("设置群头衔失败，请确认牛牛权限是否足够")
    except Exception as e:
        logger.error("处理设置群头衔消息时发生错误: {}", e)
        await ctx.finish("设置群头衔时发生异常，请稍后重试")
    else:
        logger.info(
            format_plugin_event(
                "set_special_title",
                f"Bot [{ctx.bot.self_id}] set the group special title of user [{target_user_id}] "
                f"in group [{event.group_id}]",
            )
        )
        await ctx.finish(MessageSegment.at(target_user_id) + f" 头衔已设置为：{special_title}")
