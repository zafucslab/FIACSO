

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def canny_edge_detection(image, sigma=0.5, low_threshold=30, high_threshold=150):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), sigma)
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    return edges

# Load the two images
image1 = cv2.imread('C:\\Users\\CuiCui\\Desktop\\zx3.jpg')
image2 = cv2.imread('C:\\Users\\CuiCui\\Desktop\\zx3ok.png')

# Apply Canny edge detection to both images
edges1 = canny_edge_detection(image1)
edges2 = canny_edge_detection(image2)

# Calculate SSIM between the two edge images
ssim_score, diff_image = ssim(edges1, edges2, full=True)

# Calculate the average difference in edge images
edge_diff_avg = np.mean(diff_image)

# Compute the final similarity analysis result
l = 1  # Brightness similarity weight
c = 1  # Contrast similarity weight
s = ssim_score  # Structural similarity
e = edge_diff_avg  # Average difference in edge images

similarity = l * c * ((s + e) / 2)

print("Similarity score:", similarity)

# Display the original images and edge images for visualization
cv2.imshow("Image 1", image1)
cv2.imshow("Image 2", image2)
cv2.imshow("Edges 1", edges1)
cv2.imshow("Edges 2", edges2)

cv2.waitKey(0)
cv2.destroyAllWindows()
