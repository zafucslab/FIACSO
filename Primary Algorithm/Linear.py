import cv2
import numpy as np

def calculate_distance(point1, point2):
    # 计算两个点之间的欧几里得距离
    distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance

def find_nearest_line(point, lines):
    # 找到距离点最近的直线
    min_distance = float('inf')
    nearest_line = None
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        distance = np.abs(a * point[0] + b * point[1] - rho) / np.sqrt(a**2 + b**2)
        if distance < min_distance:
            min_distance = distance
            nearest_line = line
    return nearest_line, min_distance

# 加载图像并进行预处理
image = cv2.imread('1.png', 2)
edges = cv2.Canny(image, 10, 150)
ret, threshold = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)

# 使用霍夫变换检测直线
lines = cv2.HoughLines(threshold, 1, np.pi/180, 150)

if lines is None:
    print("No lines detected.")
    exit()

# 检测到的直线按长度排序
lines = sorted(lines, key=lambda x: x[0][0], reverse=True)

# 找到最佳分隔线
best_line = lines[0]

# 图像的四根三分线
height, width = image.shape
third_lines = [
    ((width // 3, 0), (width // 3, height)),  # 左竖线
    ((2 * width // 3, 0), (2 * width // 3, height)),  # 右竖线
    ((0, height // 3), (width, height // 3)),  # 上横线
    ((0, 2 * height // 3), (width, 2 * height // 3))  # 下横线
]

# 计算语义线的两个端点
rho, theta = best_line[0]
a = np.cos(theta)
b = np.sin(theta)
x0 = a * rho
y0 = b * rho
x1 = int(x0 + 1000 * (-b))
y1 = int(y0 + 1000 * (a))
x2 = int(x0 - 1000 * (-b))
y2 = int(y0 - 1000 * (a))
semantic_line_points = [(x1, y1), (x2, y2)]

# 判断语义线是否与四根三分线之一重合，并计算距离
on_third_line = False
min_distance = float('inf')
for third_line in third_lines:
    distance1 = calculate_distance(semantic_line_points[0], third_line[0]) + calculate_distance(semantic_line_points[1], third_line[1])
    distance2 = calculate_distance(semantic_line_points[0], third_line[1]) + calculate_distance(semantic_line_points[1], third_line[0])
    distance = min(distance1, distance2)
    if distance < min_distance:
        min_distance = distance
    if distance == 0:
        on_third_line = True
        break

if on_third_line:
    print("语义线与三分线之一重合")
else:
    print("语义线与三分线不重合")
    print("语义线与最近三分线之间的距离:", min_distance)

# 可视化结果
if best_line is not None:
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

resized_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("result.jpg", resized_image)
