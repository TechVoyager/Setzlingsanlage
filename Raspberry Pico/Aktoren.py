import board
import digitalio

#Simulierte abstrakte Klasse der Aktoren
class Actors():
        def __init__(self, name, pin):  #kein @abstractmethod, da ich ja sonst bei jeder Unterklasse nen Init deklarieren müsste
                self.name = name
                self.pin = pin
                self.state = False   #False weil ich es ja IMMER auf False setze, wäre quatsch auf State zu setzen
                self.pin_obj = digitalio.DigitalInOut(pin)
                self.pin_obj.direction = digitalio.Direction.OUTPUT


        def on(self): #alle Klassen der Aktoren müssen An und Aus gehen 
            raise NotImplementedError("Jeder Aktor muss angeschaltet werden!!")
        
        def off(self): 
            raise NotImplementedError("Jeder Aktor muss angeschaltet werden!!")

#Unterklasse Aktoren:
class Fan(Actors):
    def on(self):
        self.state = True
        self.pin_obj.value = True
        print("Lüfter läuft")

    def off(self):
        self.state = False
        self.pin_obj.value = False
        print("Lüfter hört auf")

    def set_speed(self, speed_percent):
        #für die Verbesserung mit PWM-Fähigen Aktoren
        pass

class Lampfan(Actors):
    def on(self):
        self.state = True
        self.pin_obj.value = True
        print("Lampenlüfter läuft")

    def off(self):
        self.state = False
        self.pin_obj.value = False
        print("Lampenlüfter hört auf")

    def lampfan_active(self):
        if Light.state == True:
                self.on()
        else:
                self.off()

class Waterpump(Actors):
    def on(self):
        self.state = True
        self.pin_obj.value = True
        print("Wasserpumpe läuft")
    def off(self):
        self.state = False
        self.pin_obj.value = False
        print("Wasserpumpe hört auf")    
    def set_speed(self, speed_percent):
        #für die Verbesserung mit PWM-Fähigen Aktoren
        pass
        

class Wateratomizer(Actors):
    def on(self):
        self.state = True
        self.pin_obj.value = True
        print("Wasserzerstäuber läuft")
    def off(self):
        self.state = False
        self.pin_obj.value = False
        print("Wasserzerstäuber hört auf")   
    def set_speed(self, speed_percent):
        #für die Verbesserung mit PWM-Fähigen Aktoren
        pass

class Heatingmat(Actors):
    def on(self):
          self.state = True
          self.pin_obj.value = True # ist ein Befehl
          print("Heizmatte ist an")
    def off(self):
          self.state = False
          self.pin_obj.value = False
          print("Heizmatte ist aus")
    def set_speed(self, speed_percent):
        #für die Verbesserung mit PWM-Fähigen Aktoren
        pass  
     
#speed_percent : Stellgröße vom pid zwischen 0 und 100, gibt an wie stark der Actro angesteuert wird

class Light(Actors):
    def on(self):
          self.state = True
          self.pin_obj.value = True
          print("Licht ist an")
    def off(self):
          self.state = False
          self.pin_obj.value = False
          print("Licht ist aus")
    def set_speed(self, speed_percent):
        #für die Verbesserung mit PWM-Fähigen Aktoren
        pass
