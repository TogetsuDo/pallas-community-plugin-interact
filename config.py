from pydantic import BaseModel, Field

from pallas.api.config import install_hot_reload_config


class Config(BaseModel, extra="ignore"):
    enable_like: bool = Field(default=True, description="是否响应赞我口令并调用 QQ 名片点赞。")
    like_times: int = Field(default=10, ge=1, le=50, description="每次口令触发的点赞次数。")
    enable_poke_reply: bool = Field(default=False, description="是否在指定群内对戳一戳回复随机图片。")
    poke_group_ids: list[int] = Field(
        default_factory=list,
        description="启用戳一戳回复的群号列表；为空时不回复。",
    )
    poke_image_dir: str = Field(
        default="",
        description="戳一戳回复图片目录；留空使用 `data/interact/poke_images/`。",
    )
    poke_fallback_resource_subdir: str = Field(
        default="",
        description="插件图片目录为空时，尝试 resource/ 下该相对路径；留空则不回退。",
    )
    enable_special_title: bool = Field(default=True, description="是否启用 /群头衔 设置专属头衔。")


plugin_webui = install_hot_reload_config(Config, config_module=__name__)
get_config = plugin_webui.get
