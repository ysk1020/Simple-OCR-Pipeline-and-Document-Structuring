import pytesseract
from PIL import Image

img = Image.open("data/raw/SROIE2019/train/img/X00016469612.jpg")
text = pytesseract.image_to_string(img)


print(text)
