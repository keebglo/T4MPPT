import spidev
import time

# Define Variables
delay = 0.5
ldr_channel = 0

voltage_channel = 1


# Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)

#spi1 = spidev.SpiDev()
#spi1.open(0, 1)


def readadc(adcnum):
    
    spi.max_speed_hz = 1350000
    if adcnum > 3 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def readadc_voltage(adcnum1, vref = 5):
    if adcnum1 > 3 or adcnum1 < 0:
        return -1
        
    spi.max_speed_hz = 10000  
    r = spi.xfer2([1, 8 + adcnum1 << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
   
    percent = (data)/10.23 
    voltage = (percent/100.0) * 5.5
    
    
    return voltage
    


while True:
   
    ldr_value = readadc(ldr_channel)
    print
    "---------------------------------------"
    print("PhotoResistor Value: %d" % ldr_value)
    #time.sleep(delay)
    voltage_value = readadc_voltage(voltage_channel)
    print
    "---------------------------------------"
    print("voltage Value: ", round(voltage_value,4))
    time.sleep(delay)
 