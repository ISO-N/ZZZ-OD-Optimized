from typing import Tuple

import cv2
import numpy as np
from cv2.typing import MatLike


def scale_input_image_u(image: MatLike, onnx_input_width: int, onnx_input_height: int) -> Tuple[np.ndarray, int, int]:
    """
    按照 ultralytics 的方式，将图片缩放至模型使用的大小
    参考 https://github.com/orgs/ultralytics/discussions/6994?sort=new#discussioncomment-8382661
    :param image: 输入的图片 RBG通道
    :param onnx_input_width: 模型需要的图片宽度
    :param onnx_input_height: 模型需要的图片高度
    :return: 缩放后的图片 RGB通道
    """
    img_height, img_width = image.shape[:2]

    # 将图像缩放到模型的输入尺寸中较短的一边
    min_scale = min(onnx_input_height / img_height, onnx_input_width / img_width)

    # 未进行padding之前的尺寸
    scale_height = int(round(img_height * min_scale))
    scale_width = int(round(img_width * min_scale))

    # 缩放到目标尺寸
    if onnx_input_height != img_height or onnx_input_width != img_width:  # 需要缩放
        input_img = np.full(shape=(onnx_input_height, onnx_input_width, 3),
                            fill_value=114, dtype=np.uint8)
        scale_img = cv2.resize(image, (scale_width, scale_height), interpolation=cv2.INTER_LINEAR)
        input_img[0:scale_height, 0:scale_width, :] = scale_img
    else:
        input_img = image

    # 缩放后最后的处理
    # 先转置再 astype(float32)，最后在新数组上原地归一化。
    # 原来的 `input_img / 255.0` 会让 numpy 先分配一份 float64 中间体
    # （640x640x3 时约 9.8MB）再做一次 float32 拷贝；这里只保留必要的一次拷贝，
    # 且原地乘不会碰到调用方传入的 image（astype 一定返回新数组）。
    # 数值与旧实现一致，见 .dsh/performance-benchmark/verify/v02_yolo_preprocess.py。
    input_img = input_img.transpose(2, 0, 1).astype(np.float32)
    input_img *= np.float32(1.0 / 255.0)
    input_tensor = np.ascontiguousarray(input_img)[np.newaxis, :, :, :]

    return input_tensor, scale_height, scale_width
