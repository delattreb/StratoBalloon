import PIL.Image as Image
import PIL.ImageDraw as ImageDraw

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

new_img.paste(img_incrust, (3497, 100),img_incrust)

img3 = Image.alpha_composite(img_cascade, new_img)
img3.save("newimage.jpg", 'jpeg')
img3.show()

main = Image.open("cascade.png")
watermark = Image.open("cascade2.png")

watermask = watermark.convert("L").point(lambda x: min(x, 100))
watermark.putalpha(watermask)
main.paste(watermark, None, watermark)
main.save("12volt-watermarked.jpg", "JPEG")
