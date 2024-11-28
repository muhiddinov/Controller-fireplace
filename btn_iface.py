import asyncio
from gpio_module import PWMModule, GPIOModule
from time import sleep
from machine import Pin
import _thread
from dfplayer import DFPlayer
from utime import sleep_ms, ticks_ms
#from ButtonDebounce import Debounce

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
        'orange': [255, 255, 128],
        'yellow': [255, 255, 0],
        'red': [255, 0, 0],
        'blue': [0, 0, 255],
        'green': [0, 255, 0],
    }
    __rgb_colors = list(__rgb_data.keys())
    _LEN_COLOR = len(__rgb_colors)
    
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
    _volume_1_level:list(bool) = []
    _volume_2_level:list(bool) = []
    _cooler_speed: int = 0  # [0 - 100]%
    _volume: int = 15       # [0 -  30]D
    _brightness: int = 50   # [0 - 100]%
    _modul_enable: bool = False
    _change_color: int = 0  # [0 - 5]
    _charge_water: bool = False
    _discharge_water: bool = False
    _last_color = []
    _last_color_name: str = "orange"
    _mode = False
    DEBOUNCE_TIME = 500
    LEVEL_DEBOUNCE_TIME = 10000
    
    def __init__(self):
        self._dfplayer = DFPlayer(uart_id = 1, tx_pin_id = self._TXPIN, rx_pin_id = self._RXPIN)
        # RGB rangli chiroqlar uchun PWM chiquvchi pinlar
        self._redPWM = PWMModule(pinNumber=self._R_PIN, freq=1000, duty_max=255)
        self._greenPWM = PWMModule(pinNumber=self._G_PIN, freq=1000, duty_max=255)
        self._bluePWM = PWMModule(pinNumber=self._B_PIN, freq=1000, duty_max=255) # led uchun chastota 1000 bo'lishi kerak
        self._coolerPWM = PWMModule(pinNumber=self._COOL_PIN, freq=50, duty_max=12) # matorlar uchun chastota 50 ham bo'ladi
        
        # Diskret chiquvchi pinlar
        self._buzzer = GPIOModule(pinNumber=self._BUZZ_PIN)
        self._pump1 = GPIOModule(pinNumber=self._PMP_PIN1)
        self._pump2 = GPIOModule(pinNumber=self._PMP_PIN2)
        self._pump3 = GPIOModule(pinNumber=self._PMP_PIN3)
        self._pump4 = GPIOModule(pinNumber=self._PMP_PIN4)
        self._start = GPIOModule(pinNumber=self._START_PIN)
        
        #initializing values
        self._pump1.set_value(0)
        self._pump2.set_value(0)
        self._pump3.set_value(0)
        self._pump4.set_value(0)
        self._start.set_value(0)
        self.notice_charge_water = False
        self._brightness = 50
        self._last_color = self.setColorToRGB('orange')
        self._module_enable = False
        self._cooler_speed = 7
        self.running = True
        
        # Suv bachoklarini o'lchab turish uchun interrupt pinlar
        self.lvl11 = Pin(self._LVL11_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl12 = Pin(self._LVL12_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl13 = Pin(self._LVL13_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl21 = Pin(self._LVL21_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl22 = Pin(self._LVL22_PIN, Pin.IN, Pin.PULL_UP)
        self.lvl23 = Pin(self._LVL23_PIN, Pin.IN, Pin.PULL_UP)
        self._volume_1_level = [self.lvl11.value(), self.lvl12.value(), self.lvl13.value()]
        self._volume_2_level = [self.lvl21.value(), self.lvl22.value(), self.lvl23.value()]
        self._volume_1_level = [not x for x in self._volume_1_level]
        self._volume_2_level = [not x for x in self._volume_2_level]
        
        
        # Buttonlar orqali boshqarish uchun interrupt pinlar
        self.btnWtrOut = Pin(self._BTN_WTROUT_PIN, Pin.IN, Pin.PULL_UP)
        self.btnWtrOut.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.btn_handle)
        self.btnWtrIn = Pin(self._BTN_WTRIN_PIN, Pin.IN, Pin.PULL_UP)
        self.btnWtrIn.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.btn_handle)
        self.btnLed = Pin(self._BTN_LED_PIN, Pin.IN, Pin.PULL_UP)
        self.btnLed.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.btn_handle)
        self.btnPower = Pin(self._BTN_PWR_PIN, Pin.IN, Pin.PULL_UP)
        self.btnPower.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.btn_handle)
        self.btnFlame = Pin(self._BTN_FLM_PIN, Pin.IN, Pin.PULL_UP)
        self.btnFlame.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.btn_handle)
        self.btnMode = Pin(self._MODE_PIN, Pin.IN, Pin.PULL_UP)
        self.btnMode.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.btn_handle)
        self.buttons_state = {
                self.btnWtrIn: [self.btnWtrIn.value(), ticks_ms()],
                self.btnWtrOut: [self.btnWtrOut.value(), ticks_ms()],
                self.btnLed: [self.btnLed.value(), ticks_ms()],
                self.btnPower: [self.btnPower.value(), ticks_ms()],
                self.btnFlame: [self.btnFlame.value(), ticks_ms()],
                self.btnMode: [self.btnMode.value(), ticks_ms()]
            }
    
    
    def btn_handle(self, pin):
        check_pin = False
        last_value = self.buttons_state[pin][0]
        if pin.value() != last_value:
            #change state
            last_change_time = self.buttons_state[pin][1]
            if ticks_ms() - last_change_time > self.DEBOUNCE_TIME:
                if pin.value() == False: #check only pressed
                    check_pin = True
            self.buttons_state[pin] = [pin.value(), ticks_ms()] #last changed time
        if check_pin == True:
            asyncio.run(self.buzzerBeep(200))
            if pin == self.btnFlame:
                self._cooler_speed += 1
                if self._cooler_speed == 1:
                    self._cooler_speed = 7
                print("Cooler Speed:", self._cooler_speed)
                if self._cooler_speed > 12:
                    self._cooler_speed = 0
                    
            elif pin == self.btnLed:
                self._change_color += 1
                if self._change_color > self._LEN_COLOR:
                    self._change_color = 0
                self._last_color_name = self.__rgb_colors[self._change_color]
                print('Change color to', self._last_color_name)
                self._last_color = self.setColorToRGB(self._last_color_name)
                    
            elif pin == self.btnPower:
                self._modul_enable = not self._modul_enable
                self.start(self._modul_enable)
                print('Power enable:', self._modul_enable)
                
            elif pin == self.btnWtrIn:
                self._charge_water = not self._charge_water
                if self._charge_water == True:
                    self._discharge_water = False
                print("Charge water:", self._charge_water)
                
            elif pin == self.btnWtrOut:
                self._discharge_water = not self._discharge_water
                if self._discharge_water == True:
                    self._charge_water =  False
                print("Discharge water:", self._discharge_water)
            
            elif pin == self.btnMode:
                self._mode = not self._mode
                print("Mode:", self._mode)
                    
            else:
                pass
        
    def chargeWater(self, charge: bool|None) -> bool:
        if charge == None:
            return self._charge_water
        self._charge_water = charge
        return charge
    
    def disChargeWater(self, disCharge: bool|None) -> bool:
        if disCharge == None:
            return self._discharge_water
        self._discharge_water = disCharge
        return disCharge
    
    def pumpState(self) -> list[bool]:
        return [self._pump1.get_value(), self._pump2.get_value(), self._pump3.get_value(), self._pump4.get_value()]

    def coolerSpeed(self, speed: int | None = None) -> int:
        print('Set fan speed:', speed)
        if speed == None:
            return self._cooler_speed
        else:
            self._cooler_speed = speed
            return self._cooler_speed
        
    def coolerSpeedInc(self) -> None:
        self._cooler_speed += 1
        if self._cooler_speed > 6:
            self._cooler_speed = 1
        print('Cooler Speed:', self._cooler_speed)
    
    def brighness(self, scale: int | None = None) -> int:
        print('Set brightness:', scale)
        if scale == None:
            return self._brightness
        else:
            self._brightness = scale
            if self._brightness <= 10:
                self._brightness = 10
            if self._brightness > 100:
                self._brightness = 100
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
            print('Power enable:', state)
            self._modul_enable = state
            self._start.set_value(self._modul_enable)
            if state == True:
                self._dfplayer.play(folder = 1, file = 1) # Music start
            else:
                self._dfplayer.stop()
            return self._modul_enable

            
    def setColorToRGB(self, color: str | None) -> None:
        try:
            if color == None:
                return self._last_color_name
            print('Change color:', color)
            self._last_color_name = color
            (r, g, b) = self.__rgb_data[color]
            self._last_color = [r, g, b]
            return [r, g, b]
        except KeyError:
            return None
        

    def setRGB2PWM(self, rgb):
        [r, g, b] = rgb
        scale_factor = self._brightness / 100
        r *= scale_factor
        g *= scale_factor
        b *= scale_factor
        self._redPWM.set_pwm(r)
        self._greenPWM.set_pwm(g)
        self._bluePWM.set_pwm(b)

        
    async def buzzerBeep(self, delay: int):
        print("Beep active!")
        self._buzzer.set_value(1)
        sleep(delay/1000)
        print("Beep inactive!")
        self._buzzer.set_value(0)
    
    def run(self):
        _thread.start_new_thread(self.__main__, ())

    def shutdown(self):
        self.running = False
    
    def __main__ (self):
        notice_timeout = ticks_ms()
        try:
            while self.running:
                self._volume_1_level = [self.lvl11.value(), self.lvl12.value(), self.lvl13.value()]
                self._volume_2_level = [self.lvl21.value(), self.lvl22.value(), self.lvl23.value()]
                self._volume_1_level = [not x for x in self._volume_1_level]
                self._volume_2_level = [not x for x in self._volume_2_level]
                sum_level1 = sum(self._volume_1_level)
                sum_level2 = sum(self._volume_2_level)
                if sum_level1 == 0 and sum_level2 == 0:
                    self.notice_charge_water = True
                    self._discharge_water = False
                if sum_level1 == 3 and sum_level2 == 3:
                    self._charge_water = False
                self._start.set_value(self._modul_enable)
                if self._modul_enable == True:
                    if self._mode == True:
                        if self._charge_water == True:
                            if sum_level1 <= 1:
                                self._pump1.set_value(True)
                            elif sum_level2 == 3:
                                self._pump1.set_value(False)
                            if sum_level2 <= 1:
                                self._pump2.set_value(True)
                            elif sum_level2 == 3:
                                self._pump2.set_value(False)
                        else:
                            self._pump1.set_value(False)
                            self._pump2.set_value(False)
                        
                        if self._discharge_water == True:
                            self._pump3.set_value(sum_level1 > 0)
                            self._pump4.set_value(sum_level2 > 0)
                        else:
                            self._pump3.set_value(False)
                            self._pump4.set_value(False)
                    else:
                        self._pump1.set_value(self._charge_water == True and sum_level1 <= 1)
                        self._pump2.set_value(self._discharge_water == True and sum_level1 > 0)
                    self.setRGB2PWM(self._last_color)
                    self._coolerPWM.set_pwm(self._cooler_speed)
                    if self.notice_charge_water:
                        if ticks_ms() - notice_timeout > 30000: # har 30 sekundda
                            print('Please! Charge volume of water!!!')
                            if self._dfplayer.is_playing() is True:
                                self._dfplayer.stop()
                            self._dfplayer.play(folder = 1, file = 2) # Suv tugaganda to'ldirish uchun ovozli bildirishnoma
                            notice_timeout = ticks_ms()
                else:
                    self._coolerPWM.set_pwm(0)
                    self.setRGB2PWM([0, 0, 0])
                sleep(0.1)
        except KeyboardInterrupt:
            print('Exit threading!')
            running = False

