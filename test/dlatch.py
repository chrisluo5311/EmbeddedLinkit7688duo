from PIL import Image
import pytesseract

# Load the image from file
img_path = '/mnt/data/CleanShot 2024-04-21 at 22.58.17@2x.jpg'
image = Image.open(img_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(image, lang='chi_tra')

text