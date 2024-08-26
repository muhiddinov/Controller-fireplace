from machine import PWM, Pin

class GPIOModule:
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.gpio_pin = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.gpio_pin.value()
    
    def toggle(self):
        self.gpio_pin.value(not self.get_value())
        
        
class PWMModule:
    def __init__(self, pinNumber, freq=5000):
        self.pwm = PWM(Pin(pinNumber, Pin.OUT), freq)
        self._duty_attr = 65535
        self._duty_cycle = 0
        self.pwm.duty_u16(int(self._duty_cycle))
        
    def get_value(self):
        return int(self._duty_cycle)
    
    
    def set_pwm(self, duty):
        self._duty_cycle = duty / 100 * self._duty_attr
        self.pwm.duty_u16(int(self._duty_cycle))
        
        