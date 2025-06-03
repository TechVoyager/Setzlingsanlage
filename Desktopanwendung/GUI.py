import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import math


class GUI:
    # Schriftstile, die in verschiedenen Funktionen gebraucht werden
    global smallText, boldText, normText, bigLabel, dirName
    smallText = ("System", "9")
    normText = ("System", "14")
    boldText = ("System", "14", "bold")
    bigLabel = ("System", "16", "bold")

    dirName = os.path.dirname(__file__)


    @staticmethod
    def dataField(parentFrame: ttk.Frame, descriptor: str, variable, unit: str, img: str, row: int):
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

    
    @staticmethod
    def dataInput(parentFrame: ttk.Frame, descriptor: str, variable, addInfo: str, enabled: bool = False):
        # Template für ein Widget, welches einen veränderlichen Datenpunkt darstellt

        dataFrame = ttk.Frame(parentFrame, padding=15, style="Card")
        
        ttk.Label(dataFrame, text=descriptor, font=smallText, padding="0 0 0 10").grid(column=0, row=0, columnspan=2, sticky="w")
        entryField = ttk.Entry(dataFrame, textvariable=variable, width=10)
        entryField.grid(column=0, row=1)
        if enabled:
            entryField.config(state="normal")
        else:
            entryField.config(state="disabled")
        ttk.Label(dataFrame, text=addInfo, padding="5 0 0 0").grid(column=1, row=1)

        # Gibt den dataFrame (in dem alles enthalten ist) zurück, damit gelayouted werden kann
        # und das entryField, damit die Eingabe später gesperrt und entsperrt werden kann
        return dataFrame, entryField
    

    def tiledDataField(self, parentFrame: ttk.Frame, descriptors: list, variables: list, addInfo: list, columns: int):
        # Template für ein dynamisches Tiling von dataInput-Widgets

        # Nötige Anzahl an Zeilen wird anhand der gewünschten Spalten-Anzahl ermittelt
        rows = math.ceil(len(descriptors) / columns)
        tilingFrame = ttk.Frame(parentFrame)
        # die "entry"-widgets, welche in dataInput genutzt werden, werden in einer Liste gespeichert und returned,
        # um das (Ent-)Sperren der Eingabe zu erleichtern, wenn zwischen dem Automatik bzw. Manuellen Modus gewechselt wird
        dataFields = []
        for row in range(rows):
            for column in range(columns):
                index = columns * row + column
                if index <= len(descriptors) - 1:
                    # das helperFrame ist dafür da, um ein Padding zwischen den dataInput-Widgets zu erzeugen
                    helperFrame = ttk.Frame(tilingFrame, padding=5)
                    dataFrame, entryField = self.dataInput(helperFrame, descriptors[index], variables[index], addInfo[index])
                    # das dataFrame MUSS mit .grid eingelayouted werden, da es sonst nicht angezeigt wird
                    dataFrame.grid(column=0, row=0)
                    helperFrame.grid(column=column, row=row)
                    dataFields.append(entryField)
        
        return tilingFrame, dataFields


    def toggleEntryFields(self):
        for field in self.__entryFields:
            if self.__auto.get():
                field.config(state="disabled")
            else:
                field.config(state="normal")
    

    def scrollableSelection(self, parentFrame, entryFieldVar):
        container = ttk.Frame(parentFrame, padding="0 5 5 0", width=100)
        ttk.Entry(container, textvariable=entryFieldVar).grid(column=0, row=0, sticky="ew")
        ttk.Frame(container, height=5).grid(column=0, row=1)

        self.__plantSelectionBox = ttk.Treeview(container, columns=["Name"], show="", height=5)
        self.__plantSelectionBox.grid(column=0, row=2, sticky="ew")
        self.__plantSelectionBox.column("0", minwidth=0, width=100)
        for plantName in self._plantList:
            self.__plantSelectionBox.insert('', index="end", values=plantName)
        
        self.__plantSelectionBox.bind("<<TreeviewSelect>>", self.plantSelected)

        ttk.Frame(container, height=5).grid(column=0, row=3)
        ttk.Button(container, text="Profil anwenden", style="Accent.TButton", command=self.profileToPico).grid(column=0, row=4, sticky="nsew")
        
        return container
    

    def plantSelected(self, event):
        selected_row = self.__plantSelectionBox.selection()[0]
        self._selectedPlant = self.__plantSelectionBox.item(selected_row, "values")[0]
        self.__plantEntryVar.set(self._selectedPlant)

    
    def profileToPico(self):
        # Schickt das aktuell ausgewählte Pflanzenprofil und (bei Erstellung eines neuen Profils) die Soll-Werte zum Pico
        plantToSend = self.__plantEntryVar.get()
        if plantToSend in self._plantList:
            print("PLACEHOLDER: sent data:", plantToSend)
        else:
            error = messagebox.showerror("Kein Pflanzenprofil ausgewählt", "Bitte schreibe den Namen eines gespeicherten Pflanzenprofils in das Eingabefeld oder wähle ein Profil aus der Liste aus.")


    def __init__(self, updateInterval, curValues, progValues, auto, plantList, selectedPlant):
        self.__updateInterval = updateInterval
        # Messwerte und Soll-Werte werden bei der Instanzierung als Listen übergeben, da diese per Referenz übergeben werden.
        # So liest die "update"-Funktion automatisch die neusten Werte, welche sie dann in das GUI schreibt.
        self.__curValues = curValues
        self.__progValues = progValues
        self._plantList = plantList
        self._selectedPlant = selectedPlant
        
        # Initialisierung des des Fensters
        self.root = tk.Tk()
        self.root.title("SetzlingsUI")

        # Variablen müssen als tk-Variablen definiert werden, damit sie im Widget angezeigt werden können
        defVal = None
        self._curTemperature = tk.IntVar(self.root, value=defVal)
        self._curHumidity = tk.IntVar(self.root, value=defVal)
        self._curMoisture = tk.IntVar(self.root, value=defVal)
        self._curLightState = tk.StringVar(self.root, value="---")
        # Variable für den Automatik- bzw. manuellen Modus
        # Diese Variable wird entweder nicht als Referenz weitergegeben oder etwas anderes stimmt nicht. Auf jeden Fall verändert
        # sich der Wert außerhalb des Threads nicht.
        self.__auto = tk.BooleanVar(self.root, value=True)

        self.__plantEntryVar = tk.StringVar(self.root, value=selectedPlant)

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
        helperFrame = ttk.Frame(mainframe)
        helperFrame.grid(column=2, row=0, sticky="nsew")
        helperFrame.columnconfigure(1, weight=1)
        ttk.Label(helperFrame, text="Programm", font=bigLabel, padding=10).grid(column=0, row=0, sticky="w")
        # Schalter für den Automatik bzw. Manuellen Modus
        switchFrame = ttk.Frame(helperFrame, padding=10)
        switchFrame.grid(column=1, row=0, sticky="e")
        ttk.Label(switchFrame, text="Manuell", padding="0 0 5 0").grid(column=1, row=0, sticky="e")
        ttk.Checkbutton(switchFrame, text='Auto', style='Switch', variable=self.__auto, command=self.toggleEntryFields).grid(column=2, row=0, sticky="e")

        # "Monitor"-Bereich, zum Anzeigen der aktuellen Messwerte
        monitorFrame = ttk.Frame(mainframe, padding=10)
        monitorFrame.grid(column=0, row=2)
        self.dataField(monitorFrame, "Lufttemperatur:", self._curTemperature, "°C", "./imgs/dark_temp.png", 0)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=1)
        self.dataField(monitorFrame, "Luftfeuchtigkeit:", self._curHumidity, "%", "./imgs/dark_luft.png", 2)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=3)
        self.dataField(monitorFrame, "Bodenfeuchtigkeit:", self._curMoisture, "%", "./imgs/dark_tropfen.png", 4)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=5)
        self.dataField(monitorFrame, "Beleuchtung:", self._curLightState, "", "./imgs/dark_sonne.png", 6)

        # "Programm"-Bereich, zum Anzeigen der Soll-Werte
        programFrame = ttk.Frame(mainframe, padding=10)
        programFrame.grid(column=2, row=2, sticky="nw")
        plantSelectSection = self.scrollableSelection(programFrame, self.__plantEntryVar)
        plantSelectSection.grid(column=0, row=0, sticky="nw")
        # TO-DO: Platzhalter gegen echte Werte austauschen
        tilingFrame, entryFields = self.tiledDataField(parentFrame=programFrame, descriptors=range(6), variables=range(6), addInfo=range(6), columns=2)
        tilingFrame.grid(column=1, row=0)

        self.__entryFields = entryFields
        

        self.update()
        self.root.mainloop()


    def update(self):
        self._curTemperature.set(self.__curValues[0])
        self._curHumidity.set(self.__curValues[1])
        self._curMoisture.set(self.__curValues[2])
        self._curLightState.set(self.__curValues[3])

        # Die update-Funktion scheduled sich selbst, um nach bestimmter Zeit erneut ausgeführt zu werden
        self.root.after(self.__updateInterval, self.update)
