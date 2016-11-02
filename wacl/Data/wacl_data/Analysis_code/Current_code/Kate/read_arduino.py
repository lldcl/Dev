# Importing the serial data from Arduino onto the computer, without using DAQfactory. 
# Use the serial library:
import serial,os

ports = os.popen('ls /dev/tty.*').read().split('\n')
for i in ports: 
	if 'usb' in i:
		myport = i
		print 'selecting', myport
		
ser = serial.Serial(myport, 9600)
		
myfile =  open("test.txt", "a") 



while running = True: 
	data=ser.readline()
	myfile.write(data)
	print data	