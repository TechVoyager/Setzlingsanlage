# Hauptprogramm

from Aktoren import *
#from Sensoren import *
from Pflanzenprofil import *
#from SerInterface import *
from Suche import *

# für die Zeitmessung nötig
from datetime import timedelta # nur timedelta importieren spart Speicherplatz
from datetime import datetime

# für die Pausezeiten
import time

#Variabeln
# Variabeln zu den Werten der Pflanzenart
Pflanzenart = ?????? #"Erdbeeren" # übergebener String vom Gui
Pflanzenprofil = Pflanzenprofil()
Pflanzenwerte_dict = Pflanzenprofil.gib_Pflanzenwerte(Pflanzenart)

Gießhaeufigkeit = int(Pflanzenwerte_dict['Gießhaeufigkeit']) # int(): aus string int-Werte machen
Tagdauer = int(Pflanzenwerte_dict['Tagdauer'])
Nachtdauer = int(Pflanzenwerte_dict['Nachtdauer'])
Bodentemperatur_tag = int(Pflanzenwerte_dict['Bodentemperatur_tag'])
Bodentemperatur_nacht = int(Pflanzenwerte_dict['Bodentemperatur_nacht'])
Soll_lufttemp = int(Pflanzenwerte_dict['Lufttemperatur)']) 
Soll_luftfeuchte = int(Pflanzenwerte_dict['Luftfeuchte'])
Soll_bodenfeuchte = int(Pflanzenwerte_dict['Bodenfeuchte'])

# Zeit Variabeln
    # Startzeit = str(datetime.now()) 
    # besser 
# man kann damit rechnen; falls man es ausgeben will mit str(startzeit) in einen string umwandeln
Startzeit = datetime.now() # ist ein datetime.datetime-objekt; Bspw. 2025-06-11 12:03:02.704167
aktuelleZeit = ???

# Sensor Variabeln
Lufttemp =  # gleicher Sensor wie Luftfeuchte
Luftfeuchte = 
Bodenfeuchte = 


# Heizmatte anschalten
# Heizmattenklassenelement erzeugen
Heizung = heat(name = "Heizung", pin = 22, unit = "°C")
if Lufttemp < Soll_lufttemp:
    Heizung.on()
elif Lufttemp >= Soll_lufttemp:
    Heizung.off()

# LED anschalten
# LEDElement erzeugen
Licht = light(name = "Licht", pin = 15, unit = "h")
#Licht am Anfang erstmal aus
Licht.off()
letzter_wechsel = Startzeit
Dauer = 0  # in Stunden

while True:
    jetzt = datetime.now()
    differenz = jetzt - letzter_wechsel
    # Licht an: Dauer = Tagdauer; Licht aus: Dauer = Nachtdauer
    if Licht.state: # Licht.state = True wenn Licht an ist
        Dauer = Tagdauer
        if differenz >= timedelta(hours = Dauer):
            Licht.off()
            letzter_wechsel = jetzt # Zeitstempel aktualisieren
            print(f"LED ist jetzt aus (gewechselt um {jetzt.strftime('%H:%M:%S')})")

    elif Licht.state is False:
        Dauer = Nachtdauer
        if differenz >= timedelta(hours = Dauer):
            Licht.on()
            letzter_wechsel = jetzt # Zeitstempel aktualisieren
            print(f"LED ist jetzt an (gewechselt um {jetzt.strftime('%H:%M:%S')})")

    time.sleep(5*3600)  # damit die CPU nicht durchläuft, alle 5 Stunden prüfen
