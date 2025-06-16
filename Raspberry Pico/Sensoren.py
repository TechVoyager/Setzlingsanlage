"""# Modul für sämtliche Sensor-Klassen
#from abc import ABC, abstractmethod  Funktioniert nur auf dem PC!!!!
from machine import ADC, Pin  #funktioniert nur auf MicroPython!!! nicht auf dem PC mit normalem Python
from time import ticks_ms, ticks_diff 
#ticks_ms() gibt die aktuellen Millisekunden seit start zurück
#ticks_diff(a, b) #berechnet den Unterschied zw. zwei zeitpunkten
import dht #für DHT11 Temperatur und FTK Sensor 

class Sensor():
        def __init__(self, name, location, unit, interval_ms):
                self.name = name
                self.location = location
                self.unit = unit
                self.interval = interval_ms  #Zeitintervall in ms
                self.last_measurement = ticks_ms()  #Startzeitpunkt der letzten Messung

        def measure(self): #alle Unterklassen müssen die Funktion Messen haben!
                raise NotImplementedError("Die Methode Measure (Messen) muss unbedingt in jeder Sensor Klasse deklariert sein!!")
        #soll immer überschrieben werden!!, wenn sie trotzdem benutzt wird, wird ein Fehler ausgelöst!! #raise löst einen Fehler aus
        #irgendein Fehler hier bedeutet der Fehler, dass measure nicht implementiert wurde

        def should_measure(self):
                current_time = ticks_ms()  #aktuelle Zeit seit Start des Picos
                time_since_last = ticks_diff(current_time, self.last_measurement) #berechnet den Unterschied zw. aktueller und letzter Messzeit
                return time_since_last >= self.interval   #wenn der Unterschied der Messzeit größer oder gleich vom Interval ist wird True ausgegeben, sonst False
        
        def update_timestamp(self):
                self.last_measurement = ticks_ms() #der letzte Messwert wird neu aktualisiert
        



#Unterklasse Bodenfeutchitgkeitssensorik 
#kapazitiver Bodenfeuchtigkeitssensor V2.0.0 HW-390
#2 Leiterplatten da bildet sich ein elektrisches Feld wenn der Boden feucht ist = besseres leiten größere Kapazität, wenns trocken is anders herum.
#3,3V = PIN 36, GND Masse = 38,, AOUT liefter Spannung= 31: Trocken = 2,5-3V; Feucht = 1V-1,5V Nass = 0,2V-0,8V
#Sensor gibt 0= 0V bis 65535 = 3,3V zurück
#mit ADC (analog_Digital-Converter)
class Soilmoisturemeter(Sensor): #Bodenfeuchtigkeitsmesser

        def __init__(self, location, pin_gp, interval_ms):
                super().__init__("Soilmoisturemeter", location, "%", interval_ms)  #Die Einheit(unit) ist in Prozent angegeben #super macht, dass man nicht erneut die Elternklasse initialisieren muss also self.name z.B., da wir ja die Einheit festlegen)
                self.adc = ADC(Pin(pin_gp)) #ist zwar am Pin 31 aber ist GP26

        def measure(self):
               raw = self.adc.read_u16()  #Raspberry Pi Pico hat 12 Bit ADC aber MircoPython skaliert auf 16 Bit hoch #Rohwert (0-65535 lesen)
               percent = (raw / 65535) * 100  #wandelt die Zahl 0-65535 in Prozent um 
               return round(percent, 1) #wird noch auf eins gerundet
        
#DHT11 Temperatur und Feuchtigkeistssensor:
#flache seite aufm Tisch: VCC(3,3V oder 5V) ganz links; Data(Signal) in der Mitte; GND (Masse) ganz rechts
#Funktion: VCC bekommt Strom, Data sendet/empfängt. Beim ruhezustand fließt trotdem 3,3 V, mit nem Widerstand wird der Pin20 vor zu starkem Strom geschützt. 
# Der Sensor ist digital: Bei 0V wird data mit gnd verbunden... er schickt impulse 

class Temperature_humidity_sensor(Sensor): #Temperature and humidity sensor

        def __init__(self, location, pin_gp, interval_ms):
                super().__init__("Temperature_humidity_sensor", location, "%", interval_ms)
                self.sensor = dht.DHT11(Pin(pin_gp)) #Pin(15) bedeutet nutze den GPIO15 als Eingang, dht.DHT11 erzeugt ein Objekt, das weiß wie man mit DHT11 kommunizieren muss
                
        def measure(self):
                self.sensor.measure() #Sensor startet Messung
                temperature = self.sensor.temperature() #Temperatur in °C
                humidity = self.sensor.humidity() #Luftfeuchtigkeit in %
                return {"temperature": temperature, "humidity": humidity} #gibt dict. zurück mit Luftfeuchtigkeit und Temperatur

sensor = Temperature_humidity_sensor("POS:B", 15, 10000)
sensor2 = Soilmoisturemeter("POS:A", 29, 10000)
sensors = [sensor, sensor2]


while True:
        for s in sensors:
                if s.should_measure(): 
                        value = s.measure()  #Methode Messen aufrufen
                        print(f"{s.name} bei {s.location}: {value} {s.unit}") #Ausgabe der Werte
                        s.update_timestamp()

"""
from machine import Pin
import dht
from time import sleep

sensor = dht.DHT11(Pin(15))  # GPIO15

sleep(2)

while True:
    try:
        sensor.measure()
        print("Temperatur:", sensor.temperature(), "°C")
        print("Luftfeuchtigkeit:", sensor.humidity(), "%")
    except Exception as e:
        print("Fehler:", e)
        sleep(2)