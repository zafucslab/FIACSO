
import cv2
import numpy as np

def calculate_distance(image, point):
    # 计算中心位置与指定点的距离
    height, width = image.shape
    cx = width // 2
    cy = height // 2
    distance = np.sqrt((cx - point[0]) ** 2 + (cy - point[1]) ** 2)
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

    # 计算中心位置与三分法四个点的距离
    height, width = image.shape
    third_points = [(width // 3, height // 3), (width * 2 // 3, height // 3),
                    (width // 3, height * 2 // 3), (width * 2 // 3, height * 2 // 3)]
    distances = [calculate_distance(image, point) for point in third_points]

    # 找到最小距离对应的点
    min_distance_index = np.argmin(distances)
    nearest_point = third_points[min_distance_index]
    min_distance = distances[min_distance_index]

    # 计算得分
    max_distance = np.sqrt((width // 2) ** 2 + (height // 2) ** 2)
    score = calculate_score(min_distance, max_distance)

    print("最近的点:", nearest_point)
    print("距离最近点的距离:", min_distance)
    print("得分:", score)
