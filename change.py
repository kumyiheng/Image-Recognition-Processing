import cv2
from bg import rembg
import numpy as np
def change_bg(alt_imgmsg, imgmsg):
    imgFront = cv2.imread(f'bg_{alt_imgmsg}.png')
    imgBack = cv2.imread(f'{imgmsg}.jpg')

    height, width = imgFront.shape[:2]
    resizeBack = cv2.resize(imgBack, (width, height), interpolation = cv2.INTER_CUBIC)

    for i in range(width):
        for j in range(height):
            pixel = imgFront[j, i]
            if np.all(pixel == [0, 0, 0]):
                imgFront[j, i] = resizeBack[j, i]

    cv2.imwrite(f"ch_{imgmsg}.jpg", imgFront)