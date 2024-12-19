import cv2
import numpy as np

def edge(imgmsg):
    # 讀取圖像
    image = cv2.imread(f'{imgmsg}.jpg')

    # 將圖像轉換為灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 進行閾值處理，將圖像轉為二值圖像 輪廓檢測通常在灰度圖像上進行
    ret, threshold = cv2.threshold(gray, 127, 255, 0)

    # 找到輪廓
    contours_1, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #調閥值
    contours_2 = cv2.Canny(threshold, 50, 150) #要調閥值

    cv2.drawContours(image, contours_1, -1, (255, 0, 0), 2)  # -1 表示繪製所有的輪廓(可以定範圍) 、 (0,0,0) 顏色 、 2是厚薄 
    # 顯示原始圖像和繪製輪廓的圖像
    #cv2.imshow('result Image_2', contours_2)
    #cv2.imshow('result Image', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imwrite(f'edge_{imgmsg}.jpg', image)
    cv2.imwrite(f'edge_{imgmsg}.jpg', contours_2)