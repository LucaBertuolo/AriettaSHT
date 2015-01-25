#AriettaSHT:
 Python module to use Sensirion SHT7x sensor on Acme Arietta G25.
 
 
##Dependencies:
 https://github.com/tanzilli/ablib
 
 
##Installation:
 ```
 # git clone git://github.com/LucaBertuolo/AriettaSHT7x.git
 # cd AriettaSHT7x
 ~/AriettaSHT7x# python setup.py install
 ```


##Code examples:
   ```
   from AriettaSHT7x import Sensirion
   SHT75 = Sensirion('PA22','PA21')
   print SHT75.read('TEMP')
   print SHT75.read('UR')
   ```
