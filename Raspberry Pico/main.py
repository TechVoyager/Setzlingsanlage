# Hauptprogramm  
#pid IN extra datei



import time
import board

# Exakte Klassen importieren, nicht automatisch alles
from Pflanzenprofil import *
from SerInterface import SerialInterface
from pid import PID 
from hardware_setup import sensor_temp, sensor_soil, sensor_soiltemp, fan_inward, fan_outward, atomizer, pump, lampfan, sensors, heatingmat, light


#Klassenelemente erstellen
plantprofile = Pflanzenprofil()
serial = SerialInterface()

#Variablen
#Variablen zu Pflanzenarten
plantspecies = "Erdbeeren" # wird geändert durch GUI
seed = True # seed == True : Samen -- seed == False: Setzling
target_values = plantprofile.gib_Pflanzenwerte(plantspecies, seed)
time_since_start = time.monotonic() # Zahl in s -> neuer Wert zuweisen wenn neue Pflanzenart ausgewählt wurde

update_time_plantvalues = 5 
number_of_days = 0
cur_meassurements = {"air_temperature": 25, "air_humidity": 50, "soil_temperature": 25, "soil_moisture": 50, "light_state": "aus"}
pid_values = {"air_temperature": 0, "air_humidity": 0, "soil_temperature": 0, "soil_moisture": 0}

#Regelung muss nich eingestellt werden!
#Temperatur

pid_soil_temp = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=target_values["Bodentemperatur_tag"]) #Sollwert 25Grad
pid_soil_temp.min_output = 0
pid_soil_temp.max_output = 100

#Bodenfeuchtigkeit
pid_soil_moisture = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=target_values["Bodenfeuchte"]) #Sollwert Luftfeuchtigkeit 50 Prozent
pid_soil_moisture.min_output = 0
pid_soil_moisture.max_output = 100
#Luftfeuchtigkeit
pid_humidity = PID(kp=1.0, ki=0.1, kd=0.05, setpoint=target_values["Luftfeuchte"]) #Sollwert Bodenfeuchtigkeit 30 Prozent
pid_humidity.min_output = 0
pid_humidity.max_output = 100

#Setpoint = Sollwert; kp = proportional; ki = Interval nähert sich; kd achtet auf die Fehler der Zeit

#Sensoren mit zeitabstand auslesen:
#value is None: Schutzmaßnahme falls sensor bissle spinnt
#Daten speichern 
while True:
        """
        1. Sensoren auslesen
        2. Sensorwerte verarbeiten -> PID-Wert erstellen
        3. Aktoren ansteuern
        4. Kommunikation mit GUI
        """
        # nach 5 Tagen neue Werte für die Pflanze ins dict schreiben (von Samen zu Setzling)
        if plantspecies != "manuell":
            if number_of_days >= update_time_plantvalues:
                target_values = plantprofile.gib_Pflanzenwerte(plantspecies, False)
            else:
                target_values = plantprofile.gib_Pflanzenwerte(plantspecies, True)
        # Sensoren auslesen
        for s in sensors:
                if s.should_measure(): 
                        value = s.measure()  #Methode Messen aufrufen
                        s.update_timestamp()
                        
                        if value is None:   
                            continue    
                        #Optimierungsmöglichkeit: max Fehler

                        if s.name == "Temperature_humidity_sensor":
                            temp = value["temperature"]
                            hum = value["humidity"]
                            cur_meassurements["air_temperature"] = temp
                            cur_meassurements["air_humidity"] = hum
                            pid_values["air_humidity"] = pid_humidity.compute(hum)     #PID Wert von 0-100
                            print(f"PID temp output: {pid_values["air_temperature"]}, PID hum output: {pid_values["air_humidity"]}")

                        elif s.name == "Soilmoisturemeter":
                            cur_meassurements["soil_moisture"] = value
                            pid_values["soil_moisture"] = pid_soil_moisture.compute(value)
                            print(f"PID Soil Moisture Output: {pid_values["soil_moisture"]}")

                        elif s.name == "SoilTemperaturesensor":
                            cur_meassurements["soil_temperature"] = value
                            pid_values["soil_temperature"] = pid_soil_temp.compute(value)
                            print(f"PID Soil Temperature Output: {pid_values["soil_temperature"]}")

        # TO-DO: Schwellenwerte sind NICHT KORREKT, MÜSSEN ANGEPASST WERDEN
        if pid_values["soil_moisture"] > 50:
            pump.on()
        else:
            pump.off()

        # TO-DO: Schwellenwerte sind NICHT KORREKT, MÜSSEN ANGEPASST WERDEN
        if pid_values["soil_temperature"] > 50:
            heatingmat.on()
        else:
            heatingmat.off()
        
        # TO-DO: Schwellenwerte sind NICHT KORREKT, MÜSSEN ANGEPASST WERDEN
        if pid_values["air_humidity"] > 50:
            fan_inward.on()
            fan_outward.on()
        else:
            fan_inward.off()
            fan_outward.off()

        # TO-DO: Schwellenwerte sind NICHT KORREKT, MÜSSEN ANGEPASST WERDEN
        if pid_values["air_humidity"] < 50:
            atomizer.on()
        else:
            atomizer.off()
        
        cur_time_light = time.monotonic()
        if ((cur_time_light - time_since_start) - number_of_days*24*60*60) > target_values["Tagdauer"] * 60 * 60:
            # Wird ausgeführt, wenn der Tag vorbei ist
            light.off()
            cur_meassurements["light_state"] = "aus"
        if (((cur_time_light - time_since_start) - number_of_days*24*60*60) - target_values["Tagdauer"] * 60 * 60) > target_values["Nachtdauer"] * 60 * 60:
            # Wird ausgeführt, wenn die Nacht vorbei
            light.on()
            cur_meassurements["light_state"] = "an"
            number_of_days += 1

        # HIER JETZT: Kommunikation mit GUI
        if serial.connection.in_waiting > 0:
            command = serial.read()

            if command == "sync":
                serial.send("sync")
            elif command == "getConfig":
                data = {"profiles": plantprofile.Pflanzen_dict, "selectedPlant": plantspecies}
                serial.send(data)
            elif command == "setProfile":
                profile = serial.readBigData()
                if profile["Pflanzenart"] == "manuell":
                    plantspecies = "manuell"
                    target_values = profile
                else:
                    plantspecies = profile["Pflanzenart"]
                serial.send(plantspecies)
            elif command == "getMeasurements":
                serial.send(cur_meassurements)
            else:
                serial.send("unprocessed:"+command)

        time.sleep(1)



# mit pid_values["air_temperature"] -> Zersteuber und Lüfter regeln

# PID-Wert kann auch negativ sein!

