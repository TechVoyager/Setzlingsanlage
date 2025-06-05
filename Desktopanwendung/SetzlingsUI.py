# Dieses Programm erzeugt ein GUI, mit welchem sich die Setzlingsanlage von einem PC aus überwachen und steuern lässt.
# Dieses Programm wird NICHT auf den Raspberry Pico geladen.

from GUI import GUI
import threading

# curVals sind die aktuellen Messwerte, progVals die programmierten Soll-Werte
curVals = {"airTemp": 0, "humidity": 0, "moisture": 0, "lightState": "aus"}
progVals = []
auto = [True]
availableProfiles = ["Tomate", "Erdbeere"]
selectedPlant = ["Tomate"]
unsentDataFlag = [False]
connected = [False]


def run_gui(curValues, progValues, auto, availableProfiles, selectedPlant):
    gui = GUI(updateInterval=1000, curValues=curValues, progValues=progValues, auto=auto, plantList=availableProfiles, selectedPlant=selectedPlant, unsentDataFlag=unsentDataFlag, connected=connected)
    return


t1 = threading.Thread(target=run_gui, args=[curVals, progVals, auto, availableProfiles, selectedPlant])
t1.start()

while t1.is_alive():
    connected[0] = bool(input())
    print(connected)