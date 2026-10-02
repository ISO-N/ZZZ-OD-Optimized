import cv2
from cv2.typing import MatLike

from one_dragon.base.debug.debug_trace_bus import DebugTraceBus, VisionTraceItem
from one_dragon.base.geometry.rectangle import Rect
from one_dragon.base.matcher.match_result import MatchResult, MatchResultList
from one_dragon.base.screen.template_info import TemplateInfo
from one_dragon.base.screen.template_loader import TemplateLoader
from one_dragon.utils import cv2_utils
from one_dragon.utils.log_utils import log


class TemplateMatcher:

    def __init__(
        self,
        template_loader: TemplateLoader,
        debug_trace_bus: DebugTraceBus | None = None,
    ) -> None:
        self.template_loader: TemplateLoader = template_loader
        self.debug_trace_bus: DebugTraceBus | None = debug_trace_bus

    def match_template(self, source: MatLike,
                       template_sub_dir: str,
                       template_id: str,
                       template_type: str = 'raw',
                       threshold: float = 0.5,
                       mask: MatLike | None = None,
                       ignore_template_mask: bool = False,
                       only_best: bool = True,
                       ignore_inf: bool = True) -> MatchResultList:
        """
        在原图中 匹配模板 如果模板图中有掩码图 会自动使用
        :param source: 原图
        :param template_sub_dir: 模板的子文件夹
        :param template_id: 模板id
        :param template_type: 模板类型
        :param threshold: 匹配阈值
        :param mask: 额外使用的掩码 与原模板掩码叠加
        :param ignore_template_mask: 是否忽略模板自身的掩码
        :param only_best: 只返回最好的结果
        :param ignore_inf: 是否忽略无限大的结果
        :return: 所有匹配结果
        """
        template: TemplateInfo = self.template_loader.get_template(template_sub_dir, template_id)
        if template is None:
            log.error(f'未加载模板 {template_id}')
            return MatchResultList()

        mask_usage = self._resolve_mask(template, mask, ignore_template_mask)
        result = cv2_utils.match_template(source, template.get_image(template_type), threshold, mask=mask_usage,
                                          only_best=only_best, ignore_inf=ignore_inf)
        self._emit_debug_vision(template_sub_dir, template_id, result)
        return result

    @staticmethod
    def _resolve_mask(
        template: TemplateInfo,
        mask: MatLike | None,
        ignore_template_mask: bool,
    ) -> MatLike | None:
        """算出本次匹配实际要用的掩码。

        模板掩码全 255 时整体按「无掩码」处理：``bitwise_or(全255, 任意) == 全255``，
        而全 255 掩码与不传掩码结果一致（见 ``TemplateInfo.mask_is_all_white``），
        传 mask 会让 ``cv2.matchTemplate`` 慢 4.0-5.5 倍。

        **但近似常量的模板除外**：那类模板让 ``TM_CCOEFF_NORMED`` 变成 0/0，
        不带掩码会返回全 1.0（到处都算匹配），必须继续带掩码走「匹配不到」的老路。
        见 ``TemplateInfo.is_low_contrast``。

        Args:
            template: 模板
            mask: 调用方额外传入的掩码
            ignore_template_mask: 是否忽略模板自带掩码

        Returns:
            实际传给 cv2 的掩码，None 表示不传
        """
        if (not ignore_template_mask
                and template.mask_is_all_white
                and not template.is_low_contrast):
            return None

        mask_usage: MatLike | None = None
        if not ignore_template_mask:
            mask_usage = template.mask
        if mask is not None:
            mask_usage = cv2.bitwise_or(mask_usage, mask) if mask_usage is not None else mask
        return mask_usage

    def match_one_by_feature(self, source: MatLike,
                             template_sub_dir: str,
                             template_id: str,
                             source_mask: MatLike | None = None,
                             knn_distance_percent: float = 0.7
                             ) -> MatchResult | None:
        """
        使用特征匹配找到模板的位置
        @param source:
        @param template_sub_dir:
        @param template_id:
        @param source_mask:
        @param knn_distance_percent: 越小要求匹配程度越高
        @return:
        """
        source_kps, source_desc = cv2_utils.feature_detect_and_compute(source, source_mask)
        template = self.template_loader.get_template(template_sub_dir, template_id)
        if template is None:
            return None
        template_kps, template_desc = template.features

        return cv2_utils.feature_match_for_one(
            source_kps, source_desc,
            template_kps, template_desc,
            template_width=template.raw.shape[1], template_height=template.raw.shape[0],
            source_mask=source_mask,
            knn_distance_percent=knn_distance_percent
        )

    def match_template_binary(self, source: MatLike,
                              template_sub_dir: str,
                              template_id: str,
                              threshold: float = 0.5,
                              binary_threshold: int = 127,
                              mask: MatLike | None = None,
                              ignore_template_mask: bool = False,
                              only_best: bool = True,
                              ignore_inf: bool = True,
                              source_already_binary: bool = False) -> MatchResultList:
        """
        使用二值化图像进行模板匹配
        :param source: 原图
        :param template_sub_dir: 模板的子文件夹
        :param template_id: 模板id
        :param threshold: 匹配阈值
        :param binary_threshold: 二值化阈值，默认为127
        :param mask: 额外使用的掩码 与原模板掩码叠加
        :param ignore_template_mask: 是否忽略模板自身的掩码
        :param only_best: 只返回最好的结果
        :param ignore_inf: 是否忽略无限大的结果
        :param source_already_binary: source 是否已经是二值化（单通道 0/255）结果，
            为 True 时不再重复二值化
        :return: 所有匹配结果
        """
        template: TemplateInfo = self.template_loader.get_template(template_sub_dir, template_id)
        if template is None:
            log.error(f'未加载模板 {template_id}')
            return MatchResultList()

        # 对原图和模板都进行二值化处理
        # source 已经是二值图时跳过：to_binary 对二值图是恒等变换（to_binary(to_binary(x)) == to_binary(x)），
        # 再来一遍纯属浪费一遍全图遍历。
        if source_already_binary:
            source_binary = source
        else:
            source_binary = cv2_utils.to_binary(source, threshold=binary_threshold)
        template_binary = cv2_utils.to_binary(template.raw, threshold=binary_threshold)

        # 处理掩码（全 255 的模板掩码等价于没有掩码，见 _resolve_mask）
        mask_usage = self._resolve_mask(template, mask, ignore_template_mask)

        # 使用二值化图像进行匹配
        result = cv2_utils.match_template(
            source_binary,
            template_binary,
            threshold,
            mask=mask_usage,
            only_best=only_best,
            ignore_inf=ignore_inf
        )
        self._emit_debug_vision(template_sub_dir, template_id, result)
        return result

    def crop_and_match_template(
            self,
            source: MatLike,
            rect: Rect,
            template_sub_dir: str,
            template_id: str,
            **kwargs,
    ) -> MatchResultList:
        """
        裁剪图片后进行模板匹配 自动处理 overlay 坐标偏移
        :param source: 原图
        :param rect: 裁剪区域
        :param template_sub_dir: 模板的子文件夹
        :param template_id: 模板id
        :param kwargs: 传递给 match_template 的额外参数
        """
        part = cv2_utils.crop_image_only(source, rect)
        bus = self.debug_trace_bus
        if bus is not None:
            parent_x, parent_y = bus.crop_offset
            bus.set_crop_offset(parent_x + rect.x1, parent_y + rect.y1)
        try:
            result = self.match_template(part, template_sub_dir, template_id, **kwargs)
        finally:
            if bus is not None:
                bus.reset_crop_offset()
        return result

    def crop_and_match_template_binary(
            self,
            source: MatLike,
            rect: Rect,
            template_sub_dir: str,
            template_id: str,
            binarize_after_crop: bool = False,
            **kwargs,
    ) -> MatchResultList:
        """
        裁剪图片后进行二值化模板匹配 自动处理 overlay 坐标偏移
        :param source: 原图
        :param rect: 裁剪区域
        :param template_sub_dir: 模板的子文件夹
        :param template_id: 模板id
        :param binarize_after_crop: 是否先裁剪再二值化。
            调用方若已自行把整张图二值化（并在 source 里传入二值图），保持 False；
            传 True 时本方法只对裁剪出来的小图做二值化，省掉一次整图遍历。
        :param kwargs: 传递给 match_template_binary 的额外参数
        """
        part = cv2_utils.crop_image_only(source, rect)
        bus = self.debug_trace_bus
        if bus is not None:
            parent_x, parent_y = bus.crop_offset
            bus.set_crop_offset(parent_x + rect.x1, parent_y + rect.y1)
        try:
            if binarize_after_crop:
                part = cv2_utils.to_binary(
                    part, threshold=kwargs.get('binary_threshold', 127)
                )
                kwargs['source_already_binary'] = True
            result = self.match_template_binary(part, template_sub_dir, template_id, **kwargs)
        finally:
            if bus is not None:
                bus.reset_crop_offset()
        return result

    def _emit_debug_vision(
        self,
        template_sub_dir: str,
        template_id: str,
        result: MatchResultList,
    ) -> None:
        bus = self.debug_trace_bus
        if bus is None or not bus.enabled or result is None or len(result.arr) == 0:
            return

        for match in result.arr[:20]:
            bus.add_vision(
                VisionTraceItem(
                    source="template",
                    label=f"{template_sub_dir}/{template_id}",
                    x1=match.x,
                    y1=match.y,
                    x2=match.x + match.w,
                    y2=match.y + match.h,
                    score=match.confidence,
                )
            )
