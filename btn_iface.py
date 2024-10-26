from threading import Thread
import asyncio
from gpio_module import PWMModule, GPIOModule
from time import sleep
from machine import Pin

class ButtonIfaceThread(Thread):
    __rgb_data = {
        'orange': [245, 152, 66],
        'yellow': [255, 255, 0],
        'red': [255, 0, 0],
        'blue': [0, 0, 255],
        'green': [0, 255, 0],
    }
    __fuelBox = {
        'fuel1': 0, # {0 - 1 - 2}
        'fuel2': 0  # {0 - 1 - 2}
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
        # RGB rangli chiroqlar uchun PWM chiquvchi pinlar
        self._redPWM = PWMModule(pinNumber=self._R_PIN, duty_max=255)
        self._greenPWM = PWMModule(pinNumber=self._G_PIN, duty_max=255)
        self._bluePWM = PWMModule(pinNumber=self._B_PIN, duty_max=255)
        
        # Diskret chiquvchi pinlar
        self._buzzer = GPIOModule(pinNumber=self._BUZZ_PIN)
        self._pump1 = GPIOModule(pinNumber=self._PMP_PIN1)
        self._pump2 = GPIOModule(pinNumber=self._PMP_PIN2)
        self._pump3 = GPIOModule(pinNumber=self._PMP_PIN3)
        self._pump4 = GPIOModule(pinNumber=self._PMP_PIN4)
        
        
        # Suv bachoklarini o'lchab turish uchun interrupt pinlar
        lvl11 = Pin(self._LVL11_PIN, Pin.IN, Pin.PULL_UP)
        lvl11.irq(trigger=Pin.IRQ_RISING, handler=self.lvl_handle)
        lvl12 = Pin(self._LVL12_PIN, Pin.IN, Pin.PULL_UP)
        lvl12.irq(trigger=Pin.IRQ_RISING, handler=self.lvl_handle)
        lvl13 = Pin(self._LVL13_PIN, Pin.IN, Pin.PULL_UP)
        lvl13.irq(trigger=Pin.IRQ_RISING, handler=self.lvl_handle)
        lvl21 = Pin(self._LVL21_PIN, Pin.IN, Pin.PULL_UP)
        lvl21.irq(trigger=Pin.IRQ_RISING, handler=self.lvl_handle)
        lvl22 = Pin(self._LVL22_PIN, Pin.IN, Pin.PULL_UP)
        lvl22.irq(trigger=Pin.IRQ_RISING, handler=self.lvl_handle)
        lvl23 = Pin(self._LVL23_PIN, Pin.IN, Pin.PULL_UP)
        lvl23.irq(trigger=Pin.IRQ_RISING, handler=self.lvl_handle)
        
        # Buttonlar orqali boshqarish uchun interrupt pinlar
        btnWtrOut = Pin(self._BTN_WTROUT_PIN, Pin.IN, Pin.PULL_UP)
        btnWtrOut.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handle)
        btnWtrIn = Pin(self._BTN_WTRIN_PIN, Pin.IN, Pin.PULL_UP)
        btnWtrIn.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handle)
        btnLed = Pin(self._BTN_LED_PIN, Pin.IN, Pin.PULL_UP)
        btnLed.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handle)
        btnPower = Pin(self._BTN_PWR_PIN, Pin.IN, Pin.PULL_UP)
        btnPower.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handle)
        btnFlame = Pin(self._BTN_FLM_PIN, Pin.IN, Pin.PULL_UP)
        btnFlame.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handle)
        
        self._mode = Pin(self._MODE_PIN, Pin.IN, Pin.PULL_UP)
        self._mode.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.mode_handle)

    def getWorkStatus(self) -> bool:
        return False

    def mode_handle(self, pin):
        self.work_mode = self._mode.value()
    
    def lvl_handle(self, pin):
        print('Callback from: Pin-', pin)
        if pin == self._LVL11_PIN:
            self.__fuelBox['fuel1'] = 2
        elif pin == self._LVL12_PIN:
            self.__fuelBox['fuel1'] = 1
        elif pin == self._LVL13_PIN:
            self.__fuelBox['fuel1'] = 0
        elif pin == self._LVL21_PIN:
            self.__fuelBox['fuel2'] = 2
        elif pin == self._LVL22_PIN:
            self.__fuelBox['fuel2'] = 1
        elif pin == self._LVL23_PIN:
            self.__fuelBox['fuel2'] = 0
        
        
    def btn_handle(self, pin):
        asyncio.run(self.buzzerBeep(100))

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
            pass