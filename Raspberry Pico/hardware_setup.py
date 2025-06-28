import board
from Sensoren import Temperature_humidity_sensor, Soilmoisturemeter
from Aktoren import Fan, waterpump, Wateratomizer, Heatingmat, Light

#Sensoren Belegung  #3 = ZeitIntervall, in der Messungen ausgeführt werden, "kann nach belieben angepasst werden, könnte man noch in GUI implementieren"
sensor_temp = Temperature_humidity_sensor("POS:B", board.GP22, 3)
sensor_soil = Soilmoisturemeter("POS:A", board.GP28, 3)  #physisch pin 34
sensors = [sensor_temp, sensor_soil]

#Aktoren Belegung
fan1 = Fan("Lüfter1", board.GP21)  #phys. Pin 27
fan2 = Fan("Lüfter2", board.GP20)  #phys. Pin 26
atomizer = Wateratomizer("Zerstäuber", board.GP19)    #phys. Pin 25
pumpe = waterpump("Wasserpumpe", board.GP14)      #phys. Pin 19
heatingmat = Heatingmat("Heizmatte", board.GP22) #phys. Pin 29
light = Light("Licht", board.GP15) #phys. Pin 20