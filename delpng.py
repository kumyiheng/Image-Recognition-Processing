import os
import glob

png_files = glob.glob("/Users/user/Desktop/Linebot/*.png")

for png in png_files:
    try:
        os.remove(png)
    except OSError as e:
        print(f"Error:{ e.strerror}")