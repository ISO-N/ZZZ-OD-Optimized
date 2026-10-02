import os
import time
from cv2.typing import MatLike
from typing import List, Optional

from one_dragon.base.screen.template_info import TemplateInfo, is_template_existed
from one_dragon.utils import os_utils

# 模板不存在时的负缓存有效期（秒）。
# `is_template_existed` 每次要跑 1 次目录 + 3 次文件 os.path.exists（实测每次 460µs），
# 而调用方经常对着同一个不存在的模板反复问（画面识别里逐条模板试就是典型）。
# 用 TTL 而不是永久缓存：开发工具新建模板后，最多等这么久就能被认到。
MISSING_TEMPLATE_CACHE_TTL: float = 10.0


class TemplateLoader:

    def __init__(self):
        self.template: dict[str, TemplateInfo] = {}
        self._missing_until: dict[str, float] = {}  # key -> 负缓存到期时间（monotonic）

    def get_all_template_info_from_disk(self, need_raw: bool = True, need_config: bool = False) -> List[TemplateInfo]:
        """
        从硬盘加载模板信息
        模板存放在 assets/template 中，再按二级目录区分，例如 assets/template/x/y/
        x = 页面或者类别
        y = 具体的模板文件夹
        :param need_raw: 至少需要有扣出来的原图 开发工具中使用=False
        :param need_config: 是否需要有模板的配置文件 开发工具中使用=True
        :return:
        """
        info_list: List[TemplateInfo] = []

        template_dir = os_utils.get_path_under_work_dir('assets', 'template')
        sub_name_list_1 = os.listdir(template_dir)
        for sub_name_1 in sub_name_list_1:
            sub_dir_1 = os.path.join(template_dir, sub_name_1)
            if not os.path.isdir(sub_dir_1):
                continue
            sub_name_list_2 = os.listdir(sub_dir_1)
            for sub_name_2 in sub_name_list_2:
                sub_dir_2 = os.path.join(sub_dir_1, sub_name_2)
                if not os.path.isdir(sub_dir_2):
                    continue

                if not is_template_existed(sub_name_1, sub_name_2, need_raw=need_raw, need_config=need_config):
                    continue

                info_list.append(TemplateInfo(sub_name_1, sub_name_2))

        return info_list

    def load_template(self, sub_dir: str, template_id: str, only_mask: bool = False) -> Optional[TemplateInfo]:
        """
        加载某个模板到内存
        :param sub_dir: 子文件夹
        :param template_id: 模板id
        :param only_mask:
        :return: 模板图片
        """
        if not is_template_existed(sub_dir, template_id, need_raw=False):
            return None
        template: TemplateInfo = TemplateInfo(sub_dir, template_id)

        key = '%s:%s' % (sub_dir, template_id)
        self.template[key] = template
        return template

    def get_template(self, sub_dir: str, template_id: str) -> TemplateInfo:
        """
        获取某个模板 会存在内容
        :param sub_dir: 子文件夹
        :param template_id: 模板id
        :return: 模板图片
        """
        key = '%s:%s' % (sub_dir, template_id)
        if key in self.template:
            return self.template[key]

        now = time.monotonic()
        missing_until = self._missing_until.get(key)
        if missing_until is not None:
            if now < missing_until:
                return None
            del self._missing_until[key]  # 过期了，重新去磁盘确认一次

        template = self.load_template(sub_dir, template_id)
        if template is None:
            self._missing_until[key] = now + MISSING_TEMPLATE_CACHE_TTL
        return template

    def clear_missing_cache(self) -> None:
        """清空「模板不存在」的负缓存。

        开发工具新建/改名模板后调用，避免 TTL 内仍被当成不存在。
        """
        self._missing_until.clear()

    def get_template_mask(self, sub_dir: str, template_id: str) -> MatLike:
        """
        获取某个模板的掩码
        :param sub_dir: 子文件夹
        :param template_id: 模板id
        :return: 模板图片
        """
        key = '%s:%s' % (sub_dir, template_id)
        if key in self.template:
            return self.template[key].mask
        else:
            return self.load_template(sub_dir, template_id, only_mask=True).mask
