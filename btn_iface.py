from threading import Thread
import asyncio
from gpio_module import PWMModule, GPIOModule
from time import sleep

class ButtonIfaceThread(Thread):
    __rgb_data = {
        'orange': [245, 152, 66],
        'yellow': [255, 255, 0],
        'red': [255, 0, 0],
        'blue': [0, 0, 255],
        'green': [0, 255, 0],
    }

    _redPin = 12
    _bluePin = 13
    _greenPin = 14
    _buzzerPin = 15

    def __init__(self):
        Thread.__init__(self)
        self._redPWM = PWMModule(pinNumber=self._redPin, duty_max=255)
        self._greenPWM = PWMModule(pinNumber=self._greenPin, duty_max=255)
        self._bluePWM = PWMModule(pinNumber=self._bluePin, duty_max=255)
        self._buzzer = GPIOModule(pinNumber=self._buzzerPin)


    def setColorToPWM(self, color: str):
        try:
            (r, g, b) = self.__rgb_data[color]
            self._redPWM.set_pwm(r)
            self._greenPWM.set_pwm(g)
            self._bluePWM.set_pwm(b)
            print('Color:', color)
        except KeyError:
            print('Color not found!')
        

    def setRGB2PWM(self, red, green, blue):
        self._redPWM.set_pwm(red)
        self._greenPWM.set_pwm(green)
        self._bluePWM.set_pwm(blue)

    def run(self):
        self.main()
        
    def buzzerBeep(self, delay):
        self._buzzer.set_value(1)
        sleep(delay/1000)
        self._buzzer.set_value(0)

    def setUpBtnPin(self, btnPin):
        self.__upbtn_pin = btnPin

    def main(self):
        while True:

            asyncio.run(self.buzzerBeep(200))
