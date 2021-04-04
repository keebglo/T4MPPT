import spidev
import time
from numpy import interp
from time import sleep
import RPi.GPIO as GPIO

# Define Variables
delay = 0.5
ldr_channel = 0
voltage_channel = 1


# Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
GPIO.setmode(GPIO.BCM)

def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    spi.max_speed_hz = 1350000
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


'''while True:
    ldr_value = readadc(ldr_channel)
    print
    "---------------------------------------"
    print("PhotoResistor Value: %d" % ldr_value)
    time.sleep(delay)
    voltage_value = readadc(voltage_channel)
    print
    "---------------------------------------"
    print("Voltage Value: %d" % voltage_value) '''
 