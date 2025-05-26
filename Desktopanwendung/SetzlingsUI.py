# Dieses Programm erzeugt ein GUI, mit welchem sich die Setzlingsanlage von einem PC aus überwachen und steuern lässt.
# Dieses Programm wird NICHT auf den Raspberry Pico geladen.

from GUI import GUI
import threading

# curVals sind die aktuellen Messwerte, progVals die programmierten Soll-Werte
curVals = [0, 0, 0, "--"]
progVals = []
auto = True
availableProfiles = []
selectedPlant = []


def run_gui(curValues, progValues, auto, availableProfiles, selectedPlant):
    gui = GUI(updateInterval=1000, curValues=curValues, progValues=progValues, auto=auto, plantList=availableProfiles, selectedPlant=selectedPlant)
    return


t1 = threading.Thread(target=run_gui, args=[curVals, progVals, auto, availableProfiles, selectedPlant])
t1.start()

while t1.is_alive():
    print(auto)