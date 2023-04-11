import datetime

from PIL import Image, ImageDraw, ImageFont

im = Image.open('БОРДОВАЯ КАРТИНКА.jpg')

draw_text = ImageDraw.Draw(im)
font = ImageFont.truetype("Comic Sans MS.ttf", 80)
draw_text.text(
    (370,450),
    datetime.datetime.now().strftime("%Y-%m-%d"),
    fill=('#ffffff'),
    font=font,
    )

im.save('БОРДОВАЯ КАРТИНКА2.jpg')