import board
from Sensoren import Temperature_humidity_sensor, Soilmoisturemeter
from Aktoren import Fan, Waterpump, Wateratomizer, Heatingmat, Light, Lampfan

#Sensoren Belegung  #3 = ZeitIntervall, in der Messungen ausgeführt werden, "kann nach belieben angepasst werden, könnte man noch in GUI implementieren"
sensor_temp = Temperature_humidity_sensor("POS:B", board.GP13, 3)
sensor_soil = Soilmoisturemeter("POS:A", board.GP28, 3)  #physisch pin 34
sensors = [sensor_temp, sensor_soil]

#Aktoren Belegung
fan_inward = Fan("Lüfter_rein", board.GP19)  #phys. Pin 25
fan_outward = Fan("Lüfter_raus", board.GP20)  #phys. Pin 26
atomizer = Wateratomizer("Zerstäuber", board.GP18)    #phys. Pin 24
pump = Waterpump("Wasserpumpe", board.GP14)      #phys. Pin 19
heatingmat = Heatingmat("Heizmatte", board.GP16) #phys. Pin 21
light = Light("Licht", board.GP15) #phys. Pin 20
lampfan = Lampfan("Lampenlüfter", board.GP12) #phys. Pin 16