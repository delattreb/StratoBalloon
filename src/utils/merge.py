"""

a essayer

case1:
from PIL import Image

opacity_level = 170 # Opaque is 255, input between 0-255

img = Image.open('img1.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    newData.append((0, 0, 0, opacity_level))
else:
    newData.append(item)

img.putdata(newData)
img.save("img2.png", "PNG")


In my case, I have text with black background and wanted only the background semi-transparent, in which case:

case 2:
from PIL import Image

opacity_level = 170 # Opaque is 255, input between 0-255

img = Image.open('img1.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:
        newData.append((0, 0, 0, opacity_level))
    else:
        newData.append(item)

img.putdata(newData)
img.save("img2.png", "PNG")


another case:

import Image
import ImageDraw
im = Image.open("image.png")
transparent_area = (50,80,100,200)

mask=Image.new('L', im.size, color=255)
draw=ImageDraw.Draw(mask)
draw.rectangle(transparent_area, fill=0)
im.putalpha(mask)
im.save('/tmp/output.png')

"""

import PIL.Image as Image

new_incrust = Image.new('RGBA', (640, 280), "#FFFFFF")
img_incrust = Image.open("img24.png")
img_incrust = img_incrust.convert('RGBA')
new_incrust = new_incrust.convert('RGBA')
print(new_incrust.mode)
print(img_incrust.mode)
# Supression Logo google
img_incrust = Image._ImageCrop.crop(img_incrust, (0, 0, 640, 280))
new_incrust.paste(img_incrust)

watermask = new_incrust.convert("L").point(lambda x: min(x, 100))
new_incrust.putalpha(watermask)

img_cascade = Image.open("cascade.png")
new_img = Image.new('RGBA', (4237, 2813))
new_img = new_img.convert('RGBA')
img_cascade = img_cascade.convert('RGBA')

new_img.paste(img_incrust, (3497, 100), img_incrust)

img3 = Image.alpha_composite(img_cascade, new_img)
img3.save("newimage.jpg", 'jpeg')
img3.show()

main = Image.open("cascade.png")
watermark = Image.open("cascade2.png")

watermask = watermark.convert("L").point(lambda x: min(x, 100))
watermark.putalpha(watermask)
main.paste(watermark, None, watermark)
main.save("12volt-watermarked.jpg", "JPEG")
