# import cv2
# import numpy as np
# from typing import Tuple, Dict, Any, Optional
#
#
# def find_template_location(
#         target_img_path: str,
#         template_img_path: str,
#         threshold: float = 0.8
# ) -> Optional[Dict[str, Any]]:
#     """
#     在目标图片中查找模板图片的位置
#
#     :param target_img_path: 大图（背景图）的路径
#     :param template_img_path: 小图（要寻找的模板）的路径
#     :param threshold: 匹配阈值 (0.0 到 1.0)，越高越严格。默认 0.8 表示 80% 相似度
#     :return: 找到则返回包含坐标和置信度的字典，未找到返回 None
#     """
#     # 1. 读入大图和模板图（用灰度模式读入，提高匹配速度和准确率）
#     img = cv2.imread(target_img_path)
#     if img is None:
#         raise FileNotFoundError(f"找不到大图: {target_img_path}")
#
#     template = cv2.imread(template_img_path)
#     if template is None:
#         raise FileNotFoundError(f"找不到模板图: {template_img_path}")
#
#     # 转为灰度图
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#
#     # 2. 获取模板图的宽和高
#     # 还记得我们之前学的 [::-1] 吗？如果是灰度图，shape 只有 (高, 宽)，反转后 w, h 对号入座
#     w, h = template_gray.shape[::-1]
#
#     # 3. 执行模板匹配
#     # TM_CCOEFF_NORMED 是最常用的标准相关系数匹配法，结果在 0 到 1 之间
#     result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
#
#     # 4. 获取匹配结果中最大值（最佳匹配）的位置和分值
#     # min_val, max_val: 最小/最大匹配度
#     # min_loc, max_loc: 最小/最大匹配度对应的左上角坐标 (x, y)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#
#     # 5. 判断最佳匹配度是否达到了我们的期望值（阈值）
#     if max_val >= threshold:
#         top_left = max_loc
#         # 计算右下角坐标
#         bottom_right = (top_left[0] + w, top_left[1] + h)
#         # 计算中心点坐标（如果你需要控制鼠标去点击，中心点最实用）
#         center = (top_left[0] + w // 2, top_left[1] + h // 2)
#
#         return {
#             "top_left": top_left,  # (x, y)
#             "bottom_right": bottom_right,  # (x, y)
#             "center": center,  # (x, y)
#             "confidence": round(max_val, 4)  # 置信度，比如 0.9856
#         }
#
#     # 如果低于阈值，说明没找到
#     return None
#
#
# print(find_template_location(target_img_path="./assets/test.jpg", template_img_path="./assets/sub.png", threshold=0.5))

import cv2
import numpy as np
from numpy.ma.extras import median

# test0
#image = cv2.imread('./assets/opencv_logo.jpg')
# print(image.shape)
# cv2.imshow('image', image)
# cv2.waitKey(0)

# test1
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray', gray)
#
# cv2.waitKey(0)
# test2
# crop = image[10:170,40:200]
# cv2.imshow('image', crop)
# cv2.waitKey(0)
# test3
# image = np.zeros((300, 300, 3), np.uint8)
# cv2.line(image, (100, 200), (250, 250), (255, 0, 0), 2)
# cv2.rectangle(image,(30,100),(60,150),(0,255,0),2)
# cv2.circle(image,(150,100),20,(0,0,255),3)
# cv2.putText(image,"你好",(100,50),0,1,(255,255,255),2,1)
# cv2.imshow('image', image)
# cv2.waitKey(0)
#test4

# image = cv2.imread("assets/plane.jpg")
#
# gauss = cv2.GaussianBlur(image, (5, 5), 0)
# median = cv2.medianBlur(gauss, 5)
# cv2.imshow("gauss", gauss)
# cv2.imshow("median", median)
# cv2.waitKey(0)

#test5
# image = cv2.imread('assets/opencv_logo.jpg')
# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#
# corners = cv2.goodFeaturesToTrack(gray,500,0.01,10)
#
# for corner in corners:
#     x, y = corner.ravel()
#     cv2.circle(image,(int(x),int(y)),3,(255,0,255),2)
#
# cv2.imshow('image',image)
# cv2.waitKey(0)

#test6

# import cv2
# import numpy
#
# image =cv2.imread("assets/poker.jpg")
# gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#
# template = gray[75:105,235:265]
#
# match =cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
#
# locations = numpy.where(match >= 0.8)
#
# w,h=match.shape[0:2]
# for p in zip(*locations[::-1]):
#     x1,y1=p[0],p[1]
#     x2,y2=x1+w,y1+h
#     cv2.rectangle(image,(x1,y1),(x2,y2),(255,255,255),2)
#
# cv2.imshow("image", image)
# cv2.waitKey(0)

#test7
# import cv2
# from numpy.random import laplace
#
# gray = cv2.imread("assets/opencv_logo.jpg",cv2.IMREAD_GRAYSCALE)
#
# cv2.imshow("gray",gray)
# canny = cv2.Canny(gray,100,200)
# cv2.imshow("lalacian",canny)
#
#
# cv2.waitKey(0)

# test8

# import cv2
#
# gray = cv2.imread("assets/bookpage.jpg", cv2.IMREAD_GRAYSCALE)
# ret,binary = cv2.threshold(gray,10,255,cv2.THRESH_BINARY)
# binary_adaptive = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
# ret1,binary_otsu = cv2.threshold(binary_adaptive,10,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#
# cv2.imshow("binary", binary_otsu)
# cv2.waitKey()

import cv2

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key != -1:
        break

capture.release()


