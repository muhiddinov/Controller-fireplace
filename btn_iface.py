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

    _R_PIN = 16
    _B_PIN = 3
    _G_PIN = 8
    _BUZZ_PIN = 5
    _START_PIN = 4
    
    _MODE_PIN = 15
    _IR_PIN = 2
    _PMP_PIN1 = 39
    _PMP_PIN2 = 40
    _PMP_PIN3 = 41
    _PMP_PIN4 = 42
    
    _RXPIN = 35
    _TXPIN = 45
    
    _BTN_WTROUT_PIN = 48
    _BTN_WTRIN_PIN = 47
    _BTN_LED_PIN = 21
    _BTN_PWR_PIN = 20
    _BTN_FLM_PIN = 19
    
    _LVL11_PIN = 46
    _LVL12_PIN = 9
    _LVL13_PIN = 10
    
    _LVL21_PIN = 11
    _LVL22_PIN = 12
    _LVL23_PIN = 13
    
    _COOL_PIN = 14
    
    def __init__(self):
        Thread.__init__(self)
        self._redPWM = PWMModule(pinNumber=self._R_PIN, duty_max=255)
        self._greenPWM = PWMModule(pinNumber=self._G_PIN, duty_max=255)
        self._bluePWM = PWMModule(pinNumber=self._B_PIN, duty_max=255)
        self._buzzer = GPIOModule(pinNumber=self._BUZZ_PIN)
    
    btn_wtrout_clicked = False
    
    def btn_wtrout_handle(self, pin):
        self.btn_wtrout_clicked = True

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
        
    def buzzerBeep(self, delay: int) -> None:
        self._buzzer.set_value(1)
        sleep(delay/1000)
        self._buzzer.set_value(0)

    def main(self):
        while True:
            print('Buzzer run')
            asyncio.run(self.buzzerBeep(200))
            sleep(0.1)
