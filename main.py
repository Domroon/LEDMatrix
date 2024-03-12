import time
from random import randint
from machine import Pin
from neopixel import NeoPixel

LED_QTY = 256


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
        duration = duration * (1/on_dura)
        loops = 0
        while True:
            if loops == duration:
                break
            rand_num = randint(0, LED_QTY - 1)
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
            rand1 = randint(0, 50)
            rand2 = randint(0, 50)
            rand3 = randint(0, 50)
            self.np[i] = [rand1, rand2, rand3]
        self.np.write()
        time.sleep(duration)
        
     def color_changing(self, current_color, fade_to_color, max_brightness):
        # copy from fade in and add a second color! to change these two
        # colors at the same time, the one in reverse and the other not reversed
        
        
def main():
    pin = Pin(14, Pin.OUT)   # 
    np = NeoPixel(pin, LED_QTY)  
    matrix = Matrix(pin, np)
    matrix.clear()
    input("Press enter for start")
    while True:
        matrix.fill_colorful(0.01)
    
    matrix.fill([20, 0, 0]) # add second fill with duration?


if __name__ == '__main__':
    main()