from typing import Any

from app.plugins import _PluginBase
from app.schemas.types import EventType
from app.sdk.events import Event, eventmanager
from app.sdk.logging import logger


class CustomCmdMsgV3(_PluginBase):
    """命令回复自定义消息插件。"""

    # 插件名称
    plugin_name = "命令回复自定义消息v3"
    # 插件描述
    plugin_desc = "通过发送命令、微信按钮回复自定义消息。"
    # 插件图标
    plugin_icon = "Wecom_A.png"
    # 插件版本
    plugin_version = "3.0.0"
    # 插件作者
    plugin_author = "viklion"
    # 作者主页
    author_url = "https://github.com/viklion"
    # 插件配置项 ID 前缀
    plugin_config_prefix = "customcmdmsgv3_"
    # 加载顺序
    plugin_order = 0
    # 可使用的用户级别
    auth_level = 1

    # 配置
    _enabled: bool = False
    _msg_title: str | None = None
    _msg_text: str | None = None
    _msg_image: str | None = None
    _msg_link: str | None = None

    def init_plugin(self, config: dict | None = None) -> None:
        """初始化插件配置。"""
        config = config or {}

        self._enabled = bool(config.get("enabled", False))
        self._msg_title = config.get("msg_title")
        self._msg_text = config.get("msg_text")
        self._msg_image = config.get("msg_image")
        self._msg_link = config.get("msg_link")

    def _save_config(self) -> None:
        """保存插件配置。"""
        self.update_config(
            {
                "enabled": self._enabled,
                "msg_title": self._msg_title,
                "msg_text": self._msg_text,
                "msg_image": self._msg_image,
                "msg_link": self._msg_link,
            }
        )

    def get_state(self) -> bool:
        """返回插件启用状态。"""
        return self._enabled

    @staticmethod
    def get_command() -> list[dict[str, Any]]:
        """
        定义远程控制命令。
        """
        return [
            {
                "cmd": "/custom_cmdmsg",
                "event": EventType.PluginAction,
                "desc": "自定义回复",
                "category": "",
                "data": {
                    "action": "custom_cmdmsg",
                },
            }
        ]

    def get_api(self) -> list[dict[str, Any]]:
        """本插件不提供 HTTP API。"""
        return []

    def get_form(self) -> tuple[list[dict], dict[str, Any]]:
        """
        拼装插件配置页面。

        返回：
        1. 页面配置
        2. 默认数据模型
        """
        return [
            {
                "component": "VForm",
                "content": [
                    {
                        "component": "VRow",
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                    "md": 6,
                                },
                                "content": [
                                    {
                                        "component": "VSwitch",
                                        "props": {
                                            "model": "enabled",
                                            "label": "启用插件",
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "component": "VRow",
                        "props": {
                            "align": "center",
                        },
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                    "md": 12,
                                },
                                "content": [
                                    {
                                        "component": "VTextField",
                                        "props": {
                                            "model": "msg_title",
                                            "label": "消息主题",
                                            "clearable": True,
                                            "placeholder": "消息主题与文本内容必须填写其中一项，否则无法回复自定义消息！",
                                            "hint": "适配各种字符，支持换行符",
                                            "persistent-hint": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "component": "VRow",
                        "props": {
                            "align": "center",
                        },
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                    "md": 12,
                                },
                                "content": [
                                    {
                                        "component": "VTextarea",
                                        "props": {
                                            "model": "msg_text",
                                            "label": "文本内容",
                                            "clearable": True,
                                            "placeholder": "消息主题与文本内容必须填写其中一项，否则无法回复自定义消息！",
                                            "hint": "适配各种字符，支持换行符",
                                            "persistent-hint": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "component": "VRow",
                        "props": {
                            "align": "center",
                        },
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                    "md": 12,
                                },
                                "content": [
                                    {
                                        "component": "VTextField",
                                        "props": {
                                            "model": "msg_image",
                                            "label": "图片地址",
                                            "clearable": True,
                                            "placeholder": "目前只支持输入图片地址或本地路径",
                                            "hint": "图片URL地址，如果是服务器的本地图片，请自行确定具体路径。",
                                            "persistent-hint": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "component": "VRow",
                        "props": {
                            "align": "center",
                        },
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                    "md": 12,
                                },
                                "content": [
                                    {
                                        "component": "VTextField",
                                        "props": {
                                            "model": "msg_link",
                                            "label": "链接地址",
                                            "clearable": True,
                                            "placeholder": "https://example.com/",
                                            "hint": "URL链接地址；一般用于需要跳转功能的消息。",
                                            "persistent-hint": True,
                                            "active": True,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "component": "VRow",
                        "props": {
                            "align": "center",
                        },
                        "content": [
                            {
                                "component": "VCol",
                                "props": {
                                    "cols": 12,
                                    "md": 12,
                                },
                                "content": [
                                    {
                                        "component": "VAlert",
                                        "props": {
                                            "type": "info",
                                            "variant": "tonal",
                                            "style": "white-space: pre-line;",
                                            "text": (
                                                "注意：\n"
                                                "*命令为：/custom_cmdmsg\n"
                                                "\n"
                                                "*需配合『命令管理』插件实现添加微信按钮\n"
                                                "作者仓库：https://github.com/InfinityPacer/MoviePilot-Plugins/\n"
                                                "\n"
                                                "*本插件参考Aqr-K的自定义消息汇报插件\n"
                                                "作者仓库：https://github.com/Aqr-K/Moviepilot-Plugins/"
                                            ),
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                ],
            }
        ], {
            "enabled": False,
            "msg_title": "",
            "msg_text": "",
            "msg_image": "",
            "msg_link": "",
        }

    def get_page(self) -> list[dict]:
        """本插件没有额外详情页。"""
        return []

    def stop_service(self) -> None:
        """释放插件资源。"""
        pass

    @eventmanager.register(EventType.PluginAction)
    def custom_cmd_msg(self, event: Event) -> None:
        """
        收到命令，发送自定义回复消息。
        """
        event_data = event.event_data or {}

        if event_data.get("action") != "custom_cmdmsg":
            return

        logger.debug(event_data)

        userid = event_data.get("user")
        channel = event_data.get("channel")
        source = event_data.get("source")

        if not channel:
            logger.warning("收到自定义消息命令，但缺少消息渠道")
            return

        channel_str = channel.value

        logger.info(
            f"收到来自'用户:{userid},渠道:{channel_str},来源:{source}'的命令，回复消息..."
        )

        self.post_message(
            channel=channel,
            title=self._msg_title,
            text=self._msg_text,
            image=self._msg_image,
            link=self._msg_link,
            userid=userid,
            source=source,
        )