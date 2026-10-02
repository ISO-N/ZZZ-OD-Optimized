import numpy as np
from cv2.typing import MatLike
from PIL import ImageGrab

from one_dragon.base.controller.pc_screenshot.screencapper_base import ScreencapperBase
from one_dragon.base.geometry.rectangle import Rect


class PilScreencapper(ScreencapperBase):
    """使用 PIL (pyautogui) 进行截图的策略"""

    def init(self) -> bool:
        """初始化 PIL 截图方法

        PIL 不需要初始化

        Returns:
            始终返回 True
        """
        return True

    def capture(self, rect: Rect, independent: bool = False) -> MatLike | None:
        """使用 PIL 截图

        Args:
            rect: 截图区域
            independent: 是否独立截图

        Returns:
            截图数组，失败返回 None
        """
        try:
            # 直接按 bbox 抓目标区域，并开启 all_screens：
            # pyautogui.screenshot(region=...) 内部是「先 ImageGrab.grab(all_screens=False)
            # 抓整个主屏、再 crop 到 region」，实测这次多余的 crop 要花约 2ms；
            # 而且 all_screens=False 时窗口在副屏会抓到错误的屏幕。
            img = ImageGrab.grab(
                bbox=(rect.x1, rect.y1, rect.x1 + rect.width, rect.y1 + rect.height),
                all_screens=True,
            )
            # 用 np.array 而不是 np.asarray：前者一定返回可写的新数组。
            # 截图下游有就地改写（UID 遮挡），只读视图会直接报错。
            screenshot = np.array(img)
        except Exception:
            return None

        return screenshot

    def cleanup(self):
        """PIL不需要清理资源"""
        pass
