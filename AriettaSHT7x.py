#    SHT7x.py
#
#
#    (C) 2015 Bertuolo Luca <berto990@hotmail.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    Example:
#       from AriettaSHT7x import Sensirion
#       SHT75 = Sensirion('PA22','PA21')
#       print SHT75.read('TEMP')
#       print SHT75.read('UR')
#
#






from ablib import Pin
import time

usleep = lambda x: time.sleep(x/1000000.0)




class Sensirion:


	def __init__(self,PIN_DATA,PIN_CLK):
		self.PIN_DATA = PIN_DATA
		self.PIN_CLK = PIN_CLK

	def read(self,measure):

                self.SendStart()
 		if measure == 'TEMP':
                	self.SendByte(0x03)
		elif measure == 'UR':
			self.SendByte(0x05)

                data = self.ReadData()

                if measure == 'TEMP':
                        return self.TempConversion(data)
                elif measure == 'UR':
                        return "%.2f" % self.HumConversion(data)


	def SendStart(self):

	        SHT_DATA_OUT = Pin(self.PIN_DATA,'OUTPUT')
        	SHT_CLK = Pin(self.PIN_CLK,'OUTPUT')

        	SHT_DATA_OUT.on()
        	SHT_CLK.on()
        	usleep(1)

        	SHT_DATA_OUT.off()
        	SHT_CLK.off()
        	usleep(1)

        	SHT_CLK.on()
       		SHT_DATA_OUT.on()
        	usleep(1)

        	SHT_CLK.off()


	def SendByte(self,byte):

		SHT_DATA_OUT = Pin(self.PIN_DATA,'OUTPUT')
		SHT_CLK = Pin(self.PIN_CLK,'OUTPUT')

		tmp = 0x80
		for i in range(8):
			if byte & tmp:
				SHT_DATA_OUT.on()
			else:
				SHT_DATA_OUT.off()
	
			SHT_CLK.on()
        		SHT_CLK.off()
		
			tmp = tmp/2

		SHT_CLK.on()



		SHT_DATA_IN = Pin(self.PIN_DATA,'INPUT')
		#ACK Check
		actualTime = time.time()
		ACK = SHT_DATA_IN.digitalRead()
		while ACK == 1 & ((actualTime + 0.1) > time.time()):
			ACK = SHT_DATA_IN.digitalRead()
		SHT_CLK.off()

		#Wait conversion Start
		actualTime = time.time()
		ACK = SHT_DATA_IN.digitalRead()
        	while ACK == 0 & ((actualTime + 0.1) > time.time()):
        	        ACK = SHT_DATA_IN.digitalRead()


		#Wait conversion End       
		actualTime = time.time()
		ACK = SHT_DATA_IN.digitalRead()
        	while ACK == 1  & ((actualTime + 0.5) > time.time()):
                	ACK = SHT_DATA_IN.digitalRead()
		

		
	def ReadData(self):

		SHT_CLK = Pin(self.PIN_CLK,'OUTPUT')
		SHT_DATA_IN = Pin(self.PIN_DATA,'INPUT')

		#Read 8 MSB	
		byte = 0
		for i in range(8):
			SHT_CLK.on()
			byte = byte * 2 + SHT_DATA_IN.digitalRead()
			SHT_CLK.off()

		#ACK
		actualTime = time.time()
		ACK = SHT_DATA_IN.digitalRead()
		while ACK == 0 & ((actualTime + 0.1) > time.time()):
		        ACK = SHT_DATA_IN.digitalRead()


		SHT_DATA_OUT = Pin(self.PIN_DATA,'OUTPUT')
		SHT_DATA_OUT.off()
		usleep(1)
		SHT_CLK.on()
		usleep(400)
		SHT_CLK.off()
		SHT_DATA_IN = Pin(self.PIN_DATA,'INPUT')

		#Read 8 LSB
		for i in range(8):
			SHT_CLK.on()
		        byte = byte * 2 + SHT_DATA_IN.digitalRead() 
		        SHT_CLK.off()


		#CRC
		SHT_DATA_OUT = Pin(self.PIN_DATA,'OUTPUT')
		SHT_DATA_OUT.on()
		SHT_CLK.on()
		usleep(400)
		SHT_CLK.off()
		SHT_DATA_OUT.off()


		return byte


	def TempConversion(self,Temp):
		D1 = -39.7
		D2 = 0.01

		return (D1 + D2*Temp)


	def HumConversion(self,Hum):
		C1 = -2.0468
		C2 = 0.0367
		C3 = -1.5955E-6

		return C1 + (C2*Hum)+(C3*Hum*Hum)
