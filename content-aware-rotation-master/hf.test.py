import cv2

# 加载原始图像
image = cv2.imread('2.png', 1)

# 边缘检测
edges = cv2.Canny(image, 10, 40)

# 显示原始图像和边缘检测结果
cv2.imshow('Original Image', image)
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
