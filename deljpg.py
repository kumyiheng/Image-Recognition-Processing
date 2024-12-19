import os
import glob

jpg_files = glob.glob("/Users/user/Desktop/Linebot/*.jpg")

for jpg in jpg_files:
    try:
        os.remove(jpg)
    except OSError as e:
        print(f"Error:{ e.strerror}")