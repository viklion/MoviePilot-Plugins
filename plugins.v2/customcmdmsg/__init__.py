from typing import Any, List, Dict, Tuple, Optional

import pytz
from app.core.event import eventmanager, Event
from app.log import logger
from app.plugins import _PluginBase
from app.schemas.types import EventType

class CustomCmdMsg(_PluginBase):
    # 插件名称
    plugin_name = "自定义命令回复消息"
    # 插件描述
    plugin_desc = "自定义tg命令、微信按钮回复消息。"
    # 插件图标
    plugin_icon = "Wecom_A.png"
    # 插件版本
    plugin_version = "1.0"
    # 插件作者
    plugin_author = "viklion"
    # 作者主页
    author_url = "https://github.com/viklion"
    # 插件配置项ID前缀
    plugin_config_prefix = "customcmdmsg_"
    # 加载顺序
    plugin_order = 0
    # 可使用的用户级别
    auth_level = 2

    # 配置属性
    _enabled: bool = False
    _msg_text: str = ""


    def init_plugin(self, config: dict = None):
        # 配置
        if config:
            self._enabled = config.get("enabled", False)
            self._msg_text = config.get("msg_text", "回复的内容")


            # 保存配置
            self.__update_config()


    def __update_config(self):
        # 保存配置
        self.update_config(
            {
                "enabled": self._enabled,
                "msg_text": self._msg_text,
            }
        )

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        """
        定义远程控制命令
        :return: 命令关键字、事件、描述、附带数据
        """
        return [{
            "cmd": "/custom_cmdmsg",
            "event": EventType.PluginAction,
            "desc": "自定义回复",
            "category": "",
            "data": {
                "action": "custom_cmdmsg"
            }
        }]

    def get_api(self) -> List[Dict[str, Any]]:
        pass

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面，需要返回两块数据：1、页面配置；2、数据结构
        """
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'props': {
                            'align': 'center'
                        },
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextarea',
                                        'props': {
                                            'model': 'msg_text',
                                            'label': '文本内容',
                                            'placeholder': '自定义回复的内容',
                                            "clearable": True,
                                            'active': True,
                                        }
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        'component': 'VRow',
                        'props': {
                            'align': 'center'
                        },
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'style': 'white-space: pre-line;',
                                            'text': '注意：\n'
                                                    '需配合『命令管理』插件实现添加微信按钮\n'
                                                    '作者仓库：https://github.com/InfinityPacer/MoviePilot-Plugins/'
                                        }
                                    }
                                ]
                            },
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "msg_text": "回复的内容",
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        pass

    @eventmanager.register(EventType.PluginAction)
    def custom_cmdmsg(self, event: Event = None):
        """
        收到命令，发送自定义回复消息
        """
        if event:
            event_data = event.event_data
            if not event_data or event_data.get("action") != "custom_cmdmsg":
                return
        
        if event:
            logger.info("收到命令，回复消息 ...")
            self.post_message(channel=event.event_data.get("channel"),
                              title=self._text,
                              userid=event.event_data.get("user"))