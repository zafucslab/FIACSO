import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取RGB图像
img_bgr = cv2.imread('D:\\Network model file\\code\\beauty\\3finish_content-aware-rotation-master\\GAMA\\img\\input\\test1.jpg')

# 转换为HSV图像
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# 显示结果
plt.subplot(121), plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)), plt.title('HSV')
plt.xticks([]), plt.yticks([])
plt.show()

