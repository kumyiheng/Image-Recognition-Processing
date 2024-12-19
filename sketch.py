from PIL import Image #導入PIL
from tqdm import tqdm

def sketch(imgmsg):
    img = Image.open(f'{imgmsg}') #打開圖片
    new = Image.new("L", img.size, 255) #新文件，大小和原來文件一樣
    width, height = img.size #圖片大小
    img = img.convert("L")

    Pen_size = 2 #int(input('Pensize:')) #画笔大小
    Color_diff = 3 #int(input('Color diffusion variable:')) #色差擴散器

    for i in tqdm(range(Pen_size + 1, width - Pen_size - 1)): 
        for j in range(Pen_size + 1, height - Pen_size - 1):
            originalColor = 255
            lcolor = sum([img.getpixel((i - r, j)) for r in range(Pen_size)]) // Pen_size
            rcolor = sum([img.getpixel((i + r, j)) for r in range(Pen_size)]) // Pen_size

            if abs(lcolor - rcolor) > Color_diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)

            ucolor = sum([img.getpixel((i, j - r)) for r in range(Pen_size)]) // Pen_size
            dcolor = sum([img.getpixel((i, j + r)) for r in range(Pen_size)]) // Pen_size

            if abs(ucolor - dcolor) > Color_diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)

            acolor = sum([img.getpixel((i - r, j - r)) for r in range(Pen_size)]) // Pen_size
            bcolor = sum([img.getpixel((i + r, j + r)) for r in range(Pen_size)]) // Pen_size

            if abs(acolor - bcolor) > Color_diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)

            qcolor = sum([img.getpixel((i + r, j - r)) for r in range(Pen_size)]) // Pen_size
            wcolor = sum([img.getpixel((i - r, j + r)) for r in range(Pen_size)]) // Pen_size

            if abs(qcolor - wcolor) > Color_diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)
    new.save(f'sketch7_{imgmsg}')