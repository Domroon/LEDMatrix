import time
from random import randint
from machine import Pin
from neopixel import NeoPixel

LED_QTY = 256
COLOR = {
    "red" : [255, 0, 0],
    "green" : [0, 255, 0],
    "blue" : [0, 0, 255],
    "purple": [255, 0, 255],
    "yellow": [255, 255, 0],
    "white": [255, 255, 255]
}


class Matrix:
    def __init__(self, pin, np):
        self.pin = pin
        self.np = np
        
    def fill(self, color):
        self.np.fill(color)
        self.np.write()
        
    def clear(self):
        self.np.fill([0, 0, 0])
        self.np.write()
        
    def flash_random(self, color, duration, on_dura=0.1, colorful=False, clear=True):
        duration = duration / on_dura
        loops = 0
        while True:
            if loops == duration:
                break
            rand_num = randint(0, LED_QTY - 1)
            if colorful:
                colors = ["red", "green", "blue", "yellow", "white"]
                rand_col = randint(0, len(colors)-1)
                self.np[rand_num] = COLOR[colors[rand_col]]
            else:
                self.np[rand_num] = color
            self.np.write()
            time.sleep(on_dura)
            if clear:
                self.clear()
            loops = loops + 1
            
    def fade_in(self, color, steps, duration, reverse=False):
        step_duration = duration/steps
        loops = 0
        brightness = [0, 0, 0]
        if reverse:
            brightness = color
        else:
            for i in range(3):
                if color[i] > 0:
                    brightness[i] = 1
        while True:
            if loops == steps:
                break
            for i in range(3):
                if color[i] > 0 and not reverse:
                    brightness[i] += 1
                elif color[i] > 0 and reverse:
                    brightness[i] -= 1
            for i in range(0, LED_QTY):
                self.np[i] = brightness
            time.sleep(step_duration)
            self.np.write()
            loops = loops + 1
    
    def checkered_pattern(self, color1, color2, duration):
        for i in range(0, LED_QTY):
            if i % 2 == 0:
                self.np[i] = color1
            if i % 2 != 0:
                self.np[i] = color2
        self.np.write()
        time.sleep(duration)
    
    def fill_colorful(self, duration):
        for i in range(LED_QTY):
            rand1 = randint(0, 10)
            rand2 = randint(0, 10)
            rand3 = randint(0, 10)
            self.np[i] = [rand1, rand2, rand3]
        self.np.write()
        time.sleep(duration)
        
    def color_changing(self, current_color, fade_to_color, steps, duration):
        step_duration = duration/steps
        loops = 0
        mixed_color = [0, 0, 0]
        for i in range(3):
            if fade_to_color[i] > 0:
                fade_to_color[i] = 1
        while True:
            if loops == steps:
                break
            for i in range(3):
                if fade_to_color[i] > 0:
                    fade_to_color[i] += 1
                elif current_color[i] > 0:
                    current_color[i] -= 1
                mixed_color[i] = current_color[i] + fade_to_color[i]
            for i in range(0, LED_QTY):
                self.np[i] = mixed_color
            time.sleep(step_duration)
            self.np.write()
            loops = loops + 1
        
    def show_one_bus_sweep(self, color, duration):
        led_duration = duration / LED_QTY
        for i in range(0, LED_QTY):
            self.np[i] = color
            self.np.write()
            time.sleep(led_duration)
            self.clear()

    def show_square(self, x, y, color, duration, clear=True):
        if x==0 and y==0:
            for j in range(8):
                for i in range(8):
                    if j % 2 == 0:
                        self.np[i+j*16] = color
                    else:
                        self.np[i+j*16 + 8] = color
        if x == 1 and y == 0:
            for j in range(8):
                for i in range(8, 16):
                    if j % 2 == 0:
                        self.np[i+j*16] = color
                    else:
                        self.np[i+j*16 - 8] = color
        if x == 1 and y == 1:
            for j in range(8):
                for i in range(136,144):
                    if j % 2 == 0:
                        self.np[i+j*16] = color
                    else:
                        self.np[i+j*16-8] = color
        if x == 0 and y == 1:
            for j in range(8):
                for i in range(128,136):
                    if j % 2 == 0:
                        self.np[i+j*16] = color
                    else:
                        self.np[i+j*16+8] = color
        self.np.write()
        time.sleep(duration)
        self.clear()

    def show_snake(self, color, duration):
        color2 = [int(color[0]/2), int(color[1]/2), int(color[2]/2)]
        color3 = [int(color[0]/4), int(color[1]/4), int(color[2]/4)]
        color4 = [int(color[0]/8), int(color[1]/8), int(color[2]/8)]
        color5 = [int(color[0]/16), int(color[1]/16), int(color[2]/16)]
        x = 0
        loop_duration = (duration / LED_QTY)
        while True:
            if x == 256 - 4:
                break
            self.np[x+0] = color5
            self.np[x+1] = color4
            self.np[x+2] = color3
            self.np[x+3] = color2
            self.np[x+4] = color
            self.np.write()
            time.sleep(loop_duration)
            x += 1
            self.clear()

    def show_comets(self, color, duration):
        color2 = [int(color[0]/2), int(color[1]/2), int(color[2]/2)]
        color3 = [int(color[0]/4), int(color[1]/4), int(color[2]/4)]
        color4 = [int(color[0]/8), int(color[1]/8), int(color[2]/8)]
        color5 = [int(color[0]/16), int(color[1]/16), int(color[2]/16)]
        x = 0
        loop_duration = (duration / LED_QTY)
        while True:
            if x == 16-4:
                break
            for i in range(16):
                self.np[x+0+i*16] = color5
                self.np[x+1+i*16] = color4
                self.np[x+2+i*16] = color3
                self.np[x+3+i*16] = color2
                self.np[x+4+i*16] = color
            self.np.write()
            time.sleep(loop_duration)
            x += 1
            self.clear()

    def show_random_pixel_slides(self, color, duration):
        x = 0
        loop_duration = (duration / LED_QTY)
        while True:
            if x == 16:
                break
            for i in range(16):
                show = randint(0, 1)
                if show:
                    self.np[x+i*16] = color
            self.np.write()
            time.sleep(loop_duration)
            x += 1
            self.clear()

    def fill_in_pieces(self, color, duration):
        loop_duration = duration / LED_QTY
        for i in range(LED_QTY):
            self.np[i] = color
            self.np.write()
            time.sleep(loop_duration)

    def tetris_point_fill(self, color, duration):
        loop_duration = duration / LED_QTY
        led_num = LED_QTY
        while led_num >= 0:
            for i in range(led_num):
                self.np[i] = color
                self.np.write()
                # time.sleep(loop_duration)
                self.np[i] = [0, 0, 0]
                self.np.write()
            self.np[led_num-1] = color
            self.np.write()
            led_num -= 1

    def tetris_line_fill(self, color, duration):
        loop_duration = duration / LED_QTY
        line_num = 16
        while line_num >= 0:
            for j in range(line_num):
                for i in range(16):
                    self.np[i+16*j] = color
                self.np.write()
                time.sleep(loop_duration)
                for i in range(16):
                    self.np[i+16*j] = [0, 0, 0]
                self.np.write()
            for i in range(16):
                    self.np[i+16*j] = color
            self.np.write()
            line_num -= 1


