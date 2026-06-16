from __future__ import annotations

import asyncio
from random import choice

from nonebot import logger
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, PokeNotifyEvent
from nonebot.exception import ActionFailed

from src.features.plugin_sdk import PluginHandlerContext

from .config import get_config
from .service import poke_image_candidates, schedule_user_likes


async def handle_praise(ctx: PluginHandlerContext) -> None:
    cfg = get_config()
    if not cfg.enable_like:
        return
    user_id = ctx.event.user_id
    if not isinstance(user_id, int) or user_id <= 0:
        return
    schedule_user_likes(ctx.bot, user_id, times=cfg.like_times)


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
        return
    except Exception as e:
        logger.debug("poke image file:// failed: {}", e)

    try:
        image_bytes = await asyncio.to_thread(img.read_bytes)
        await bot.send(event, MessageSegment.image(image_bytes))
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

    at_list = [
        seg.data["qq"]
        for seg in event.message
        if seg.type == "at" and seg.data.get("qq") != "all"
    ]
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
        await ctx.finish(MessageSegment.at(target_user_id) + f" 头衔已设置为：{special_title}")
