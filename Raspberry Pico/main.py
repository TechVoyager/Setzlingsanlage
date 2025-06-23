# Hauptprogramm  
#Automatik/manuell
#pid IN extra datei



import time

#from Aktoren import *
from Sensoren import *
#from Pflanzenprofil import *
#from SerInterface import *

#Sensoren belegung
sensor1 = Temperature_humidity_sensor("POS:B", board.GP15, 3)
sensor2 = Soilmoisturemeter("POS:A", board.GP28, 3)  #physisch pin 34
sensors = [sensor1, sensor2]

#Regelung muss nich eingestellt werden!
#Temperatur
pid_temp = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=25) #Sollwert 25Grad
#Bodenfeuchtigkeit
pid_soil = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=50) #Sollwert Luftfeuchtigkeit 50 Prozent
#Luftfeuchtigkeit
pid_air = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=30) #Sollwert Bodenfeuchtigkeit 30 Prozent

#Setpoint = Sollwert; kp = proportional; ki = Interval nähert sich; kd achtet auf die Fehler der Zeit


#testen automatisieren
class PID:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp   
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.last_error = 0
        self.integral = 0
        self.lasttime = time.monotonic()

    def compute(self, measured_value):
        current_time = time.monotonic()           #aktuelle Zeit
        delta = current_time - self.lasttime    #Zeitdiff...
        error = self.setpoint - measured_value  #Fehler

        self.integral += error * delta          #Summe aller Fehler während der Zeit

        if delta > 0: #Ableitung berechnen
            derivative = (error - self.last_error) / delta #Fehlerdifff geteilt durch Zeitdiff
        else:
            derivative = 0

        #PID Regelwert berechnen:
        p_value = self.kp * error
        i_value = self.ki * self.integral 
        d_value = self.kd * derivative
        output = p_value + i_value + d_value

        #aktuelle Werte wieder abspeichern
        self.last_error = error 
        self.lasttime = current_time

        return output #regelgröße damit z.B. wenn größer als 50 ist werden aktoren angesteuert
 
#Sensoren mit zeitabstand auslesen:
#value is None: Schutzmaßnahme falls sensor bissle spinnt
#Daten speichern 
while True:
        for s in sensors:
                if s.should_measure(): 
                        value = s.measure()  #Methode Messen aufrufen
                        print(f"{s.name} bei {s.location}: {value} {s.unit}") #Ausgabe der Werte
                        s.update_timestamp()
                        
                        if value is None:   
                            continue    
                        #Optimierungsmöglichkeit: max Fehler

                        if s.name == "Temperature_humidity_sensor":
                            temp = value["temperature"]
                            hum = value["humidity"]
                            output_temp = pid_temp.compute(temp)
                            output_hum = pid_air.compute(hum)
                            print(f"PID temp output: {output_temp}, PID hum output: {output_hum}")

                        elif s.name == "Soilmoisturemeter":
                            output_soil = pid_soil.compute(value)
                            print(f"PID Soil Moisture Output: {output_soil}")


if output_temp > 30:
     luefter.on()
else: 
     luefter.off()


#vielleicht noch min und max Outputoutput