def flash_in_different_colors(matrix):
    matrix.flash_random(COLOR["white"], 1)
    matrix.flash_random(COLOR["red"], 1)
    matrix.flash_random(COLOR["green"], 1)
    matrix.flash_random(COLOR["blue"], 1)
    matrix.flash_random(COLOR["purple"], 1)
    matrix.flash_random(COLOR["yellow"], 1)
    matrix.flash_random(COLOR["white"], 1, on_dura=0.01)
    matrix.flash_random(COLOR["white"], 1, on_dura=0.01, colorful=True)


def fade_different_colors(matrix, brightness, single_duration):
    matrix.fade_in([brightness, 0, 0], brightness, single_duration)
    matrix.fade_in([brightness, 0, 0], brightness, single_duration, reverse=True)
    matrix.fade_in([0, brightness, 0], brightness, single_duration)
    matrix.fade_in([0, brightness, 0], brightness, single_duration, reverse=True)
    matrix.fade_in([0, 0, brightness], brightness, single_duration)
    matrix.fade_in([0, 0, brightness], brightness, single_duration, reverse=True)


def show_different_checkered(matrix):
    loop = 0
    while loop < 20:
        matrix.checkered_pattern([20, 0, 0], [0, 0, 20], 0.1)
        matrix.checkered_pattern([0, 0, 20], [20, 0, 0], 0.1)
        loop += 1
    loop = 0
    while loop < 20:
        matrix.checkered_pattern([0, 20, 0], [20, 0, 20], 0.1)
        matrix.checkered_pattern([20, 0, 20], [0, 20, 0], 0.1)
        loop += 1
    loop = 0
    while loop < 20:
        matrix.checkered_pattern([20, 20, 20], [0, 0, 0], 0.1)
        matrix.checkered_pattern([0, 0, 0], [20, 20, 10], 0.1)
        loop += 1
    matrix.clear()


