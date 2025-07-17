import board
import random
from Sensoren import Temperature_humidity_sensor, Soilmoisturemeter
from Aktoren import Fan, Waterpump, Wateratomizer, Heatingmat, Light, Lampfan

class DummyDHT:
    def __init__(self):
        self.name = "Temperature_humidity_sensor"
        self.values = {"temperature": 0, "humidity": 1}
    
    def should_measure(self):
        return True
    
    def measure(self):
        self.values["temperature"] = random.randint(1, 100)
        self.values["humidity"] = random.randint(1, 100)
        return self.values
        
    def update_timestamp(self):
        pass

class DummySensor:
    def __init__(self, name):
        self.name = name

    def should_measure(self):
        return True
    
    def measure(self):
        return random.randint(1, 100)
         
    def update_timestamp(self):
        pass
        
#Sensoren Belegung  #3 = ZeitIntervall, in der Messungen ausgeführt werden, "kann nach belieben angepasst werden, könnte man noch in GUI implementieren"
sensor_temp = DummyDHT()
sensor_soil = DummySensor(name="Soilmoisturemeter")
sensors = [sensor_temp, sensor_soil]

#Aktoren Belegung
fan_inward = Fan("Lüfter_rein", board.GP19)  #phys. Pin 25
fan_outward = Fan("Lüfter_raus", board.GP20)  #phys. Pin 26
atomizer = Wateratomizer("Zerstäuber", board.GP18)    #phys. Pin 24
pump = Waterpump("Wasserpumpe", board.GP14)      #phys. Pin 19
heatingmat = Heatingmat("Heizmatte", board.GP16) #phys. Pin 21
light = Light("Licht", board.GP15) #phys. Pin 20
lampfan = Lampfan("Lampenlüfter", board.GP12) #phys. Pin 16