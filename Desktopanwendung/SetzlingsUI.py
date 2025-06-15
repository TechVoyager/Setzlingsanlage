# Dieses Programm erzeugt ein GUI, mit welchem sich die Setzlingsanlage von einem PC aus überwachen und steuern lässt.
# Dieses Programm wird NICHT auf den Raspberry Pico geladen.

from GUI import GUI, SerialInterface
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


def run_serial(curValues, progValues, auto, availableProfiles, selectedPlant, unsentDataFlag, connected):
    connection = SerialInterface(curValues, progValues, auto, availableProfiles, selectedPlant, unsentDataFlag, connected)


t1 = threading.Thread(target=run_gui, args=[curVals, progVals, auto, availableProfiles, selectedPlant])
t2 = threading.Thread(target=run_serial, args=[curVals, progVals, auto, availableProfiles, selectedPlant, unsentDataFlag, connected])
t1.start()
t2.start()

t1.join()
t2.join()