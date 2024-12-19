import colorsys
from PIL import Image

def black_white(imgmsg):
    
    img = Image.open(f'{imgmsg}.jpg')
    '''
    img.load()

    r,g,b = img.split()
    result = []

    for pixel_r, pixel_g, pixel_b in zip(r.getdata(), g.getdata(), b.getdata()):
        gray_value = (pixel_r + pixel_g + pixel_b) // 6
        result.append((gray_value, gray_value, gray_value))
    
    img.putdata(result)
    '''
    bw_img = img.convert('1')
    bw_img.save(f'BW_{imgmsg}.png')

