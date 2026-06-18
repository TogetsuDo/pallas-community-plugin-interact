from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

from nonebot import logger
from nonebot.exception import ActionFailed

from pallas.api.paths import plugin_data_dir, resource_dir

from .config import get_config

if TYPE_CHECKING:
    from nonebot.adapters import Bot

PLUGIN_ID = "interact"

_IMAGE_GLOBS = (
    "*.[jJ][pP][gG]",
    "*.[jJ][pP][eE][gG]",
    "*.[pP][nN][gG]",
    "*.[gG][iI][fF]",
    "*.[wW][eE][bB][pP]",
)


def resolve_poke_image_dir() -> Path:
    cfg = get_config()
    custom = (cfg.poke_image_dir or "").strip()
    if custom:
        return Path(custom).expanduser()
    return plugin_data_dir(PLUGIN_ID) / "poke_images"


def list_image_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    files: list[Path] = []
    for pattern in _IMAGE_GLOBS:
        files.extend(directory.glob(pattern))
    return sorted({path.resolve() for path in files if path.is_file()})


def poke_image_candidates() -> list[Path]:
    primary = list_image_files(resolve_poke_image_dir())
    if primary:
        return primary
    fallback_subdir = (get_config().poke_fallback_resource_subdir or "").strip()
    if not fallback_subdir:
        return []
    return list_image_files(resource_dir(*fallback_subdir.split("/")))


async def send_user_likes(bot: Bot, user_id: int, *, times: int) -> None:
    try:
        await bot.call_api("send_like", user_id=user_id, times=times)
    except ActionFailed as e:
        detail = str(e)
        if "点赞" in detail and "上限" in detail:
            logger.debug("send_like capped user_id={}: {}", user_id, e)
        else:
            logger.warning("send_like failed user_id={}: {}", user_id, e)
    except Exception as e:
        logger.warning("send_like unexpected error user_id={}: {}", user_id, e)


def schedule_user_likes(bot: Bot, user_id: int, *, times: int) -> None:
    asyncio.create_task(
        send_user_likes(bot, user_id, times=times),
        name=f"{PLUGIN_ID}_{bot.self_id}_{user_id}",
    )