def fade_pixels_in_and_out(matrix):
    matrix.flash_random([20, 20, 20], 10, clear=False, on_dura=0.01)
    matrix.flash_random([0, 0, 0], 10, clear=False, on_dura=0.01)
    
    matrix.flash_random([20, 0, 0], 10, clear=False, on_dura=0.01)
    matrix.flash_random([0, 0, 0], 10, clear=False, on_dura=0.01)

    matrix.flash_random([0, 20, 0], 10, clear=False, on_dura=0.01)
    matrix.flash_random([0, 0, 0], 10, clear=False, on_dura=0.01)

    matrix.flash_random([0, 0, 20], 10, clear=False, on_dura=0.01)
    matrix.flash_random([0, 0, 0], 10, clear=False, on_dura=0.01)


def show_pixel_noise(matrix):
    for _ in range(200):
        matrix.fill_colorful(0.04)


def different_color_fadeing(matrix, brightness, dura_per_color):
    matrix.color_changing([brightness, 0, 0], [0, brightness, 0], brightness, dura_per_color)
    matrix.color_changing([0, brightness, 0], [0, 0, brightness], brightness, dura_per_color)
    matrix.color_changing([0, 0, brightness], [brightness, 0, 0], brightness, dura_per_color)
    matrix.color_changing([brightness, 0, 0], [0, 0, brightness], brightness, dura_per_color)


def show_sweep_different_colors(matrix, duration_per_color):
    matrix.show_one_bus_sweep([255, 0, 0], duration_per_color)
    matrix.show_one_bus_sweep([0, 255, 0], duration_per_color)
    matrix.show_one_bus_sweep([0, 0, 255], duration_per_color)
    matrix.show_one_bus_sweep([255, 255, 255], duration_per_color)


def show_squares(matrix, duration_per_square, loops):
    color = [10, 0, 0]
    for _ in range(loops):
        matrix.show_square(1, 1, color, duration_per_square)
        matrix.show_square(0, 0, color, duration_per_square)
        matrix.show_square(0, 1, color, duration_per_square)
        matrix.show_square(1, 0, color, duration_per_square)
        
        
    color = [0, 0, 10]
    for _ in range(loops):
        matrix.show_square(0, 0, color, duration_per_square)
        matrix.show_square(1, 0, color, duration_per_square)
        matrix.show_square(1, 1, color, duration_per_square)
        matrix.show_square(0, 1, color, duration_per_square)
    color = [0, 10, 0]
    for _ in range(loops):
        matrix.show_square(0, 1, color, duration_per_square)
        matrix.show_square(1, 1, color, duration_per_square)
        matrix.show_square(1, 0, color, duration_per_square)
        matrix.show_square(0, 0, color, duration_per_square)
        
        
def main():
    pin = Pin(14, Pin.OUT)   # 
    np = NeoPixel(pin, LED_QTY)  
    matrix = Matrix(pin, np)
    matrix.clear()
    input("Press enter for start")
    # flash_in_different_colors(matrix)
    # fade_different_colors(matrix, 10, 2)
    # show_different_checkered(matrix)
    # fade_pixels_in_and_out(matrix)
    # show_pixel_noise(matrix)
    # different_color_fadeing(matrix, 20, 5)
    # show_sweep_different_colors(matrix, 0.1)
    show_squares(matrix, 0.1, 10)

    # matrix.flash_random([0, 0, 20], 5, on_dura=0.5, colorful=True)
    # matrix.flash_random([0, 0, 20], 4, on_dura=0.05, colorful=True)
    # matrix.flash_random([0, 0, 20], 2, on_dura=0.01, colorful=True)
    #matrix.show_snake([100, 100, 100], 0.5)
    #matrix.show_snake([0, 0, 100], 0.5)
    # matrix.fill([10, 0, 0])
    #matrix.show_comets([100, 0, 0], 10)
    #matrix.show_comets([0, 100, 0], 10)
    #matrix.show_comets([0, 0, 100], 10)
    # loop = 0
    # while loop <=2:
    #     matrix.show_random_pixel_slides([0, 0, 100], 5)
    #     loop += 1
    # loop = 0    
    # while loop <=2:
    #     matrix.show_random_pixel_slides([0, 100, 0], 5)
    #     loop += 1
    # loop = 0
    # while loop <=2:
    #     matrix.show_random_pixel_slides([100, 0, 0], 5)
    #     loop += 1
    #matrix.fill_in_pieces([0, 0, 20], 1)
    #matrix.fill_in_pieces([0, 20, 0], 1)
    #matrix.tetris_line_fill([20, 0, 0], 1)
    #matrix.clear()
    #matrix.tetris_line_fill([0, 20, 0], 1)
    #matrix.clear()
    #matrix.tetris_line_fill([0, 0, 20], 1)
    #matrix.clear()
    


if __name__ == '__main__':
    main()