import time
from pathlib import Path
from typing import Optional, Dict, Any

import flet as ft
import cv2
from yolo_flet import YoloFlet,types
import logging



logging.getLogger().setLevel(logging.INFO)
log=logging.getLogger("yolo_flet")
default_assets_dir = Path(__file__).parent / "assets"
fp = default_assets_dir / "yolo26n_int8.tflite"
print(fp)
log.info("python debug path " + str(fp))

def find_template_location(
        target_img_path: str,
        template_img_path: str,
        threshold: float = 0.8
) -> Optional[Dict[str, Any]]:
    """
    在目标图片中查找模板图片的位置

    :param target_img_path: 大图（背景图）的路径
    :param template_img_path: 小图（要寻找的模板）的路径
    :param threshold: 匹配阈值 (0.0 到 1.0)，越高越严格。默认 0.8 表示 80% 相似度
    :return: 找到则返回包含坐标和置信度的字典，未找到返回 None
    """
    # 1. 读入大图和模板图（用灰度模式读入，提高匹配速度和准确率）
    img = cv2.imread(target_img_path)
    if img is None:
        raise FileNotFoundError(f"找不到大图: {target_img_path}")

    template = cv2.imread(template_img_path)
    if template is None:
        raise FileNotFoundError(f"找不到模板图: {template_img_path}")

    # 转为灰度图
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 2. 获取模板图的宽和高
    # 还记得我们之前学的 [::-1] 吗？如果是灰度图，shape 只有 (高, 宽)，反转后 w, h 对号入座
    w, h = template_gray.shape[::-1]

    # 3. 执行模板匹配
    # TM_CCOEFF_NORMED 是最常用的标准相关系数匹配法，结果在 0 到 1 之间
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # 4. 获取匹配结果中最大值（最佳匹配）的位置和分值
    # min_val, max_val: 最小/最大匹配度
    # min_loc, max_loc: 最小/最大匹配度对应的左上角坐标 (x, y)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 5. 判断最佳匹配度是否达到了我们的期望值（阈值）
    if max_val >= threshold:
        top_left = max_loc
        # 计算右下角坐标
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # 计算中心点坐标（如果你需要控制鼠标去点击，中心点最实用）
        center = (top_left[0] + w // 2, top_left[1] + h // 2)

        return {
            "top_left": top_left,  # (x, y)
            "bottom_right": bottom_right,  # (x, y)
            "center": center,  # (x, y)
            "confidence": round(max_val, 4)  # 置信度，比如 0.9856
        }

    # 如果低于阈值，说明没找到
    return None






async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    try:
        log.info("创建模型类",)
        yolo_flet = YoloFlet(src=str(fp))
    except RuntimeError as e:
        log.info(f"加载模型失败{e}",)
        log.error(e)
        return

    async def detect() :
        log.debug("/。。。。。。。。。。开始识别中。。。。。。。。。。")
        log.info(f"{find_template_location(target_img_path="./assets/test.jpg", template_img_path="./assets/sub.png", threshold=0.5)}")


        with open("./assets/test.jpg", "rb") as f:

            image_bytes = f.read()
            for i in range(1000):
                start = time.time()
                a:list[types.DetectionResult] =await  yolo_flet.detect(image_bytes)
                end = time.time()
                text.value = str((end - start) * 1000)+ f"这是第{i}次推理"
                log.debug("耗时"+str((end - start) * 1000))
                text.update()
                # for i in a:
                #     log.debug(i)



    bt =ft.Button(content="start detect" , on_click=detect)
    text =ft.Text(value="aaa")
    page.add(
        bt,text
    )


ft.run(main, assets_dir="assets")
