import time
from hardware_setup import sensor_temp, sensor_soil, fan1, fan2, atomizer, pumpe
from pid import PID

#Konstanten werden nicht verändert! (Deshalb Großbuchstaben)
KP_START = 0.0
KI_START = 0.0
KD_START = 0.0

KP_STEP = 0.1
KI_STEP = 0.05
KD_STEP = 0.05

KP_MAX = 2.0
KI_MAX = 0.5
KD_MAX = 0.5

#in Sekunden wie lange jeder Parametersatz getestet wird
TEST_DURATION = 10  

#Zeitintervall zw. 2 Messungen (z.B. 2 Sekunden für DHt11)
MEASURE_INTERVALL_S = 2.0

#ab wann wird ein Aktor aktiviert in Prozent(0-100)
OUTPUT_THRESHOLD = 50

#keine Steuerung bei minimalem Fehler (z.B. 1 Grad), in welchem Bereich soll nichts passieren 
DEADZONE = 1.0 

#Sollwert
setpoint = 25

#Kommazahlen zürückgeben für die Schleife
def drange(start, stop, step):
    while start <= stop:
        yield round(start, 3)
        start += step

#testen wie gut bestimmte PID kombi funktioniert
def evaluate_pid(pid, sensor, actuator, setpoint):
    error_sum = 0           #Summe aller Fehler (Abweichungen vom Sollwert)^
    last_measure_time = 0   #letzter Messzeitpunkt 
    start_time = time.monotonic()   #Startzeitpunkt des Testlaufs

    while time.monotonic() - start_time < TEST_DURATION: #während die zeitdif kleiner als Parametersatz...
        now = time.monotonic()                           #aktuelle Zeit
        
        if now - last_measure_time >= MEASURE_INTERVALL_S:
            last_measure_time = now

            sensor_value = sensor.measure()  #sensor einlesen
            error = setpoint - sensor_value
            abs_error = abs(error)  #abs gibt den wert (error ohne vorzeichen also +/- zurück immmer +)
            error_sum += abs_error            #Summierter Fehler über Zeit (halt von der Sensorzeit)

            #Deadzone ist ein Bereich in dem nichts passieren soll. Sensor hat Toleranzen usw.
            if abs_error > DEADZONE:
                output = pid.compute(sensor_value)  #output = Stellgröße
                #nur wenn Steuerwert groß genug ist: mind. wert
                if output > OUTPUT_THRESHOLD:
                    actuator.set_speed(output)
                else:
                    actuator.off()
                    
            else:
                actuator.off()
                #Fehler liegt in der Deadzone also passiert auch nichtsi

        #aktor nach Testlauf auschalten
        actuator.off()
        return  error_sum

#alle Kombis ausprobieren und die beste merken
def auto_tune_pid(pid, sensor, actuator, setpoint):
    best_error = float("inf")  #float("inf") ist eine unendlich große Zahl (kann auch mit-negativ sein) der Fehler startet unendlich groß damit man ihn direkt unterscheiden kann vom eigentlichen
    best_params = (0, 0, 0)     #anfangswerte verändern sich

    #beste Kombination finden:
    for kp in drange(KP_START, KP_MAX, KP_STEP):
        for ki in drange(KI_START, KI_MAX, KI_STEP):
            for kd in drange(KD_START, KD_MAX, KD_STEP):
                pid.Kp = kp
                pid.Ki = ki
                pid.Kd = kd
                print(f"Teste Kp = {kp}, Ki = {ki}, Kd = {kd}")
                #PID Kombi testen:
                error = evaluate_pid(pid, sensor, actuator, setpoint)
                if error < best_error:
                    best_error = error
                    best_params = (kp, ki, kd)
    print(f" beste Parameter gefunden: Kp={best_params[0]}, Ki= {best_params[1]}, Kd= {best_params[2]} mit Fehler {best_error}")

    pid.Kp = best_params[0]
    pid.Ki = best_params[1]
    pid.Kd = best_params[2]

    print("die besten Parameter sind gesetzt")