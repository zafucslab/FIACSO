# 这段代码是用于检测图像中的垂直直线。它使用了OpenCV库进行图像处理和霍夫直线变换。
# 首先，通过cv2.imread()函数读取指定路径下的图像，并将其转换为灰度图像。然后，使用cv2.Canny()函数进行边缘检测，将图像中的边缘提取出来。
# 接下来，使用cv2.HoughLines()函数进行霍夫直线变换，检测图像中的直线。参数1表示输入图像，参数2表示距离分辨率（即像素距离的精确度），参数3表示角度分辨率（即角度的精确度），参数4表示阈值，用于过滤直线。
# 然后，遍历检测到的直线，判断其角度是否在垂直线的范围内。如果是垂直线，则使用cv2.line()函数在原图像上绘制红色的直线。
# 最后，使用cv2.imshow()函数显示带有垂直直线的结果图像，并使用cv2.waitKey()和cv2.destroyAllWindows()函数来控制图像显示的交互操作。
# 你可以将以上代码保存为.py文件，并替换"image.jpg"为你想要检测的图像路径，运行代码即可进行垂直直线检测。


import cv2
import numpy as np


# 加载原始图像
image = cv2.imread('1.png', 2)

# 边缘检测
edges = cv2.Canny(image, 10, 150)

# 二值化
ret, threshold = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)

# 霍夫变换
lines = cv2.HoughLines(threshold, 1, np.pi/180, 150)

# 如果没有检测到直线，则退出或进行其他处理
if lines is None:
    print("No lines detected.")
    exit()

# 检测到的直线按长度排序
lines = sorted(lines, key=lambda x: x[0][0], reverse=True)

# 计算直线两侧区域的平均梯度的比值
best_line = None
max_gradient_ratio = 0

for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho

    # 计算直线两侧区域的平均梯度
    left_region = threshold[:, :int(x0)]
    right_region = threshold[:, int(x0):]

    gradient_ratio = np.mean(left_region) / np.mean(right_region)

    # 更新最佳分隔线
    if gradient_ratio > max_gradient_ratio:
        max_gradient_ratio = gradient_ratio
        best_line = line

# 在原始图像上绘制最佳分隔线
if best_line is not None:
    rho, theta = best_line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 计算夹角度数
angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi

# 将结果写入txt文件
with open('angle.txt', 'w') as f:
    f.write(str(angle))


# 缩小图片尺寸
resized_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

# 显示结果
cv2.imshow('Resized Image', resized_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

# 将处理后的图像保存到本地
cv2.imwrite("result.jpg", resized_image)
# # 显示结果
# cv2.imshow('Original Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# # 显示结果
# cv2.imshow('Original Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()