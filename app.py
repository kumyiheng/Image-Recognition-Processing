from flask import Flask, request, abort
import json

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os 

#自己寫的函數
from bg import rembg
from upload import upload_picture
from blur import blurring
#from blackwhite import black_white
from filter import *
from edge import edge
from change import change_bg

app = Flask(__name__)

#變數設定
pic = False
reply_text = True
flt = False
ch_bg = False
imgur_id = '4ba52708446e72b'
imgur_secret = 'b3e760d72946aaa64ed71d4bfdfd7a8c33ddcf9f'

@app.route("/", methods=['POST'])   
def linebot():
    body = request.get_data(as_text=True)                    # 取得訊息內容
    global imgmsg       # str 待處理圖片的訊息ID後6碼
    global pic          # bool 有無可處理圖片
    global reply_text    # bool 決定要不要傳文字(有傳圖就不傳文字)
    global image_message # ?type 回傳給使用者的圖 包含兩個變數 預覽圖和完成圖
    global flt          #要使用濾鏡時 設為True
    global ch_bg        #使用換背景時 設為True
    global alt_img      #換背景時存下第一張圖
    try:
        json_data = json.loads(body)                         # 轉json格式
        access_token = 'G6a0W08GOKs4x9V+eECvB+FCqpsiRFWCE6pRZNLu9CW+z1npN4VnG2/RtJnYdnOvuBnTGzIeAiqgwwVHszzjdB4Tpm38dOjtYwHph3FbK+W+T7Usnrb7jCXOp9waQ56xA4rv7AVaNIijmMSq2ZtVEwdB04t89/1O/w1cDnyilFU='
        secret = 'b5f7b258feb5e4323208308cd00a1780'
        line_bot_api = LineBotApi(access_token)              # 確認token 
        handler = WebhookHandler(secret)                     # 確認secret
        signature = request.headers['X-Line-Signature']      # 加入回傳headers
        handler.handle(body, signature)                      # 綁定回傳資訊
        reply_token = json_data['events'][0]['replyToken']   # 取得回傳Token
        type = json_data['events'][0]['message']['type']     # 取得收到訊息類型
        if type == 'text' :
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
        #接收數字    
            if (flt):
                flt = False
                if not msg[0].isdigit():
                    reply = '請輸入有效數字(0~10)'
                    line_bot_api.reply_message(reply_token,TextSendMessage(reply))
                else:
                    num = int(msg)
                    if(num == 0):
                        reply = '已取消使用濾鏡'
                        line_bot_api.reply_message(reply_token,TextSendMessage(reply))
                        reply_text = False
                    elif(num>=1 and num<=10):
                        flt_name = filter(f'{imgmsg}.jpg', num)
                        pic_link = upload_picture(f'{flt_name}{num}_{imgmsg}.jpg',imgur_id,imgur_secret) 
                        image_message = ImageSendMessage(                 # 放做好的圖片
                            # 完全跑完的圖片
                            original_content_url = pic_link,             
                            # 載入時顯示的圖片
                            preview_image_url = pic_link#'https://png.pngtree.com/png-vector/20211111/ourmid/pngtree-minimal-loading-icon-graphic-png-image_4029241.png'
                        )
                        line_bot_api.reply_message(reply_token, image_message)
                        print('圖片已傳送')
                        reply_text = False   
                        pic = False
                        #os.remove(f'{flt_name}{num}_{imgmsg}.jpg') #刪掉做好的圖檔 
                    else:
                        reply = '請輸入有效數字(0~10)'
                        line_bot_api.reply_message(reply_token,TextSendMessage(reply))
        #處理換背
            if (ch_bg):  #這裡不該為True 若輸入非圖片 則取消操作
                ch_bg = False
                reply = '已取消更換背景'
                line_bot_api.reply_message(reply_token,TextSendMessage(reply))
                reply_text = False   
                pic = False
        #去背   
            if re.match('去除背景',msg):
                if pic == True:                              # 有可處裡圖片                   
                    reply = '去除背景中...'
                    rembg(imgmsg)                            # 做去背(bg.py)
                    #去背完上傳到imgur (upload.py) 
                    pic_link = upload_picture(f'bg_{imgmsg}.png',imgur_id,imgur_secret)
                    image_message = ImageSendMessage(                 # 放做好的圖片
                        # 完全跑完的圖片
                        original_content_url = pic_link,             
                        # 載入時顯示的圖片
                        preview_image_url = pic_link#'https://png.pngtree.com/png-vector/20211111/ourmid/pngtree-minimal-loading-icon-graphic-png-image_4029241.png'
                    )
                    line_bot_api.reply_message(reply_token, image_message)
                    print('圖片已傳送') 
                    reply_text = False  
                    pic = False
                    #os.remove(f'bg_{imgmsg}.jpg') #刪掉做好的圖檔             
                else:
                    reply = '未傳送圖片或是此圖片已處理完成'
        #模糊圖片 彩蛋 非功能
            elif re.match('沒戴眼鏡',msg) or re.match('模糊',msg):
                if pic == True:
                    reply = '模糊圖片中...'   
                    blurring(imgmsg)
                    pic_link = upload_picture(f'blur_{imgmsg}.png',imgur_id,imgur_secret)
                    image_message = ImageSendMessage(                 # 放做好的圖片
                        # 完全跑完的圖片
                        original_content_url = pic_link,             
                        # 載入時顯示的圖片
                        preview_image_url = pic_link#'https://png.pngtree.com/png-vector/20211111/ourmid/pngtree-minimal-loading-icon-graphic-png-image_4029241.png'
                    )
                    line_bot_api.reply_message(reply_token, image_message)
                    print('圖片已傳送')
                    reply_text = False   
                    pic = False
                    #os.remove(f'blur_{imgmsg}.jpg') #刪掉做好的圖檔 
                else:
                    reply = '傳送圖片並輸入關鍵字解鎖彩蛋!' 
        #濾鏡           
            elif re.match('使用濾鏡',msg):
                if pic == True:
                    flt = True
                    reply = '請輸入數字編號以使用濾鏡：\n0: 取消/返回\n1: 冬天\n2: 秋天\n3: 復古\n4: 日系\n5: 黑白\n6: 卡通\n7: 素描\n8: 色鉛筆\n9: 底片相機'
                    line_bot_api.reply_message(reply_token,TextSendMessage(reply))
                    print('圖片已傳送')
                    reply_text = False
                else:
                    reply = '未傳送圖片或是此圖片已處理完成' 
        #偵測邊緣
            elif re.match('邊緣偵測',msg):
                if pic == True:
                    reply = '偵測輪廓中...'   
                    edge(imgmsg)
                    pic_link = upload_picture(f'edge_{imgmsg}.jpg',imgur_id,imgur_secret)
                    image_message = ImageSendMessage(                 # 放做好的圖片
                        # 完全跑完的圖片
                        original_content_url = pic_link,             
                        # 載入時顯示的圖片
                        preview_image_url = pic_link#'https://png.pngtree.com/png-vector/20211111/ourmid/pngtree-minimal-loading-icon-graphic-png-image_4029241.png'
                    )
                    line_bot_api.reply_message(reply_token, image_message)
                    print('圖片已傳送')
                    reply_text = False   
                    pic = False
                    #os.remove(f'edge_{imgmsg}.jpg') #刪掉做好的圖檔 
                else:
                    reply = '未傳送圖片或是此圖片已處理完成' 
        #更換背景
            elif re.match('更換背景',msg):
                if pic == True:
                    ch_bg = True
                    alt_img = imgmsg    
                    reply = '處理完成 請傳送一張背景圖\n輸入"取消"以返回操作'
                    #rembg(imgmsg)
                    line_bot_api.reply_message(reply_token,TextSendMessage(reply))
                    rembg(imgmsg)
                    print('等待接收背景圖...')
                    reply_text = False
                    pic = False
                else:
                    reply = '未傳送圖片或是此圖片已處理完成' 
        #若為無效訊息 回傳該訊息          
            else:
                reply = msg
            print(msg)
    
        elif type == 'image':
            pic = True
            img_msgID = json_data['events'][0]['message']['id']  # 取得訊息id
            imgmsg = img_msgID[-6:]                                # =訊息id後六碼
            message_content = line_bot_api.get_message_content(img_msgID)  # 用訊息ID取得內容
            # 在同資料夾建立以訊息ID後6碼為檔名的.jpg檔
            with open(f'{img_msgID[-6:]}.jpg', 'wb') as fd:
                fd.write(message_content.content)                # 以二進位的方式寫入檔案
        #執行換背景
            if(ch_bg):
                ch_bg = False
                change_bg(alt_img, imgmsg)
                pic_link = upload_picture(f'ch_{imgmsg}.jpg',imgur_id,imgur_secret)
                image_message = ImageSendMessage(                 # 放做好的圖片
                    # 完全跑完的圖片
                    original_content_url = pic_link,             
                    # 載入時顯示的圖片
                    preview_image_url = pic_link#'https://png.pngtree.com/png-vector/20211111/ourmid/pngtree-minimal-loading-icon-graphic-png-image_4029241.png'
                )
                line_bot_api.reply_message(reply_token, image_message)
                print('圖片已傳送')
                reply_text = False   
                pic = False
            else:
                reply = '圖片儲存成功！\n請選擇要對圖片做的處理: ' 
        else:
            reply = '請傳送文字或是圖片(.jpg)哦～'
            print(reply)

        if(reply_text):
            line_bot_api.reply_message(reply_token,TextSendMessage(reply))  # 回傳Text
        else:
            reply_text = True
    except:
        print('error')
        #print(body)          # 錯誤時，印出收到的內容
    return 'OK'              # 驗證Webhook，不能省

if __name__ == "__main__":
    app.run()
