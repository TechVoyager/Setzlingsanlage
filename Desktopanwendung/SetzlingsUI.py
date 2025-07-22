# Dieses Programm erzeugt ein GUI, mit welchem sich die Setzlingsanlage von einem PC aus überwachen und steuern lässt.
# Dieses Programm wird NICHT auf den Raspberry Pico geladen.

from GUI import GUI, SerialInterface
import threading


# Das hier sind Defaultwerte, welche an beide Klassen übergeben werden und angezeigt werden, bis die Initialisierung abgeschlossen wurde.
# Der Grund, warum alle Daten nochmal in einer Liste verpackt sind, ist mehrstufig:
# 1. 
curVals = [{"air_temperature": 25, "air_humidity": 50, "soil_temperature": 25, "soil_moisture": 50, "light_state": "aus"}]
availableProfiles = [{'Rosen': {'S_Luftfeuchte': 65, 'S_Lufttemperatur': 20, 'P_Bodenfeuchte': 65, 'P_Luftfeuchte': 65, 'S_Nachtdauer': 10, 'S_Tagdauer': 10, 'P_Lufttemperatur': 22, 'S_Bodentemperatur_nacht': 18, 'P_Nachtdauer': 10, 'S_Bodentemperatur_tag': 20, 'P_Tagdauer': 8, 'P_Bodentemperatur_tag': 22, 'P_Bodentemperatur_nacht': 18, 'Pflanzenart': 'Rosen', 'S_Bodenfeuchte': 60}, 'Erdbeeren': {'S_Luftfeuchte': 50, 'S_Lufttemperatur': 20, 'P_Bodenfeuchte': 65, 'P_Luftfeuchte': 60, 'S_Nachtdauer': 12, 'S_Tagdauer': 12, 'P_Lufttemperatur': 22, 'S_Bodentemperatur_nacht': 16, 'P_Nachtdauer': 10, 'S_Bodentemperatur_tag': 21, 'P_Tagdauer': 14, 'P_Bodentemperatur_tag': 20, 'P_Bodentemperatur_nacht': 16, 'Pflanzenart': 'Erdbeeren', 'S_Bodenfeuchte': 50}}]
selectedPlant = ["Rosen"]
curProfile = [availableProfiles[0]['Rosen']]
# "statusFlags" ist ein dict, welches die Zustände des aktuellen Programms enthält: 
# "auto" für den Automatikmodus, "unsentData" als Signal, dass Daten zum Raspi übertragen werden sollen
# "connected" für den Zustand der seriellen Schnittstelle, "running" für den Zustand des GUIs
statusFlags = {"auto": True, "unsentData": False, "connected": False, "running": True}


def run_gui(curVals, curProfile, availableProfiles, selectedPlant, statusFlags):
    gui = GUI(curVals, curProfile,  availableProfiles, selectedPlant, statusFlags, updateInterval=1000)


def run_serial(curVals, curProfile, availableProfiles, selectedPlant, statusFlags):   
    connection = SerialInterface(curVals, curProfile, availableProfiles, selectedPlant, statusFlags)


t1 = threading.Thread(target=run_gui, args=[curVals, curProfile, availableProfiles, selectedPlant, statusFlags])
t2 = threading.Thread(target=run_serial, args=[curVals, curProfile, availableProfiles, selectedPlant, statusFlags])
t1.start()
t2.start()

t1.join()
t2.join()