# Dieses Programm erzeugt ein GUI, mit welchem sich die Setzlingsanlage von einem PC aus überwachen und steuern lässt.
# Dieses Programm wird NICHT auf den Raspberry Pico geladen.

from GUI import GUI, SerialInterface
import threading

# curVals sind die aktuellen Messwerte, progVals die programmierten Soll-Werte
curVals = [{"air_temperature": 25, "air_humidity": 50, "soil_temperature": 25, "soil_moisture": 50, "light_state": "aus"}]
progVals = {"P_Tagdauer": 2, "P_Nachtdauer": 3, "P_Bodentemperatur_tag": 6, 
            "P_Bodentemperatur_nacht": 5, "P_Lufttemperatur": 6, "P_Luftfeuchte": 7, "P_Bodenfeuchte": 8,
            "S_Tagdauer": 2, "S_Nachtdauer": 3, "S_Bodentemperatur_tag": 4, 
            "S_Bodentemperatur_nacht": 5, "S_Lufttemperatur": 6, "S_Luftfeuchte": 7, "S_Bodenfeuchte": 8}
availableProfiles = ["Rosen", "Erdbeeren"]
selectedPlant = [availableProfiles[0]]
curProfile = [{"Pflanzenart": selectedPlant, **progVals}]
# "statusFlags" ist ein dict, welches die Zustände des aktuellen Programms enthält: 
# "auto" für den Automatikmodus, "unsentData" als Signal, dass Daten zum Raspi übertragen werden sollen
# "connected" für den Zustand der seriellen Schnittstelle, "running" für den Zustand des GUIs
statusFlags = {"auto": True, "unsentData": False, "connected": False, "running": True}


def run_gui(curVals, curProfile, progVals, availableProfiles, selectedPlant, statusFlags):
    gui = GUI(curVals, curProfile, progVals, availableProfiles, selectedPlant, statusFlags, updateInterval=1000)


def run_serial(curVals, curProfile, progVals, availableProfiles, selectedPlant, statusFlags):   
    connection = SerialInterface(curVals, curProfile, progVals, availableProfiles, selectedPlant, statusFlags)


t1 = threading.Thread(target=run_gui, args=[curVals, curProfile, progVals, availableProfiles, selectedPlant, statusFlags])
t2 = threading.Thread(target=run_serial, args=[curVals, curProfile, progVals, availableProfiles, selectedPlant, statusFlags])
t1.start()
t2.start()

t1.join()
t2.join()