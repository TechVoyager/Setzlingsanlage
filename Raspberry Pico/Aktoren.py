import board
import digitalio
import time

#Abstrakte Klasse der Aktoren
class Actors():
        def __init__(self, name, pin, unit):  #kein @abstractmethod, da ich ja sonst bei jeder Unterklasse nen Init deklarieren müsste
                self.name = name
                self.pin = pin
                self.unit = unit
                self.state = False   #False weil ich es ja IMMER auf False setze, wäre quatsch auf State zu setzen

        def on(self): #alle Klassen der Aktoren müssen An und Aus gehen
            raise NotImplementedError("Jeder Aktor muss angeschaltet werden!!")
        
        def off(self): 
            self.state = False
            raise NotImplementedError("Jeder Aktor muss angeschaltet werden!!")

#Unterklasse Aktoren:
class Fan(Actors):
    def on(self):
        self.state = True
        print("Lüfter läuft")
    def off(self):
        self.state = False
        print("Lüfter hört auf")

class waterpump(Actors):
    def on(self):
        self.state = True
        print("Wasserpumpe läuft")
    def off(self):
        self.state = False
        print("Wasserpumpe hört auf")    


class Wateratomizer(Actors):
    def on(self):
        self.state = True
        print("Wasserzerstäuber läuft")
    def off(self):
        self.state = False
        print("Wasserzerstäuber hört auf")   

#class Heatingmat(Actors):
   

#class Light(Actors):
    


    
