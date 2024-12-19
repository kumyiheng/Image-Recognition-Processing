import cv2
import numpy as np
from IPython.display import clear_output
import math
from scipy.interpolate import UnivariateSpline
from PIL import Image

from sketch import sketch

def filter(imgmsg, choose):
    img=cv2.imread(f'{imgmsg}')
    #img = Image.open(f'{imgmsg}.jpg')
    #img = f'{imgmsg}.jpg'
    def LookupTable(x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))

    def cartoon(img):
    #inbuilt function to create sketch effect in colour and greyscale
        img1=cv2.stylization(img,sigma_s=3,sigma_r=0.2)
        return  img1

    def pencil_sketch_col(img):
    #inbuilt function to create sketch effect in colour and greyscale
        sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.06, shade_factor=0.06)
        return  sk_color

    def sepia(img):
        img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
        img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],[0.349, 0.686, 0.168],[0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
        img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
        img_sepia = np.array(img_sepia, dtype=np.uint8)
        return img_sepia

    def Summer(img):
        increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel,red_channel  = cv2.split(img)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        sum= cv2.merge((blue_channel, green_channel, red_channel ))
        return sum

    def Winter(img):
        increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel,red_channel = cv2.split(img)
        red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        win= cv2.merge((blue_channel, green_channel, red_channel))
        return win

    def gray(img):
        imgout = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return imgout

    def modify_lightness_saturation(img, lightness=0, saturation=300):
        
        origin_img = img

        # 圖像歸一化，且轉換為浮點型
        fImg = img.astype(np.float32)
        fImg = fImg / 255.0
        
        # 顏色空間轉換 BGR -> HLS
        hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
        hlsCopy = np.copy(hlsImg)

    #     lightness = 0 # lightness 調整為  "1 +/- 幾 %"
    #     saturation = 300 # saturation 調整為 "1 +/- 幾 %"
    
        # 亮度調整
        hlsCopy[:, :, 1] = (1 + lightness / 100.0) * hlsCopy[:, :, 1]
        hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1  # 應該要介於 0~1，計算出來超過1 = 1

        # 飽和度調整
        hlsCopy[:, :, 2] = (1 + saturation / 100.0) * hlsCopy[:, :, 2]
        hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1  # 應該要介於 0~1，計算出來超過1 = 1
        
        # 顏色空間反轉換 HLS -> BGR 
        result_img = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
        result_img = ((result_img * 255).astype(np.uint8))

        return result_img
    
    def modify_color_temperature(img, cold_rate=20):
        
        # ---------------- 冷色調 ---------------- #  
        
    #     height = img.shape[0]
    #     width = img.shape[1]
    #     dst = np.zeros(img.shape, img.dtype)

        # 1.計算三個通道的平均值，並依照平均值調整色調
        imgB = img[:, :, 0] 
        imgG = img[:, :, 1]
        imgR = img[:, :, 2] 

        # 調整色調請調整這邊~~ 
        # 白平衡 -> 三個值變化相同
        # 冷色調(增加b分量) -> 除了b之外都增加
        # 暖色調(增加r分量) -> 除了r之外都增加
        bAve = cv2.mean(imgB)[0] 
        gAve = cv2.mean(imgG)[0] + cold_rate
        rAve = cv2.mean(imgR)[0] + cold_rate
        aveGray = (int)(bAve + gAve + rAve) / 3

        # 2. 計算各通道增益係數，並使用此係數計算結果
        bCoef = aveGray / bAve
        gCoef = aveGray / gAve
        rCoef = aveGray / rAve
        imgB = np.floor((imgB * bCoef))  # 向下取整
        imgG = np.floor((imgG * gCoef))
        imgR = np.floor((imgR * rCoef))

        # 將原文第3部分的演算法做修改版，加快速度
        imgb = imgB
        imgb[imgb > 255] = 255
        
        imgg = imgG
        imgg[imgg > 255] = 255
        
        imgr = imgR
        imgr[imgr > 255] = 255
            
        cold_rgb = np.dstack((imgb, imgg, imgr)).astype(np.uint8) 
                
        return cold_rgb
    
    def gaussian_noise(img, mean=0, sigma=0.1):
        
        # int -> float (標準化)
        img = img / 255.0
        # 隨機生成高斯 noise (float + float)
        noise = np.random.normal(mean, sigma, img.shape)
        # noise + 原圖
        gaussian_out = img + noise
        # 所有值必須介於 0~1 之間，超過1 = 1，小於0 = 0
        gaussian_out = np.clip(gaussian_out, 0, 1)
        
        # 原圖: float -> int (0~1 -> 0~255)
        gaussian_out = np.uint8(gaussian_out*255)
        # noise: float -> int (0~1 -> 0~255)
        noise = np.uint8(noise*255)

        return gaussian_out
    
    def modify_contrast_and_brightness(img, brightness=0 , contrast=-100):
        # 上面做法的問題：有做到對比增強，白的的確更白了。
        # 但沒有實現「黑的更黑」的效果

        B = brightness / 255.0
        c = contrast / 255.0 
        k = math.tan((45 + 44 * c) / 180 * math.pi)

        img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
        
        # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
        img = np.clip(img, 0, 255).astype(np.uint8)

        return img
        
    def reduce_highlights(img, light_threshold=200):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 先轉成灰階處理
        ret, thresh = cv2.threshold(img_gray, light_threshold, 255, 0)  # 利用 threshold 過濾出高光的部分，目前設定高於 200 即為高光
        contours, hierarchy  = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        highlight_mask = np.zeros(img.shape, dtype=np.uint8) 
        
    #     print(len(contours))

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour) 
            highlight_mask[y:y+h, x:x+w] = 255 

    #     print("Highlight part: ")
    #     show_img(highlight_mask)
        
        # alpha，beta 共同決定高光消除後的模糊程度
        # alpha: 亮度的缩放因子，默認是 0.2， 範圍[0, 2], 值越大，亮度越低
        # beta:  亮度缩放後加上的参数，默認是 0.4， 範圍[0, 2]，值越大，亮度越低
        result = cv2.illuminationChange(img, highlight_mask, alpha=0.2, beta=0.2) 
    #     show_img(result)
            
        return result
    
    def japanese_style_filter(img):
        img = modify_lightness_saturation(img, lightness=0, saturation=50) # 單位: +- %

        img = modify_color_temperature(img, cold_rate=20) # 看你要+多冷 

        img = gaussian_noise(img, mean=0, sigma=0.05) # mean 平均, sigma 標準差
    
        img = modify_contrast_and_brightness(img, brightness=20 , contrast=-35) # -255 ~ 255
    
        img = reduce_highlights(img, light_threshold=255) # 光源的 threshold 以上會被做降光處理
    
        return img

    def film_camera_filter(img):
        img = modify_lightness_saturation(img, lightness=-15, saturation=-40) # 單位: +- %
        img = modify_contrast_and_brightness(img, brightness=+10 , contrast=-80) # -255 ~ 255
    
        img = reduce_highlights(img, light_threshold=255) # 光源的 threshold 以上會被做降光處理
    
        return img

    # cv2.imwrite('result_img.jpg', result_img)

    #image=cv2.imread('7.jpg')


    match choose:
        case 1:     #冬天
            flt_name = 'winter'
            img = Winter(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
        case 2:     #夏天
            flt_name = 'summer'
            img = Summer(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
        case 3:     #復古
            flt_name = 'retro'
            img = sepia(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
        case 4:     #日系
            flt_name = 'japan'
            img = japanese_style_filter(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
        case 5:     #黑白
            flt_name = 'gray'
            img = gray(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
        case 6:     #卡通
            flt_name = 'cartoon'
            img = cartoon(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)    
        case 7:     #素描
            flt_name = 'sketch'
            sketch(imgmsg)
        case 8:     #色鉛筆
            flt_name = 'col_pencil'
            img = pencil_sketch_col(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
        case 9:     #底片相機 原本放在case 5
            flt_name = 'camera'
            img = film_camera_filter(img)
            cv2.imwrite(f'{flt_name}{choose}_{imgmsg}', img)
    return flt_name
