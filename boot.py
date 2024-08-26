# boot.py -- run on boot-up
import network, utime

# Replace the following with your WIFI Credentials
ssid = 'ESP-AKA'
password = '123456789'

def do_connect():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    print('Connected! Network config:', ap.ifconfig())
    
print("Connecting to your wifi...")
do_connect()

