# Hauptprogramm  
#Automatik/manuell
#pid IN extra datei



import time
import board

from Aktoren import *
from Sensoren import *
from Pflanzenprofil import *
from SerInterface import *
from pid import PID 
from hardware_setup import sensor_temp, sensor_soil, fan1, fan2, atomizer, pumpe, sensors
#Regelung muss nich eingestellt werden!
#Temperatur
pid_temp = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=25) #Sollwert 25Grad
pid_temp.min_output = 0
pid_temp.max_output = 100

#Bodenfeuchtigkeit
pid_soil = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=50) #Sollwert Luftfeuchtigkeit 50 Prozent
pid_soil.min_output = 0
pid_soil.max_output = 100

#Luftfeuchtigkeit
pid_air = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=30) #Sollwert Bodenfeuchtigkeit 30 Prozent
pid_air.min_output = 0
pid_air.max_output = 100

#Setpoint = Sollwert; kp = proportional; ki = Interval nähert sich; kd achtet auf die Fehler der Zeit


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
                            output_temp = pid_temp.compute(temp)  #PID Wert von 0-100
                            output_hum = pid_air.compute(hum)     #PID Wert von 0-100
                            print(f"PID temp output: {output_temp}, PID hum output: {output_hum}")

                        elif s.name == "Soilmoisturemeter":
                            output_soil = pid_soil.compute(value)
                            print(f"PID Soil Moisture Output: {output_soil}")



