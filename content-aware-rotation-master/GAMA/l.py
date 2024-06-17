import cv2
import numpy as np


def Adaptive_light_correction(img):
    height = img.shape[0]
    width = img.shape[1]

    HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    V = HSV_img[:,:,2]

    kernel_size = min(height, width)
    if kernel_size % 2 == 0:
        kernel_size -= 1

    SIGMA1 = 15
    SIGMA2 = 80
    SIGMA3 = 250
    q = np.sqrt(2.0)
    F = np.zeros((height,width,3),dtype=np.float64)
    F[:,:,0] = cv2.GaussianBlur(V,(kernel_size, kernel_size),SIGMA1 / q)
    F[:,:,1] = cv2.GaussianBlur(V,(kernel_size, kernel_size),SIGMA2 / q)
    F[:,:,2] = cv2.GaussianBlur(V,(kernel_size, kernel_size),SIGMA3 / q)
    F_mean = np.mean(F,axis=2)
    average = np.mean(F_mean)
    gamma = np.power(0.5,np.divide(np.subtract(average,F_mean),average))
    out = np.power(V / 255.0, gamma) * 255.0
    HSV_img[:,:,2] = out
    img = cv2.cvtColor(HSV_img,cv2.COLOR_HSV2BGR)
    return img


if __name__ == '__main__':
    img = cv2.imread("C:\\Users\\CuiCui\\Desktop\\2yx.png")
    result_img = Adaptive_light_correction(img)
    cv2.imshow("result_img",result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
