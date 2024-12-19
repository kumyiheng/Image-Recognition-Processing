from imgurpython import ImgurClient
import sys,os


def upload_picture(image_path,client_id,client_secret):
    
    client = ImgurClient(client_id, client_secret)
    #image_path =r'.\output_image.png'
    image = client.upload_from_path(image_path, anon=True)

    image_link = image['link']
    return image_link