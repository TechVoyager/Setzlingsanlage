import tkinter as tk
from tkinter import ttk
import os


class GUI:
    # Schriftstile, die in verschiedenen Funktionen gebraucht werden
    global smallText, boldText, normText, bigLabel, dirName
    smallText = ("System", "9")
    normText = ("System", "14")
    boldText = ("System", "14", "bold")
    bigLabel = ("System", "16", "bold")

    dirName = os.path.dirname(__file__)


    @staticmethod
    def datafield(parentFrame, descriptor: str, variable, unit: str, img: str, row: int):
        # Template für ein Widget, welches einen Datenpunkt zusammen mit einer Beschreibung, Einheit und einem Bild darstellt

        # Der Pfad zum Bild wird relativ zum Pfad dieses Skripts bestimmt
        filepath = os.path.join(dirName, img)
        image = tk.PhotoImage(file=filepath)

        dataframe = ttk.Frame(parentFrame, padding="5 15 5 15", style="Card")
        # Das Bild muss als Referenz gespeichert werden, da es sonst direkt garbage-collected wird
        dataframe.image = image
        dataframe.grid(row=row, sticky="w")
        dataframe.columnconfigure(1, minsize=40)
        dataframe.columnconfigure(2, minsize=100)

        ttk.Label(dataframe, image=image, padding="0 0 10 0").grid(column=0, row=0, rowspan=3, sticky="s")
        ttk.Label(dataframe, text=descriptor, font=smallText, padding="0 0 10 0").grid(column=1, row=0, columnspan=2, sticky="w")
        ttk.Label(dataframe, textvariable=variable, font=bigLabel).grid(column=1, row=1, sticky="w")
        ttk.Label(dataframe, text=unit, font=bigLabel).grid(column=2, row=1, sticky="w")


    def __init__(self, updateInterval, curValues, progValues, auto, plantList, selectedPlant):
        self.__updateInterval = updateInterval
        # Messwerte und Soll-Werte werden bei der Instanzierung als Listen übergeben, da diese per Referenz übergeben werden.
        # So liest die "update"-Funktion automatisch die neusten Werte, welche sie dann in das GUI schreibt.
        self.__curValues = curValues
        self.__progValues = progValues
        # Variable für den Automatik- bzw. manuellen Modus
        # Diese Variable wird entweder nicht als Referenz weitergegeben oder etwas anderes stimmt nicht. Auf jeden Fall verändert
        # sich der Wert außerhalb des Threads nicht.
        self.__auto = auto
        
        # Initialisierung des des Fensters
        self.root = tk.Tk()
        self.root.title("SetzlingsUI")

        # Variablen müssen als tk-Variablen definiert werden, damit sie im Widget angezeigt werden können
        defVal = None
        self._curTemperature = tk.IntVar(value=defVal)
        self._curHumidity = tk.IntVar(value=defVal)
        self._curMoisture = tk.IntVar(value=defVal)
        self._curLightState = tk.StringVar(value="---")

        # Diese Art von Styling kann erst nach Initialisierung vorgenommen werden
        # Wir verwenden ein vorgefertigtes Tkinter-Theme von rdbende, zu finden unter https://github.com/rdbende/Forest-ttk-theme
        self.root.tk.call('source', dirName+'/theme/forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky="nsew")
        
        # Vertikale und horizontale Trennlinien
        ttk.Frame(mainframe, style="Card", width=1).grid(row=0, column=1, rowspan=100, sticky="ns")
        ttk.Frame(mainframe, style="Card", height=1).grid(row=1, column=0, columnspan=100, sticky="ew")

        # Überschriften-Bereich
        ttk.Label(mainframe, text="Monitor", font=bigLabel, padding=10).grid(column=0, row=0, sticky="ew")
        ttk.Label(mainframe, text="Programm", font=bigLabel, padding=10).grid(column=2, row=0, columnspan=2, sticky="ew")
        # Schalter für den Automatik bzw. Manuellen Modus
        switchFrame = ttk.Frame(mainframe, padding=10)
        switchFrame.grid(column=4, row=0, sticky="e")
        ttk.Label(switchFrame, text="Auto", padding="0 0 5 0").grid(column=1, row=0, sticky="e")
        ttk.Checkbutton(switchFrame, text='Manuell', style='Switch', variable=self.__auto).grid(column=2, row=0, sticky="e")

        # "Monitor"-Bereich, zum Anzeigen der aktuellen Messwerte
        monitorFrame = ttk.Frame(mainframe, padding=10)
        monitorFrame.grid(column=0, row=2)
        self.datafield(monitorFrame, "Lufttemperatur:", self._curTemperature, "°C", "./imgs/dark_temp.png", 0)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=1)
        self.datafield(monitorFrame, "Luftfeuchtigkeit:", self._curHumidity, "%", "./imgs/dark_luft.png", 2)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=3)
        self.datafield(monitorFrame, "Bodenfeuchtigkeit:", self._curMoisture, "%", "./imgs/dark_tropfen.png", 4)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=5)
        self.datafield(monitorFrame, "Beleuchtung:", self._curLightState, "", "./imgs/dark_sonne.png", 6)

        # "Programm"-Bereich, zum Anzeigen der Soll-Werte
        programFrame = ttk.Frame(mainframe, padding=10)
        programFrame.grid(column=2, row=2)
        ttk.Frame(programFrame, width=200, height=100).grid(column=0, row=0)
        

        self.update()
        self.root.mainloop()


    def update(self):
        self._curTemperature.set(self.__curValues[0])
        self._curHumidity.set(self.__curValues[1])
        self._curMoisture.set(self.__curValues[2])
        self._curLightState.set(self.__curValues[3])

        self.__auto = not self.__auto

        # Die update-Funktion scheduled sich selbst, um nach bestimmter Zeit erneut ausgeführt zu werden
        self.root.after(self.__updateInterval, self.update)
