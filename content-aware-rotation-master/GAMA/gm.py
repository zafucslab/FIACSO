import cv2
import numpy as np
import math
import os


def gamma_trans(img, gamma):  # gamma函数处理
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立映射表
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 颜色值为整数
    return cv2.LUT(img, gamma_table)  # 图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。

def nothing(x):
    pass

data_base_dir = 'D:\\Network model file\\code\\beauty\\3finish_content-aware-rotation-master\\GAMA\\img\\input'  # 输入文件夹的路径
outfile_dir = 'D:\\Network model file\\code\\beauty\\3finish_content-aware-rotation-master\\GAMA\\img\\output'  # 输出文件夹的路径

list = os.listdir(data_base_dir)
list.sort()
list2 = os.listdir(outfile_dir)
list2.sort()
for file in list:  # 遍历目标文件夹图片
    read_img_name = data_base_dir + '/' + file.strip()  # 取图片完整路径
    image = cv2.imread(read_img_name)  # 读入图片
    img_gray = cv2.imread(read_img_name, 0)  # 灰度图读取，用于计算gamma值

    mean = np.mean(img_gray)
    gamma_val = math.log10(0.5) / math.log10(mean / 255)  # 公式计算gamma

    image_gamma_correct = gamma_trans(image, gamma_val)  # gamma变换

    out_img_name = outfile_dir + '/' + file.strip()
    cv2.imwrite(out_img_name, image_gamma_correct)
    print("The photo which is processed is {}".format(file))

