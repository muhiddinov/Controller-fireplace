import machine
import utime
from machine import Pin, Timer
import _thread

class Debounce:
    _btn: Pin | None
    _debounce_time: int | None
    _last_change_time: int = 50
    _btn_state: bool | None
    
    def __init__(self, callback:None, pinNumber:int|None, debounce:int=50, state:bool=False):
        if callback != None:
            self._callback = callback
        else :
            self._callback = self.dosomthing
        self._btn = Pin(pinNumber, Pin.IN, Pin.PULL_UP)
        self._btn.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.button_interrupt)
        self._debounce_time = debounce
        self._btn_state = state
        
    def dosomthing(self, pin):
        print("Debounce handler:", pin)

    def button_interrupt(self, pin):
        current_time = utime.ticks_ms()
        if current_time - self.last_change_time > self._debounce_time:
            with self._button_semaphore:
              self._btn_state = not self._btn_state
            self._last_change_time = current_time

    def button_task(self, timer):
        while True:
            try:
                with self._button_semaphore:
                    if self._btn_state == True:
                        self._callback(self._btn)
                        print('Task handle')
                    self._btn_state = False
                utime.sleep_ms(10)
            
            except KeyboardInterrupt:
                break

    def run(self):
        self._button_semaphore = _thread.allocate_lock()
        self.timer = Timer(0)
        self.timer.init(period=10, mode=Timer.PERIODIC, callback=self.button_task)

