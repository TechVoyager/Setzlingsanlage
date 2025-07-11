import board   #geändert statt machine.pin
import analogio #geändert für machine
import adafruit_dht 
import time 
import math
imoort analogio
#abstrakte Klasse:
class Sensor():
        def __init__(self, name, location, unit, interval_s):
                self.name = name
                self.location = location
                self.unit = unit
                self.interval = interval_s  #Zeitintervall in s
                self.last_measurement = time.monotonic()  #Startet wie ticks_ms und zählt hoch in Sekunden
                

        def measure(self): #alle Unterklassen müssen die Funktion Messen haben!
                raise NotImplementedError("Die Methode Measure (Messen) muss unbedingt in jeder Sensor Klasse deklariert sein!!")
        #soll immer überschrieben werden!!, wenn sie trotzdem benutzt wird, wird ein Fehler ausgelöst!! #raise löst einen Fehler aus
        #irgendein Fehler hier bedeutet der Fehler, dass measure nicht implementiert wurde

        def should_measure(self):
                current_time = time.monotonic()  #aktuelle Zeit seit Start des Picos
                time_since_last = current_time - self.last_measurement #berechnet den Unterschied zw. aktueller und letzter Messzeit
                print(f"aktuelle Zeit: {current_time} ")
                print(f"times_since_last Zeit: {time_since_last} ")
                return time_since_last >= self.interval   #wenn der Unterschied der Messzeit größer oder gleich vom Interval ist wird True ausgegeben, sonst False
        
        def update_timestamp(self):
                self.last_measurement = time.monotonic() #der letzte Messwert wird neu aktualisiert
                print("passt")
        
#zahl wird immer größer bitte änern delta t


#Unterklasse Bodenfeutchitgkeitssensorik 
#kapazitiver Bodenfeuchtigkeitssensor V2.0.0 HW-390
#2 Leiterplatten da bildet sich ein elektrisches Feld wenn der Boden feucht ist = besseres leiten größere Kapazität, wenns trocken is anders herum.
#3,3V = PIN 36, GND Masse = 38,, AOUT liefter Spannung= 31: Trocken = 2,5-3V; Feucht = 1V-1,5V Nass = 0,2V-0,8V
#Sensor gibt 0= 0V bis 65535 = 3,3V zurück
#mit ADC (analog_Digital-Converter)
class Soilmoisturemeter(Sensor): #Bodenfeuchtigkeitsmesser

        def __init__(self, location, pin, interval_s):
                super().__init__("Soilmoisturemeter", location, "%", interval_s)  #Die Einheit(unit) ist in Prozent angegeben #super macht, dass man nicht erneut die Elternklasse initialisieren muss also self.name z.B., da wir ja die Einheit festlegen)
                self.adc = analogio.AnalogIn(pin)
        def measure(self):
               raw = self.adc.value  #Raspberry Pi Pico hat 12 Bit ADC aber MircoPython skaliert auf 16 Bit hoch #Rohwert (0-65535 lesen)
               percent = (raw / 65535) * 100  #wandelt die Zahl 0-65535 in Prozent um 
               return round(percent, 1) #wird noch auf eins gerundet
        
class SoilTemperaturesensor(Sensor): #Bodentemperatur, rknown ist der referenzwiderstand(10kOhm), beta Konstante des Nt´TC, t0 = Referenztemperatur in Grad
        def __init__(self, location, pin, interval_s, adc_max=65535, r_known = 10000, beta=3950, t0=25):
                super().__init__("SoilTemperaturesensor", location, "°C", interval_s)  #Die Einheit(unit) ist in Prozent angegeben #super macht, dass man nicht erneut die Elternklasse initialisieren muss also self.name z.B., da wir ja die Einheit festlegen)
                self.adc = analogio.AnalogIn(pin)
                self.adc_max = adc_max
                self.r_known = r_known
                self.beta = beta
                self.t0_kelvin = t0 + 273.15

        def adc_to_resistance(self, adc_value):
                if adc_value == 0:
                        return float("inf")
                #unendlicher Widerstand
                return self.r_known * (self.adc_max / adc_value -1)
        
        def resistance_to_temp(self, resistance == 0 or resistance == float("inf")):
                return None #keinen gültigen Wert
                ln = math.log(resistance / self.r_known)
                inv_t = (1/self.t0_kelvin) + (1 / self.beta) *len
                t_kelvin = 1 / inv_t
                returm t_kelvin - 273.15


        def measure(self):
                raw = self.adc.value  #Raspberry Pi Pico hat 12 Bit ADC aber MircoPython skaliert auf 16 Bit hoch #Rohwert (0-65535 lesen)
                resistance = self.adc_to_resistance(raw)
                temperature = self.resistance_to_temp(resistance)
                if temperature is None:
                        print(f"Ungültiger ADC WERT beim Sensor {self.name}, an {self.location}")
                        return None
                return round(temperature, 2)

        
#DHT11 Temperatur und Feuchtigkeistssensor:
#flache seite aufm Tisch: VCC(3,3V oder 5V) ganz links; Data(Signal) in der Mitte; GND (Masse) ganz rechts
#Funktion: VCC bekommt Strom, Data sendet/empfängt. Beim ruhezustand fließt trotdem 3,3 V, mit nem Widerstand wird der Pin20 vor zu starkem Strom geschützt. 
# Der Sensor ist digital: Bei 0V wird data mit gnd verbunden... er schickt impulse 

class Temperature_humidity_sensor(Sensor): #Temperature and humidity sensor

        def __init__(self, location, pin, interval_s):
                super().__init__("Temperature_humidity_sensor", location, "%", interval_s)
                self.sensor = adafruit_dht.DHT11(pin) #Pin(15) bedeutet nutze den GPIO15 als Eingang, dht.DHT11 erzeugt ein Objekt, das weiß wie man mit DHT11 kommunizieren muss
                
        def measure(self):
                try:          
                        self.sensor.measure() #Sensor startet Messung
                        temperature = self.sensor.temperature #Temperatur in °C
                        humidity = self.sensor.humidity  #Luftfeuchtigkeit in %
                        return {"temperature": temperature, "humidity": humidity} #gibt dict. zurück mit Luftfeuchtigkeit und Temperatur
                except RuntimeError as e:
                        print(f"Fehler beim Lesen ({self.name}, bei {self.location}, {e})")
                        return None

