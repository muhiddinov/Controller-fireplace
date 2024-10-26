import asyncio
from gpio_module import PWMModule, GPIOModule
from time import sleep
from machine import Pin
import _thread
from dfplayer import DFPlayer

""" SD media card tree
.
├── 01
│   ├── 001.mp3
│   ├── 002.mp3
│   └── ...
├── 02
│   ├── 001.mp3
│   ├── 002.mp3
│   └── ...
├── 03
│   ├── 001.mp3
│   ├── 002.mp3
│   └── ...
└── ...

"""


class ButtonIfaceThread():
    __rgb_data = {
        'orange': [245, 152, 66],
        'yellow': [255, 255, 0],
        'red': [255, 0, 0],
        'blue': [0, 0, 255],
        'green': [0, 255, 0],
    }
    __rgb_colors = list(__rgb_data.keys())
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
    
    _cooler_speed: int = 0  # [0 - 100]%
    _volume: int = 15       # [0 -  30]D
    _brightness: int = 50   # [0 - 100]%
    _modul_enable: bool = False
    _change_color: int = 0  # [0 - 5]
    _charge_water: bool = False
    _discharge_water: bool = False
    
    def __init__(self):
        self._dfplayer = DFPlayer(uart_id = 1, tx_pin_id = self._TXPIN, rx_pin_id = self._RXPIN)
        
        # RGB rangli chiroqlar uchun PWM chiquvchi pinlar
        self._redPWM = PWMModule(pinNumber=self._R_PIN, duty_max=255)
        self._greenPWM = PWMModule(pinNumber=self._G_PIN, duty_max=255)
        self._bluePWM = PWMModule(pinNumber=self._B_PIN, duty_max=255)
        self._coolerPWM = PWMModule(pinNumber=self._COOL_PIN, duty_max=6)
        
        # Diskret chiquvchi pinlar
        self._buzzer = GPIOModule(pinNumber=self._BUZZ_PIN)
        self._pump1 = GPIOModule(pinNumber=self._PMP_PIN1)
        self._pump2 = GPIOModule(pinNumber=self._PMP_PIN2)
        self._pump3 = GPIOModule(pinNumber=self._PMP_PIN3)
        self._pump4 = GPIOModule(pinNumber=self._PMP_PIN4)
        self._start = GPIOModule(pinNumber=self._START_PIN)
        self._start.set_value(0)
        
        # Suv bachoklarini o'lchab turish uchun interrupt pinlar
        self.lvl11 = Pin(self._LVL11_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl11.irq(trigger=Pin.IRQ_FALLING, handler=self.lvl_handle)
        self.lvl12 = Pin(self._LVL12_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl12.irq(trigger=Pin.IRQ_FALLING, handler=self.lvl_handle)
        self.lvl13 = Pin(self._LVL13_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl13.irq(trigger=Pin.IRQ_FALLING, handler=self.lvl_handle)
        self.lvl21 = Pin(self._LVL21_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl21.irq(trigger=Pin.IRQ_FALLING, handler=self.lvl_handle)
        self.lvl22 = Pin(self._LVL22_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl22.irq(trigger=Pin.IRQ_FALLING, handler=self.lvl_handle)
        self.lvl23 = Pin(self._LVL23_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl23.irq(trigger=Pin.IRQ_FALLING, handler=self.lvl_handle)
        
        # Buttonlar orqali boshqarish uchun interrupt pinlar
        btnWtrOut = Pin(self._BTN_WTROUT_PIN, Pin.IN, Pin.PULL_UP)
        btnWtrOut.irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handle)
        btnWtrIn = Pin(self._BTN_WTRIN_PIN, Pin.IN, Pin.PULL_UP)
        btnWtrIn.irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handle)
        btnLed = Pin(self._BTN_LED_PIN, Pin.IN, Pin.PULL_UP)
        btnLed.irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handle)
        btnPower = Pin(self._BTN_PWR_PIN, Pin.IN, Pin.PULL_UP)
        btnPower.irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handle)
        btnFlame = Pin(self._BTN_FLM_PIN, Pin.IN, Pin.PULL_UP)
        btnFlame.irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handle)
        
        self._mode = Pin(self._MODE_PIN, Pin.IN, Pin.PULL_UP)
        self._mode.irq(trigger=Pin.IRQ_FALLING, handler=self.mode_handle)

    def coolerSpeed(self, speed: int | None = None) -> int:
        print('Set fan speed:', speed)
        if speed == None:
            return self._cooler_speed
        else:
            self._cooler_speed = speed
            return speed
    
    def brighness(self, scale: int | None = None) -> int:
        print('Set brightness:', scale)
        if scale == None:
            return self._brightness
        else:
            self._brightness = scale
            return scale
    
    def volume(self, vol: int | None = None) -> int:
        print('Set volume:', vol)
        if vol == None:
            return self._volume
        else:
            self._volume = vol
            self._dfplayer.volume(self._volume)
            return vol
    
    def start(self, state: bool | None = None) -> bool:
        if state == None:
            return self._start.get_value()
        else:
            return self._start.set_value(state)
    
    def mode_handle(self, pin) -> None:
        self.work_mode = not self.work_mode
    
    def lvl_handle(self, pin) -> None:
        print('Callback from: Pin-', pin)
        if pin == self._LVL11_PIN:
            self.__fuelBox['fuel1'] = 2
            self._charge_water = False
        elif pin == self._LVL12_PIN:
            self.__fuelBox['fuel1'] = 1
        elif pin == self._LVL13_PIN:
            self.__fuelBox['fuel1'] = 0
            self._charge_water = True
        elif pin == self._LVL21_PIN:
            self.__fuelBox['fuel2'] = 2
            self._charge_water = False
        elif pin == self._LVL22_PIN:
            self.__fuelBox['fuel2'] = 1
        elif pin == self._LVL23_PIN:
            self.__fuelBox['fuel2'] = 0
            self._charge_water = True
        
        
    def btn_handle(self, pin):
        asyncio.run(self.buzzerBeep(100))
        if pin == self._BTN_FLM_PIN:
            self._cooler_speed += 1
            if self._cooler_speed > 6:
                self._cooler_speed = 0
                
        elif pin == self._BTN_LED_PIN:
            self._change_color += 1
            self.setColorToPWM(self.__rgb_colors[self._change_color])
            if self._change_color > len(self.__rgb_colors):
                self._change_color = 0
                
        elif pin == self._BTN_PWR_PIN:
            self._modul_enable = not self._modul_enable
            
        elif pin == self._BTN_WTRIN_PIN:
            self._charge_water = not self._charge_water
            
        elif pin == self._BTN_WTROUT_PIN:
            self._discharge_water = not self._discharge_water
            
        else:
            pass
            
    def setColorToPWM(self, color: str) -> None:
        try:
            (r, g, b) = self.__rgb_data[color]
            scale_factor = 100 / self._brightness
            r *= scale_factor
            g *= scale_factor
            b *= scale_factor
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

        
    async def buzzerBeep(self, delay: int):
        self._buzzer.set_value(1)
        sleep(delay/1000)
        self._buzzer.set_value(0)
    
    def run(self):
        _thread.start_new_thread(self.__main__, ())
        
    def __main__ (self):
        while True:
            try:
                if self._modul_enable == True:
                    if self._charge_water == True:
                        if self._mode == True:
                            self._pump1.value(1)
                            self._pump2.value(0)
                            self._pump3.value(1)
                            self._pump4.value(0)
                        else:
                            self._pump1.value(1)
                            self._pump2.value(0)
                    else:
                        if self._mode == True:
                            self._pump1.value(0)
                            self._pump2.value(0)
                            self._pump3.value(0)
                            self._pump4.value(0)
                        else:
                            self._pump1.value(0)
                            self._pump2.value(0)
                    
                    if self._discharge_water == True:
                        if self._mode == True:
                            self._pump1.value(0)
                            self._pump2.value(1)
                            self._pump3.value(0)
                            self._pump4.value(1)
                        else:
                            self._pump1.value(0)
                            self._pump2.value(1)
                    else:
                        if self._mode == True:
                            self._pump1.value(0)
                            self._pump2.value(0)
                            self._pump3.value(0)
                            self._pump4.value(0)
                        else:
                            self._pump1.value(0)
                            self._pump2.value(0)
                    
                           
                    if self._start.get_value() == 1:
                        if self._dfplayer.is_playing():
                            self._dfplayer.stop()
                        self._dfplayer.play(folder = 0, file = 0)
                    else:
                        self._dfplayer.stop()
                    if self._start.get_value() == True:
                        self._coolerPWM.set_pwm(self._cooler_speed)
                        if ((self.lvl11.value() == False and self.lvl12.value() == False and self.lvl13.value() == False) or
                            (self.lvl21.value() == False and self.lvl22.value() == False and self.lvl23.valure() == False)):
                            if self._dfplayer.is_playing() is True:
                                self._dfplayer.stop()
                                self._dfplayer.play(folder = 0, file = 1) # Suv tugaganda to'ldirish uchun ovozli bildirishnoma
                else:
                    self._dfplayer.stop()
                    self._start.set_value(0)
            except KeyboardInterrupt:
                print('Breaked threading!')
                break
            sleep(0.1)
