import tkinter as tk
from tkinter import ttk
import os


class GUI:
    # Schriftstile, die in verschiedenen Funktionen gebraucht werden
    global smallText, boldText, normText, bigLabel
    smallText = ("System", "9")
    normText = ("System", "14")
    boldText = ("System", "14", "bold")
    bigLabel = ("System", "16", "bold")


    @staticmethod
    def datafield(parentFrame, descriptor: str, variable, unit: str, img: str, row: int):
        # Template für ein Widget, welches einen Datenpunkt zusammen mit einer Beschreibung, Einheit und einem Bild darstellt

        # Der Pfad zum Bild wird relativ zum Pfad dieses Skripts bestimmt
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, img)
        image = tk.PhotoImage(file=filepath)

        dataframe = ttk.Frame(parentFrame, padding="0 15 0 15")
        # Das Bild muss als Referenz gespeichert werden, da es sonst direkt garbage-collected wird
        dataframe.image = image
        dataframe.grid(row=row, sticky="w")

        ttk.Label(dataframe, image=image, padding="0 0 10 0").grid(column=0, row=0, rowspan=3, sticky="s")
        ttk.Label(dataframe, text=descriptor, font=smallText, padding="0 0 10 0").grid(column=1, row=0, columnspan=6, sticky="w")
        ttk.Label(dataframe, textvariable=variable, font=bigLabel).grid(column=1, row=1, sticky="w")
        ttk.Label(dataframe, text=unit, font=bigLabel).grid(column=2, row=1, sticky="w")


    def __init__(self, updateInterval, curValues, progValues):
        self.__updateInterval = updateInterval
        # Messwerte und Soll-Werte werden bei der Instanzierung als Listen übergeben, da diese per Referenz übergeben werden.
        # So liest die "update"-Funktion automatisch die neusten Werte, welche sie dann in das GUI schreibt.
        self.__curValues = curValues
        self.__progValues = progValues
        
        # Initialisierung des des Fensters
        self.root = tk.Tk()
        self.root.title("SetzlingsUI")

        # TO-DO: Ist für die Variablen ein Setter notwendig, oder reicht es die Attribute direkt zu setzen?
        defVal = None
        self._curTemperature = tk.IntVar(value=defVal)
        self._curHumidity = tk.IntVar(value=defVal)
        self._curMoisture = tk.IntVar(value=defVal)
        self._curLightState = tk.StringVar(value="---")

        # Diese Art von Styling kann erst nach Initialisierung vorgenommen werden
        style = ttk.Style()
        style.theme_use('default')
        style.configure("ThinBorder.TFrame", background="black")

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky="nsew")
        
        # Überschriften-Bereich
        ttk.Label(mainframe, text="Monitor", font=bigLabel, padding=10).grid(column=0, row=0, sticky="ew")
        ttk.Frame(mainframe, style="ThinBorder.TFrame", width=1).grid(row=0, column=1, rowspan=100, sticky="ns")
        ttk.Label(mainframe, text="Programm", font=bigLabel, padding=10).grid(column=2, row=0, columnspan=2, sticky="ew")
        ttk.Frame(mainframe, style="ThinBorder.TFrame", height=1).grid(row=1, column=0, columnspan=4, sticky="ew")

        # "Monitor"-Bereich, zum Anzeigen der aktuellen Messwerte
        monitorFrame = ttk.Frame(mainframe, padding=10)
        monitorFrame.grid(column=0, row=2)
        self.datafield(monitorFrame, "Lufttemperatur:", self._curTemperature, "°C", "./imgs/temp.png", 0)
        self.datafield(monitorFrame, "Luftfeuchtigkeit:", self._curHumidity, "%", "./imgs/luft.png", 1)
        self.datafield(monitorFrame, "Bodenfeuchtigkeit:", self._curMoisture, "%", "./imgs/tropfen.png", 2)
        self.datafield(monitorFrame, "Beleuchtung:", self._curLightState, "", "./imgs/sonne.png", 3)

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

        # Die update-Funktion scheduled sich selbst, um nach bestimmter Zeit erneut ausgeführt zu werden
        self.root.after(self.__updateInterval, self.update)
