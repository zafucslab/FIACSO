from seam_carving import SeamCarver
import numpy as np
import cv2
import os
def image_resize_without_mask(filename_input, filename_output, new_height, new_width):
    obj = SeamCarver(filename_input, new_height, new_width)
    obj.save_result(filename_output)


def image_resize_with_mask(filename_input, filename_output, new_height, new_width, filename_mask):
    obj = SeamCarver(filename_input, new_height, new_width, protect_mask=filename_mask)
    obj.save_result(filename_output)


def object_removal(filename_input, filename_output, filename_mask):
    obj = SeamCarver(filename_input, 0, 0, object_mask=filename_mask)
    obj.save_result(filename_output)

if __name__ == '__main__':
    """
    Put image in in/images folder and protect or object mask in in/masks folder
    Ouput image will be saved to out/images folder with filename_output
    """


    filename_input = "C:\\Users\\CuiCui\\Desktop\\sp2.png"
    filename_output = "C:\\Users\\CuiCui\\Desktop\\sp2_1.png"
    new_width = 648
    new_height = 155

    # # 提供保护蒙版图像的文件名
    # filename_mask = "D:\\Network model file\\code\\beauty\\4finish_seam-carving-master\\4_ok_seam-carving-master\\seam-carving-master\\example\\mask2.png"


    # image_resize_without_mask(input_image, output_image, new_height, new_width)
    image_resize_without_mask(filename_input, filename_output, new_height, new_width)
    # object_removal(filename_input, filename_output, filename_mask)








