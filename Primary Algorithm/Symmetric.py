import cv2
import numpy as np

def calculate_distance_to_line(point, line_point1, line_point2):
    # 计算点到直线的欧几里得距离
    x0, y0 = point
    x1, y1 = line_point1
    x2, y2 = line_point2
    distance = np.abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    return distance

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

# 图像的水平和垂直中心线
height, width = image.shape
center_lines = [
    ((width // 2, 0), (width // 2, height)),  # 垂直中心线
    ((0, height // 2), (width, height // 2))  # 水平中心线
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

# 判断语义线是否与水平或垂直中心线重合，并计算距离
on_center_line = False
min_distance = float('inf')
for center_line in center_lines:
    distance1 = calculate_distance_to_line(semantic_line_points[0], center_line[0], center_line[1])
    distance2 = calculate_distance_to_line(semantic_line_points[1], center_line[0], center_line[1])
    distance = min(distance1, distance2)
    if distance < min_distance:
        min_distance = distance
    if distance == 0:
        on_center_line = True
        break

if on_center_line:
    print("语义线与中心线之一重合")
else:
    print("语义线与中心线不重合")
    print("语义线与最近中心线之间的距离:", min_distance)

# 可视化结果
if best_line is not None:
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

resized_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("result.jpg", resized_image)
