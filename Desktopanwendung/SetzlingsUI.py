# Dieses Programm erzeugt ein GUI, mit welchem sich die Setzlingsanlage von einem PC aus überwachen und steuern lässt.
# Dieses Programm wird NICHT auf den Raspberry Pico geladen.

from GUI import GUI
import threading

curVals = [0, 0, 0, "--"]
progVals = []
running = True

def run_gui(curValues, progValues):
    gui = GUI(updateInterval=1000, curValues=curValues, progValues=[])
    return

t1 = threading.Thread(target=run_gui, args=[curVals, progVals])
t1.start()

while t1.is_alive():
    curVals[0] = input("Neue Temperatur: \n")