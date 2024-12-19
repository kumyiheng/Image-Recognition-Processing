#import cv2
#from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

def rembg(imgmsg):
    os.system(f'backgroundremover -i "{imgmsg}.jpg"  -o "bg_{imgmsg}.png"')
    '''
    segmentor = SelfiSegmentation()
    img = cv2.imread(f'{imgmsg}.jpg')
    img_Out = segmentor.removeBG(img, (255, 255, 255))
    cv2.imwrite(f'bg_{imgmsg}.png', img_Out)
    '''

