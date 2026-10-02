from one_dragon.base.config.yaml_config import YamlConfig


class PrivacyConfig(YamlConfig):
    """隐私相关配置。"""

    def __init__(self) -> None:
        YamlConfig.__init__(self, module_name='privacy')

    @property
    def telemetry_enabled(self) -> bool:
        """是否上报匿名遥测。默认关闭，隔离自己的用户数据不出本机。"""
        return self.get('telemetry_enabled', False)

    @telemetry_enabled.setter
    def telemetry_enabled(self, new_value: bool) -> None:
        self.update('telemetry_enabled', new_value)
