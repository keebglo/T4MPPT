import spidev
import time

# Define Variables
delay = 0.5
ldr_channel = 0
current_channel = 1
thermistor_channel = 2

# Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)


def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


while True:
    ldr_value = readadc(ldr_channel)
    print
    "---------------------------------------"
    print("PhotoResistor Value: %d" % ldr_value)
    time.sleep(delay)
    current_value = readadc(current_channel)
    print
    "---------------------------------------"
    print("Current Value: %d" % current_value)
    thermistor_value = readadc(thermistor_channel)
    print
    "---------------------------------------"
    print("Thermistor Value: %d" % thermistor_value)