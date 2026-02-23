from typing import Any, List, Dict, Tuple, Optional

from app.core.config import settings
from app.log import logger
from app.plugins import _PluginBase
from app.agent.prompt import prompt_manager


class CustomAgentPrompt(_PluginBase):
    # 插件名称
    plugin_name = "自定义智能体提示词"
    # 插件描述
    plugin_desc = "自定义修改智能体提示词。"
    # 插件图标
    plugin_icon = "Bookstack_A.png"
    # 插件版本
    plugin_version = "1.0"
    # 插件作者
    plugin_author = "viklion"
    # 作者主页
    author_url = "https://github.com/viklion"
    # 插件配置项ID前缀
    plugin_config_prefix = "customagentprompt_"
    # 加载顺序
    plugin_order = 0
    # 可使用的用户级别
    auth_level = 1

    # 配置属性
    _enabled: bool = False
    _auto_replace: bool = False
    _prompt_custom: Optional[str] = None

    prompt_txt = settings.ROOT_PATH / "app"  / "agent" / "prompt" / "Agent Prompt.txt"

    def init_plugin(self, config: dict = None):
        # 配置
        if config:
            self._enabled = config.get("enabled", False)
            self._auto_replace = config.get("auto_replace", False)
            self._prompt_custom = config.get("prompt_custom") or self.prompt_txt.read_text(encoding="utf-8")

            # 单次写入
            if self._enabled:
                if self._prompt_custom:
                    self.prompt_txt.write_text(self._prompt_custom, encoding="utf-8")
                    logger.info("已单次更新智能体提示词内容")
                    # 清空提示词缓存
                    prompt_manager.clear_cache()
                    logger.info("已清空智能体提示词缓存")
                else:
                    logger.warning("智能体提示词内容为空，本次未写入")
                self._enabled = False
                # 保存配置
                self.__update_config()
                return

            # 自动替换
            if self._auto_replace:
                if self._prompt_custom:
                    self.prompt_txt.write_text(self._prompt_custom, encoding="utf-8")
                    logger.info("已自动替换智能体提示词内容")
                    # 清空提示词缓存
                    prompt_manager.clear_cache()
                    logger.info("已清空智能体提示词缓存")
                else:
                    logger.warning("智能体提示词内容为空，未自动替换")

            self.__update_config()

    def __update_config(self):
        # 保存配置
        self.update_config(
            {
                "enabled": self._enabled,
                "auto_replace": self._auto_replace,
                "prompt_custom": self._prompt_custom,
                "prompt_now": self.prompt_txt.read_text(encoding="utf-8"),
            }
        )

    def get_state(self) -> bool:
        return self._auto_replace

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

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
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'auto_replace',
                                            'label': '自动替换提示词',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '本次替换提示词',
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
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'style': 'white-space: pre-line;',
                                            'text': '注意：\n'
                                                    '*如果容器更新后提示词恢复默认，可以尝试开启自动替换。\n'
                                                    '默认提示词内容见：'
                                        },
                                        'content': [
                                            {
                                                'component': 'a',
                                                'props': {
                                                    'href': 'https://github.com/jxxghp/MoviePilot/blob/v2/app/agent/prompt/Agent%20Prompt.txt',
                                                    'target': '_blank'
                                                },
                                                'content': [
                                                    {
                                                        'component': 'u',
                                                        'text': '[github]jxxghp/MoviePilot - Agent Prompt.txt'
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        'component': 'VTabs',
                        'props': {
                            'model': '_tabs',
                            'style': {
                                'margin-top': '8px',
                                'margin-bottom': '16px'
                            },
                            'stacked': False,
                            'fixed-tabs': False
                        },
                        'content': [
                            {
                                'component': 'VTab',
                                'props': {
                                    'value': 'preset_tab'
                                },
                                'text': '当前提示词'
                            }, {
                                'component': 'VTab',
                                'props': {
                                    'value': 'custom_tab'
                                },
                                'text': '自定义提示词'
                            }
                        ]
                    },
                    {
                        'component': 'VWindow',
                        'props': {
                            'model': '_tabs'
                        },
                        'content': [
                            {
                                'component': 'VWindowItem',
                                'props': {
                                    'value': 'preset_tab'
                                },
                                'content': [
                                    {
                                        'component': 'VRow',
                                        'content': [
                                            {
                                                'component': 'VCol',
                                                'props': {
                                                    "cols": 12
                                                },
                                                'content': [
                                                    {
                                                        'component': 'VAceEditor',
                                                        'props': {
                                                            'modelvalue': 'prompt_now',
                                                            'lang': 'text',
                                                            'theme': 'monokai',
                                                            'style': 'height: 35rem; font-size: 14px',
                                                            'readonly': True
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                'component': 'VWindowItem',
                                'props': {
                                    'value': 'custom_tab'
                                },
                                'content': [
                                    {
                                        'component': 'VRow',
                                        'content': [
                                            {
                                                'component': 'VCol',
                                                'props': {
                                                    "cols": 12
                                                },
                                                'content': [
                                                    {
                                                        'component': 'VAceEditor',
                                                        'props': {
                                                            'modelvalue': 'prompt_custom',
                                                            'lang': 'text',
                                                            'theme': 'monokai',
                                                            'style': 'height: 35rem; font-size: 14px'
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                ]
            }
        ], {
            "enabled": False,
            "auto_replace": False,
            "prompt_now" : self.prompt_txt.read_text(encoding="utf-8"),
            "prompt_custom": self.prompt_txt.read_text(encoding="utf-8"),
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        pass