#testen automatisieren
import time
from hardware_setup import sensor_temp, sensor_soil, fan_inward, fan_outward, atomizer, pump
#kp = Proportionalfaktor
#ki = Integralfaktor
#
class PID:
    def __init__(self, kp, ki, kd, setpoint, min_output=None, max_output=None):
        self.kp = kp   
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint  
        #setpoint = Sollwert

        self.last_error = 0 
        #vorheriger Fehlerwert
        self.integral = 0
        #Summe der Fehler 
        self.lasttime = time.monotonic()
        #letzte Zeitmessung

        self.min_output = None
        self.max_output = None
    
    def compute(self, measured_value):
        current_time = time.monotonic()           #aktuelle Zeit seit Start
        delta = current_time - self.lasttime    #Zeitdiff.. seit letzter Regelung
        error = self.setpoint - measured_value  #Fehler

        self.integral += error * delta          #Summe aller Fehler während der Zeit

        #Integralbegrenzung damit der I Anteil vom PID nicht zu groß wird (Anti_Windup)
        max_integral = 1000
        min_integral = -1000

        self .integral = max(min(self.integral, max_integral), min_integral)

        if delta > 0: #Ableitung berechnen
            derivative = (error - self.last_error) / delta #Fehlerdifff geteilt durch Zeitdiff
        else:
            derivative = 0


        #PID Regelwert berechnen:
        p_value = self.kp * error
        i_value = self.ki * self.integral 
        d_value = self.kd * derivative
        output = p_value + i_value + d_value

        #max gibt den größten wert zurück min den kleinsten
        if self.min_output is not None:
            output = max(self.min_output, output)

        if self.max_output is not None:
            output = min(self.max_output, output)

        #aktuelle Werte wieder abspeichern
        self.last_error = error 
        self.lasttime = current_time

        return output #regelgröße damit z.B. wenn größer als 50 ist werden aktoren angesteuertx


#vielleicht noch min und max Outputoutput