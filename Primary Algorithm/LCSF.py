import cv2
import numpy as np

# 读取图像
image = cv2.imread("D:\\Network model file\\code\\swin_transformer\\metest\\me\\input1.png")

# 使用高斯滤波器进行图像滤波处理
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
lab_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2Lab)

# 提取亮度通道
l_channel = lab_image[:,:,0]

# 尝试不同的阈值进行亮度通道的阈值分割
threshold_values = [100, 120, 140]  # 可以根据需要添加更多的阈值值

for threshold_value in threshold_values:
    _, thresholded = cv2.threshold(l_channel, threshold_value, 255, cv2.THRESH_BINARY)

    # 尝试不同大小和形状的结构元素进行形态学操作
    kernel_sizes = [(3, 3), (5, 5), (7, 7)]  # 可以根据需要添加更多的结构元素大小

    for kernel_size in kernel_sizes:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
        closed = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

        # 计算显著性特征
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 计算每个轮廓的面积，并根据面积降序排序
        areas = [cv2.contourArea(c) for c in contours]
        sorted_contours = sorted(zip(contours, areas), key=lambda x: x[1], reverse=True)
        max_contour, max_area = sorted_contours[0]

        # 创建一个与输入图像大小相同的空白掩模
        mask = np.zeros_like(l_channel)

        # 在掩模上绘制最大的显著性特征
        cv2.drawContours(mask, [max_contour], -1, 255, -1)

        # 将显著性图输出为文件
        cv2.imwrite("temp_output_mask.png", mask)

        # 读取临时生成的显著性图像
        salient_image = cv2.imread("temp_output_mask.png")

        # 使用GrabCut算法进行图像分割
        mask_gc = np.zeros(image.shape[:2], np.uint8)
        bgdModel_gc = np.zeros((1, 65), np.float64)
        fgdModel_gc = np.zeros((1, 65), np.float64)
        rect = (50, 50, image.shape[1]-50, image.shape[0]-50)  # 初始矩形区域
        cv2.grabCut(image, mask_gc, rect, bgdModel_gc, fgdModel_gc, 5, cv2.GC_INIT_WITH_RECT)

        # 根据GrabCut算法的结果提取前景
        mask2 = np.where((mask_gc==2) | (mask_gc==0), 0, 255).astype('uint8')

        # 将提取的前景与原始图像相乘得到显著性图像
        final_salient_image = cv2.bitwise_and(salient_image, salient_image, mask=mask2)

        # 保存显著性图像
        cv2.imwrite("final_salient_image_threshold_{}_kernel_{}.png".format(threshold_value, kernel_size), final_salient_image)
