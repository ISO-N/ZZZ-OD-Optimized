from PySide6.QtGui import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon, HyperlinkCard

from one_dragon.base.operation.one_dragon_env_context import OneDragonEnvContext
from one_dragon.utils.i18_utils import gt
from one_dragon_qt.widgets.scroll_credits import ScrollCreditsWidget
from one_dragon_qt.widgets.vertical_scroll_interface import VerticalScrollInterface


class LikeInterface(VerticalScrollInterface):

    def __init__(self, ctx: OneDragonEnvContext, parent=None):
        VerticalScrollInterface.__init__(self, object_name='like_interface',
                                         parent=parent, content_widget=None,
                                         nav_text_cn='点赞', nav_icon=FluentIcon.HEART)
        self.ctx: OneDragonEnvContext = ctx

    def get_content_widget(self) -> QWidget:
        # 主容器
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(40)

        # 左侧栏
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        star_opt = HyperlinkCard(icon=FluentIcon.HOME, title='Star', text=gt('前往'),
                                 content=gt('GitHub主页右上角点一个星星是最简单直接的'),
                                 url=self.ctx.project_config.github_homepage)
        star_opt.setFixedHeight(50)
        left_layout.addWidget(star_opt)

        left_layout.addStretch(1)

        # 右侧栏 - 滚动字幕
        scroll_credits = ScrollCreditsWidget(self.ctx)
        scroll_credits.setMinimumWidth(400)

        # 添加到主布局
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(scroll_credits, 2)

        return main_widget
