# Modul für sämtliche Aktor-Klassen

from abc import ABC, abstractmethod

#Abstrakte Klasse der Aktoren
class Actors(ABC):
        def __init__(self, name, pin, unit):  #kein @abstractmethod, da ich ja sonst bei jeder Unterklasse nen Init deklarieren müsste
                self.name = name
                self.pin = pin
                self.unit = unit
                self.state = False   #False weil ich es ja IMMER auf False setze, wäre quatsch auf State zu setzen

        @abstractmethod
        def on(self): #alle Klassen der Aktoren müssen An und Aus gehen
            pass
        
        @abstractmethod
        def off(self): 
            self.state = False
            pass

#Unterklasse Aktoren:
class fan(Actors):
    def on(self):
        self.state = True
        print("Hallo")
    def off(self):
        self.state = False
        print(self.pin)
            
        
lufter = fan("lufter", 2, "l")
lufter.on()
    
