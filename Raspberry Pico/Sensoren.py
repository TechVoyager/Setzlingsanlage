# Modul für sämtliche Sensor-Klassen
from abc import ABC, abstractmethod

class Sensor(ABC):
        @abstractmethod
        def __innit__(self, name, location, unit):
                self.name = name
                self.location = location
                self.unit = unit

        def masure(self): #alle Unterklassen müssen die Funktion Messen haben!
            pass