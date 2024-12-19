from PIL import Image, ImageFilter

def blurring(imgmsg):
    img = Image.open(f'{imgmsg}.jpg')
    #img.show()

    blur_img = img.filter(ImageFilter.BLUR)

    for _ in range(10):
        blur_img = blur_img.filter(ImageFilter.BLUR)

    blur_img.save(f'blur_{imgmsg}.png')
