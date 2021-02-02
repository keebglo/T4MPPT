import RPi.GPIO as GPIO
import time
import array as arr
GPIO.setmode(GPIO.BCM)

#Pin number declarations. We're using the Broadcom chip pin numbers.
	CurrentInputPin = 18	#GPIO 18, Pin 12
	VoltageInputPin = 23	#GPIO 23, Pin 16 
	VoltageOutputPin = 24	#GPIO 24, Pin 18
	TemperaturePin = 5		#GPIO 5, Pin 29
	IrradiancePin = 6		#GPIO 6, Pin 31
	pwmPin = 32				#GPIO 12 (PWM0), Pin 32
	PowerValue = arr.array(i, [0,0,0,0,0]
	VoltageValue = arr.array(i, [0,0,0,0,0]
	frequency = 100000000
	dutycycle = 50

#Initialization
	GPIO.setup(CurrentInputPin, GPIO.IN)
	GPIO.setup(VoltageInputPin, GPIO.IN)
	GPIO.setup(TemperaturePin, GPIO.IN)
	GPIO.setup(IrradiancePin, GPIO.IN)
	pulse = GPIO.PWM(pwmPin, frequency)
	pulse.start(25) #starts PWM at 25% duty cycle
	
#Last 5 power values held in array
    while(true)
    {
		sleep(60) #1 minute delay
        if (startAlgorithm) # Algorithm is to start,
        {
			PowerValueShift() #Push old values down array
			VoltageValueShift() #Push old values down
			VoltageValue[0] = VoltagePin;
			PowerValue[0] = CurrentPin * VoltagePin; #Calculate Power
			PrintValues() #Prints out as "00:00am, 0, 0, 0, 0, 0"
			
			#
			#Algorithm
			#
			
			#If PV(n) is not equal to PV(n-1)
			if PowerValue[0] != PowerValue[1])
			{
				if PowerValue[0] > PowerValue[1]
				{
					#If PV_v(n) > PV_v(n-1)
					if VoltageValue[0] > VoltageValue[1]
					{
						dutycycle -= 5
						pulse.ChangeDutyCycle(dutycycle)
					}
					#If PV(n) < PV(n-1)
					else
					{
						//Increase PWM
						dutycycle += 5
						pulse.ChangeDutyCycle(dutycycle)

					}
				}
				else
				{
					#If PV_v(n) > PV_v(n-1)
					if VoltageValue[0] > VoltageValue[1]
					{
						#Increase PWM
						dutycycle += 5
						pulse.ChangeDutyCycle(dutycycle)
					}
					#If PV(n) < PV(n-1)
					else
					{
						//Decrease PWM
						dutycycle -= 5
						pulse.ChangeDutyCycle(dutycycle)
					}
				}
			}
        }
    }
    return 0;
}

#Shifts current Power values down the array to hold previous values
def PowerValueShift()
{
	for i in range(4)
	{
		PowerValue[i] = PowerValue[i-1]
	}
}

#Shifts current Voltage values down the array to hold previous  values
def VoltageValueShift()
{
	for i in range(4)
	{
		VoltageValue[i] = VoltageValue[i-1]
	}
}

#Module to print out values
def PrintValues();
{
	with open('output.txt','w') as f:
		from datetime import datetime
		now = datetime.now()
		gettime = now.strftime("%H:%M:%S")
		print(gettime)
		print("\n")
		print(VoltagePin, CurrentPin, VoltagePin*CurrentPin, TemperaturePin, IrradiancePin,"\n")
}