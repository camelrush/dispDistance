import datetime
import board
import numpy as np
from adafruit_vl53l0x import VL53L0X 
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image , ImageDraw ,ImageFont

FONT_SANS_12 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ,12)
FONT_SANS_18 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ,18)

display = SSD1306_I2C(128, 64, board.I2C(), addr=0x3C)
dsensor = VL53L0X(board.I2C(), address=0x29)

if __name__== '__main__':

    display.fill(0)
    display.show()
    distance_array = []

    # Main loop.
    while True:

        # 距離を取得(平均)
        data = dsensor.range
        distance_array.append(data)
        distance = round(np.average(distance_array))

        # 3回分の平均を表示
        if len(distance_array) == 3:
            img = Image.new("1",(display.width, display.height))
            draw = ImageDraw.Draw(img)

            # 時刻表示
            timestamp = datetime.datetime.now()
            draw.text((0,0),'時刻  ' + timestamp.strftime('%H:%M:%S'),font=FONT_SANS_12,fill=1)

            # H/W仕様の2mを超える値が返ってきたら"測定不能"とする
            if distance > 2000:
                draw.text((0,20),'距離  ' + '計測不能',font=FONT_SANS_18,fill=1)
            else:
                draw.text((0,20),'距離  ' + str(round(distance/10 ,1)) + 'cm',font=FONT_SANS_18,fill=1)
            display.image(img)
            display.show()

            # Array Clear
            distance_array = []
