# Modul für sämtliche Aktor-Klassen

from abc import ABC, abstractmethod

class Actors(ABC):
        @abstractmethod
        def __innit__(self, name, location, unit):
                self.name = name
                self.location = location
                self.unit = unit

        @abstractmethod
        def on(self): #alle Klassen der Aktoren müssen An und Aus gehen
            pass

        @abstractmethod
        def off(self): 
               pass
        



