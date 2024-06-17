import cv2
import numpy as np

def calculate_distance(point1, point2):
    # 计算两个点之间的距离
    distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance

def calculate_score(distance, max_distance):
    # 根据距离计算得分（范围在0-1之间）
    score = 1 - distance / max_distance
    score = max(0, min(score, 1))
    return score

# 加载图像
image = cv2.imread("dc3y.png", 0)  # 读取灰度图像
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)  # 二值化图像

# 寻找白色区域的轮廓
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 计算白色区域的中心位置
if len(contours) > 0:
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    cx = int(M["m10"] / M["m00"])  # 中心点x坐标
    cy = int(M["m01"] / M["m00"])  # 中心点y坐标

    # 计算图像中线的交叉点
    height, width = image.shape
    cross_point1 = (width // 2, cy)
    cross_point2 = (cx, height // 2)

    # 计算中心位置与交叉点的距离
    distance = calculate_distance((cx, cy), cross_point1)

    # 计算得分
    max_distance = np.sqrt((width // 2) ** 2 + (height // 2) ** 2)
    score = calculate_score(distance, max_distance)

    print("中心点位置:", (cx, cy))
    print("距离中线的距离:", distance)
    print("得分:", score)
