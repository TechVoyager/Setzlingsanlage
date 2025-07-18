import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import math
import serial
import serial.tools.list_ports
import platform
import time
from helperClasses import SerialDataObject
from Suche import Suche
import json


class GUI:
    # Schriftstile, die in verschiedenen Funktionen gebraucht werden
    global smallText, bigLabel
    smallText = ("System", "9")
    bigLabel = ("System", "16", "bold")


    def __init__(self, curMeasurements, curProfile, availableProfiles, selectedPlant, statusFlags, updateInterval):
        self.__curMeasurements = curMeasurements
        self.__curProfile = curProfile
        self._availableProfiles = availableProfiles
        self.__selectedPlant = selectedPlant
        # StatusFlags ist ein Dict, dass den Zustand des aktuellen Programms enthält: 
        # "auto" für den Automatikmodus, "unsentData" als Signal, dass Daten zum Raspi übertragen werden sollen,
        # "connected" für den Zustand der seriellen Schnittstelle, "running" für den Zustand des GUIs
        self.__statusFlags = statusFlags
        self.__updateInterval = updateInterval
        

        # Liste mit nur den Pflanzennamen für übersichtlicheren Code
        self._plantNameList = list(self._availableProfiles[0].keys())
        
        self.__previousConnectionStatus = False
        self.__enableSearch = True


        # Initialisierung des des Fensters
        self.root = tk.Tk()
        self.root.title("SetzlingsUI")
        # Wir verwenden ein vorgefertigtes Tkinter-Theme von rdbende, zu finden unter https://github.com/rdbende/Forest-ttk-theme
        self.root.tk.call('source', os.path.dirname(__file__)+'/theme/forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        ttk.Style().configure("Red.TLabel", foreground="red")
        ttk.Style().configure("Green.TLabel", foreground="green")


        # Such-Funktion muss initialisiert werden
        self.__searchFunction = Suche()

        # TK-Variable, die an den Automatik/ Manuell-Schalter oben rechts weitergegeben wird
        self.__TKauto = tk.BooleanVar(self.root, value=self.__statusFlags["auto"])

        # TK-Variable, in der die Eingabe vom Eingabe- bzw. Suchfeld gespeichert wird (Bei der Pflanzenauswahl)
        self.__TKplantEntryVar = tk.StringVar(self.root, value=self.__selectedPlant[0])
        # Wir hinterlegen eine Callback-Funktion für die Variable, um die angezeigte Liste an Pflanzenprofilen an die Eingabe anzupassen
        self.__TKplantEntryVar.trace_add("write", self.updatePlantList)

        # Die Soll-Werte werden zu TK-Variablen umformatiert
        self.__TKseedProgVals = {}
        self.__TKplantProgVals = {}
        # Außerdem bereiten wir ein dict mit TK-Variablen für die manuelle Eingabe der Soll-Werte vor
        self.__TKmanualVals = {}
        for key in self.__curProfile[0]:
            # Wir sortieren die Tk-Variablen in zwei dicts. Das ist für die Erstellung der GUI-Bereiche relevant
            if key.startswith("S_"):
                self.__TKseedProgVals[key] = tk.IntVar(self.root, value=self.__curProfile[0][key])
                # Als Default-Wert für die manuelle Eingabe nehmen wir 0, vllt. sind realistische Werte besser?
                self.__TKmanualVals[key.replace("S_", "")] = tk.IntVar(self.root, value=0)
            if key.startswith("P_"):
                self.__TKplantProgVals[key] = tk.IntVar(self.root, value=self.__curProfile[0][key])


        # Die Ist-Werte werden ebenfalls zu TK-Variablen umformatiert um sie anzeigen zu können
        self.__TKcurMeasurements = {}
        for key in self.__curMeasurements[0]:
            self.__TKcurMeasurements[key] = tk.StringVar(self.root, value = self.__curMeasurements[0][key])


        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky="nsew")
        
        # Vertikale und horizontale Trennlinien
        ttk.Frame(mainframe, style="Card", width=1).grid(row=0, column=1, rowspan=100, sticky="ns")
        ttk.Frame(mainframe, style="Card", height=1).grid(row=1, column=0, columnspan=100, sticky="ew")

        # Überschriften-Bereich
        # Linke Seite
        monitorFrame = ttk.Frame(mainframe)
        monitorFrame.grid(column=0, row=0, sticky="nsew")
        monitorFrame.columnconfigure(0, weight=1)
        ttk.Label(monitorFrame, text="Monitor", font=bigLabel, padding=10).grid(column=0, row=0, sticky="nsew")
        self.__connectionStatusField = ttk.Label(monitorFrame, text="...", padding=10)
        self.__connectionStatusField.grid(column=1, row=0, sticky="e")
        # Rechte Seite
        helperFrame = ttk.Frame(mainframe)
        helperFrame.grid(column=2, row=0, sticky="nsew")
        helperFrame.columnconfigure(1, weight=1)
        ttk.Label(helperFrame, text="Programm", font=bigLabel, padding=10).grid(column=0, row=0, sticky="w")
        # Schalter für den Automatik bzw. Manuellen Modus
        switchFrame = ttk.Frame(helperFrame, padding=10)
        switchFrame.grid(column=1, row=0, sticky="e")
        ttk.Label(switchFrame, text="Manuell", padding="0 0 5 0").grid(column=1, row=0, sticky="e")
        ttk.Checkbutton(switchFrame, text='Auto', style='Switch', variable=self.__TKauto, command=self.toggleMode).grid(column=2, row=0, sticky="e")

        # "Monitor"-Bereich, zum Anzeigen der aktuellen Messwerte
        monitorFrame = ttk.Frame(mainframe, padding=10)
        monitorFrame.grid(column=0, row=2)
        # Jeder Messwert besteht aus einer Beschreibung, dem Wert, einer Einheit und zuletzt einem Symbolbild
        self.dataField(monitorFrame, "Lufttemperatur:", self.__TKcurMeasurements["air_temperature"], "°C", "./imgs/dark_temp.png", 0)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=1)
        self.dataField(monitorFrame, "Luftfeuchtigkeit:", self.__TKcurMeasurements["air_humidity"], "%", "./imgs/dark_luft.png", 2)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=3)
        self.dataField(monitorFrame, "Bodentemperatur:", self.__TKcurMeasurements["soil_temperature"], "°C", "./imgs/dark_temp.png", 4)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=5)
        self.dataField(monitorFrame, "Bodenfeuchtigkeit:", self.__TKcurMeasurements["soil_moisture"], "%", "./imgs/dark_tropfen.png", 6)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=7)
        self.dataField(monitorFrame, "Beleuchtung:", self.__TKcurMeasurements["light_state"], "", "./imgs/dark_sonne.png", 8)

        # "Programm"-Bereich, zum Anzeigen der Soll-Werte
        programFrame = ttk.Frame(mainframe, padding=10)
        programFrame.grid(column=2, row=2, sticky="nw")
        # Der Übersicht halber wurde der Auswahl-Bereich für die Pflanzen(-profile) in eine eigene Funktion verpackt
        self.__plantSelectSectionArea = self.scrollableSelection(programFrame, self.__TKplantEntryVar)
        self.__plantSelectSectionArea.grid(column=0, row=0, sticky="nw")
        # Helperframe dient lediglich zum Einfügen von Padding
        helperFrame = ttk.Frame(programFrame, padding=5)
        helperFrame.grid(column=1, row=0, sticky="nsew")
        # Notebooks lassen Informationen auf mehreren Tabs anzeigen. In diesem Fall gibt es einen Tab für die Samen-Soll-Werte
        # und einen für die Pflanzen-Soll-Werte
        self.__progValDisplayNotebook = ttk.Notebook(helperFrame)
        self.__progValDisplayNotebook.grid(column=0, row=0)
        seedTilingFrame, seedEntryFields = self.tiledDataField(parentFrame=self.__progValDisplayNotebook, descriptors=list(self.__TKseedProgVals.keys()), variables=list(self.__TKseedProgVals.values()), addInfo=[], columns=2)
        self.__progValDisplayNotebook.add(seedTilingFrame, text="Samenstadium")
        saplingTilingFrame, saplingEntryFields = self.tiledDataField(parentFrame=self.__progValDisplayNotebook, descriptors=list(self.__TKplantProgVals.keys()), variables=list(self.__TKplantProgVals.values()), addInfo=[], columns=2)
        self.__progValDisplayNotebook.add(saplingTilingFrame, text="Setzlingstadium")

        # Wir erstellen außerdem einen separaten Eingabe-Bereich für den manuellen Modus. Hier wird der Nutzer selbst Soll-Werte
        # eingeben können, die direkt auf den Raspi übertragen werden.
        # Wir layouten diese "manualSection" noch nicht, damit sie "versteckt" bleibt!
        self.__manualSection = ttk.Frame(helperFrame)
        stylingFrame = ttk.Frame(self.__manualSection, style="Card", padding="5")
        stylingFrame.grid(column=0, row=0)
        manualValsTilingFrame, manualEntryFields = self.tiledDataField(parentFrame=stylingFrame, descriptors=list(self.__TKmanualVals.keys()), variables=list(self.__TKmanualVals.values()), addInfo=[], columns=2, startEnabled=True)
        manualValsTilingFrame.grid(column=0, row=0)
        # Abstandhalter
        ttk.Frame(self.__manualSection, height=10).grid(column=0, row=1)
        ttk.Button(self.__manualSection, text="Soll-Werte anwenden", style="Accent.TButton", command=self.profileToPico).grid(column=0, row=2, sticky="nsew")
        
        self.update()
        self.root.mainloop()
        # Die running-Flagge muss auf False gesetzt werden, um auch den Thread mit der seriellen Schnittstelle anzuhalten!
        self.__statusFlags["running"] = False
        print("closing")


    def update(self):
        # Update-Funktion, die sich um alles kümmert, was nicht direkt von TK erledigt wird

        # Messwerte werden aktualisert
        for key in self.__curMeasurements[0]:
            self.__TKcurMeasurements[key].set(self.__curMeasurements[0][key])

        # Hat sich der Verbindungsstatus geändert?
        if self.__statusFlags["connected"] != self.__previousConnectionStatus:
            if self.__statusFlags["connected"]:
                self.__connectionStatusField.config(text="Verbunden", style="Green.TLabel")
                # Wenn wir uns zum ersten Mal verbinden, werden die Pflanzenprofile vom Raspi geladen. Damit diese angezeigt
                # werden, müssen die Default-Werte überschrieben werden
                self._plantNameList = list(self._availableProfiles[0].keys())
                # Der Name des auf dem Raspi laufenden Profils wurde ebenfalls in die "selectedPlant"-Variable geladen.
                # Um diesen anzuzeigen, wird das Eingabe- bzw. Suchfeld aktualisiert.
                self.NewPlantSelected()
            else:
                self.__connectionStatusField.config(text="Getrennt", style="Red.TLabel")

            self.__previousConnectionStatus = self.__statusFlags["connected"]

        # Die update-Funktion scheduled sich selbst, um nach bestimmter Zeit erneut ausgeführt zu werden
        self.root.after(self.__updateInterval, self.update)
    

    @staticmethod
    def dataField(parentFrame: ttk.Frame, descriptor: str, variable, unit: str, img: str, row: int):
        # Template für ein Widget, welches einen Datenpunkt zusammen mit einer Beschreibung, Einheit und einem Bild darstellt

        # Der Pfad zum Bild wird relativ zum Pfad dieses Skripts bestimmt
        filepath = os.path.join(os.path.dirname(__file__), img)
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
    def dataInput(parentFrame: ttk.Frame, descriptor: str, variable, enabled: bool = False, *args):
        # Template für ein Widget, welches einen veränderlichen Datenpunkt darstellt

        dataFrame = ttk.Frame(parentFrame, padding=10)
        
        ttk.Label(dataFrame, text=descriptor, font=smallText, padding="0 0 0 10").grid(column=0, row=0, columnspan=2, sticky="nsew")
        entryField = ttk.Entry(dataFrame, textvariable=variable, width=15)
        entryField.grid(column=0, row=1, sticky="w")
        if enabled:
            entryField.config(state="normal")
        else:
            entryField.config(state="disabled")
        ttk.Label(dataFrame, text=args, padding="5 0 0 0").grid(column=1, row=1)

        # Gibt den dataFrame (in dem alles enthalten ist) zurück, damit gelayouted werden kann
        # und das entryField, damit die Eingabe später gesperrt und entsperrt werden kann
        return dataFrame, entryField
    

    def tiledDataField(self, parentFrame: ttk.Frame, descriptors: list, variables: list, addInfo: list, columns: int, startEnabled = False):
        # Template für ein dynamisches Tiling von dataInput-Widgets

        # Nötige Anzahl an Zeilen wird anhand der gewünschten Spalten-Anzahl ermittelt
        rows = math.ceil(len(descriptors) / columns)
        tilingFrame = ttk.Frame(parentFrame)
        # die "entry"-widgets, welche in dataInput genutzt werden, werden in einer Liste gespeichert und returned,
        # um das (Ent-)Sperren der Eingabe zu erleichtern, wenn zwischen dem Automatik bzw. Manuellen Modus gewechselt wird
        dataFields = {}
        for row in range(rows):
            for column in range(columns):
                index = columns * row + column
                if index <= len(descriptors) - 1:
                    dataFrame, entryField = self.dataInput(tilingFrame, descriptors[index].replace("P_", "").replace("S_", ""), variables[index], enabled=startEnabled)
                    dataFrame.grid(column=column, row=row, sticky="nsew")
                    dataFields[descriptors[index]] = entryField
        
        return tilingFrame, dataFields


    def toggleMode(self):
        # Wird vom "Automatik/ Manuell"-Schalter oben rechts aufgerufen, setzt das GUI in den ausgewählten Modus

        self.__statusFlags["auto"] = self.__TKauto.get()

        if self.__statusFlags["auto"]:
            self.__manualSection.grid_forget()
            self.__progValDisplayNotebook.grid(column=0, row=0)
            self.__plantSelectSectionArea.grid(column=0, row=0, sticky="nw")
        else:
            self.__plantSelectSectionArea.grid_forget()
            self.__progValDisplayNotebook.grid_forget()
            self.__manualSection.grid(column=0, row=0)
    

    def scrollableSelection(self, parentFrame, entryFieldVar):
        # Ein zusammengesetztes Widget für die Pflanzen-Auswahl, enthält ein Such-Feld, eine Liste der verfügbaren Profile
        # und ein Bestätigungs-Button.

        container = ttk.Frame(parentFrame, padding="0 5 5 0", width=100)
        # Suchfeld
        ttk.Entry(container, textvariable=entryFieldVar).grid(column=0, row=0, sticky="ew")
        # Abstandhalter
        ttk.Frame(container, height=5).grid(column=0, row=1)

        # show="" sorgt dafür, dass der Tabellenkopf ausgeblendet wird, "height" gibt die Anzahl an angezeigten Elementen an
        self.__plantSelectionBox = ttk.Treeview(container, columns=["Name"], show="", height=5)
        self.__plantSelectionBox.grid(column=0, row=2, sticky="ew")
        self.__plantSelectionBox.column("0", minwidth=0, width=100)
        for plantName in self._plantNameList:
            self.__plantSelectionBox.insert('', index="end", values=plantName)
        
        self.__plantSelectionBox.bind("<<TreeviewSelect>>", self.NewPlantSelected)

        # Abstandhalter
        ttk.Frame(container, height=5).grid(column=0, row=3)
        ttk.Button(container, text="Profil anwenden", style="Accent.TButton", command=self.profileToPico).grid(column=0, row=4, sticky="nsew")
        
        # Container wird für weiteres Styling zurückgegeben
        return container
        

    def updatePlantList(self, *args):
        # Diese Funktion füllt die Liste unterhalb des Eingabe- bzw. Suchfelds mit den zur Eingabe passenden Pflanzenprofilen

        if self.__enableSearch:
            entry = self.__TKplantEntryVar.get()
            newPlantList = self.__searchFunction.Suche_Pflanzenart(suchstring=entry, suchliste=self._plantNameList)
            # Die alten Optionen werden gelöscht
            for plantName in self.__plantSelectionBox.get_children():
                self.__plantSelectionBox.delete(plantName)
            # Und die neuen hinzugefügt
            for plantName in newPlantList:
                self.__plantSelectionBox.insert('', index="end", values=plantName)
    

    def updateCurProfile(self):
        # Schreibt die Soll-Werte des aktuell ausgewählten Profils in die Felder auf der rechten Seite
        
        # Dafür aktualisieren wir die entsprechende Variable
        # Wichtig: Das hier gespeicherte Profil wird vom Thread der seriellen Schnittstelle gelesen und bei Bedarf zum Raspi geschickt!
        self.__curProfile[0] = self._availableProfiles[0][self.__selectedPlant[0]]
        for field in self.__TKseedProgVals:
            self.__TKseedProgVals[field].set(self.__curProfile[0][field])
        for field in self.__TKplantProgVals:
            self.__TKplantProgVals[field].set(self.__curProfile[0][field])
    

    def NewPlantSelected(self, *args):
        # Aktualisiert die nötigen Werte, wenn sich das ausgewählte Profil ändert
        # Wird auch aufgerufen, wenn der Nutzende eine Pflanze aus der Liste unter dem Eingabe-Feld auswählt

        # Wird diese Funktion als Callback durch das Klicken auf eine Pflanze in der Liste aufgerufen, werden in
        # "args" Details zu diesem Event übergeben. Daran erkennen wir, dass wir die Variabel "selectedPlant" 
        # auf den ausgewählten Wert setzen müssen.
        if args and len(self.__plantSelectionBox.selection()) > 0:
            selected_row = self.__plantSelectionBox.selection()[0]
            self.__selectedPlant[0] = self.__plantSelectionBox.item(selected_row, "values")[0]
        # Wir löschen die Eingabe im Such-Feld, damit die "UpdatePlantList"-Funktion getriggert wird und die gesamte Liste
        # an Pflanzenprofilen anzeigt wird
        self.__TKplantEntryVar.set("")
        # Dann deaktivieren wir die "UpdatePlantList"-Funktion kurz, um den ausgewählten Pflanzennamen in das Such-Feld zu schreiben, ohne,
        # dass dadurch die Liste an angezeigten Pflanzenprofilen verändert wird. (Im Normalfall würde diese Funktion jetzt nur noch Pflanzenprofile
        # anzeigen, die Ähnlich zu der Eingabe sind)
        self.__enableSearch = False
        self.__TKplantEntryVar.set(self.__selectedPlant[0])
        self.__enableSearch = True
        # Zum Schluss aktualisieren wir die angezeigten Soll-Werte auf der rechten Seite
        self.updateCurProfile()

    
    def profileToPico(self):
        # Dient als Callback für den "Profil anwenden"-Knopf, schickt das aktuell ausgewählte Pflanzenprofil zum Pico

        # Wenn wir im manuellen Modus sind, überschreiben wir zuerst "curProfile" mit den manuellen Werten
        if not self.__statusFlags["auto"]:
            # Pflanzenart wird auf manuell gesetzt um Zustand eindeutig zu machen
            newProfile = {"Pflanzenart": "manuell"}
            
            for key in self.__TKmanualVals:
                newProfile[key] = self.__TKmanualVals[key].get()

            if self.__curProfile[0] != newProfile:
                # Wir schicken nur Daten, wenn sie tatsächlich auch Änderungen enthalten
                self.__curProfile[0] = newProfile

        if not self.__statusFlags["connected"]:
            messagebox.showerror("Verbindung getrennt", "Es besteht keine Verbindung zur Setzlingsanlage. Überprüfen sie das Kabel und die Stromversorgung")
            return
        
        if self.__statusFlags["auto"] and self.__TKplantEntryVar.get() not in self._plantNameList:
            messagebox.showerror("Kein Pflanzenprofil ausgewählt", "Bitte schreiben Sie den vollständigen Namen eines gespeicherten Pflanzenprofils in das Eingabefeld oder wählen Sie ein Profil aus der Liste aus.")
            return

        if not self.__statusFlags["unsentData"]:
            self.__statusFlags["unsentData"] = True
        else:
            messagebox.showerror("Zu viele Daten", "Es wurden noch nicht alle Daten auf die Setzlingsanlage übertragen. Bitte versuchen Sie es gleich erneut.")


class SerialInterface:
    def __init__(self, curMeasurements, curProfile, availableProfiles, selectedPlant, statusFlags, port=None, baudrate=115200):
        self.__statusFlags = statusFlags

        # Serielle Verbindung konfigurieren
        self.connection = serial.Serial(timeout=.1)
        self.connection.baudrate = baudrate

        # Zeit in Sekunden, für die auf eine Antwort vom Raspi gewartet werden soll
        self.dataRecievingTimeOut = 1

        # Optionales Bestimmen des Betriebsystems, um bessere Fehlermeldungen auszugeben
        self.osType = platform.system()

        # Verbindungsaufbau
        result = self.findPortAndConnect(port)

        if result:  
            # Holt die auf dem Raspi gespeicherten Pflanzenprofile und das aktuell ausgewählte Profil
            curConfiguration = self.send("getConfig")
            availableProfiles[0] = curConfiguration["profiles"]
            selectedPlant[0] = curConfiguration["selectedPlant"]
            print(selectedPlant)
            self.__statusFlags["connected"] = True
            
            # Solange das GUI läuft, werden Daten gesendet und empfangen
            while self.__statusFlags["running"]:
                if self.__statusFlags["unsentData"]:
                    response = self.send("setProfile")
                    if response == "begin":
                        self.sendBigData(curProfile[0])
                    self.__statusFlags["unsentData"] = False
                
                curMeasurements[0] = self.send("getMeasurements")
                time.sleep(1)
            
            print("disconnecting")
            self.send("disconnect", waitForResponse=False)
            self.disconnect()
        else:
            print("Couldn't find device to connect")
    

    def send(self, data, waitForResponse=True):
        # Schickt Daten zum Raspberry Pico und wartet auf eine Antwort
        # Das Warten auf die Antwort blockiert zwar den aktuellen Thread, ist aber in den meisten Fällen sinnvoll/ nicht schlimm:
        # 1. Bei "Anfragen", also wenn Werte vom Raspi zum PC übertragen werden sollen, wird sowieso nur eine Anfrage gleichzeitig
        #    abgeschickt, da mehrere Anfragen zu Chaos und einem deutlichen komplizierteren Protokoll führen würden.
        # 2. Bei "Befehlen" bzw. dem Übertragen von Werten vom PC zum Raspi dient die Antwort vom Raspi als Bestätigung, dass die
        #    Verbindung noch am Leben ist.
        # Im Ausnahmefall kann mit "waitForResponse=False" auch auf das Warten verzichtet werden.
        self.connection.write(bytes(str(data), "utf-8"))

        if waitForResponse:
            self.waitTillTimeout(self.dataRecievingTimeOut)
            data = self.read()
            return data


    def read(self):
        # Liest Daten aus dem Input-Buffer und entfernt unnötige Formatierungszeichen
        recieved = self.connection.readline().decode()
        processed = recieved.replace("\r","").replace("\n","")
        if processed.startswith("json:"):
            processed = json.loads(processed.replace("json:", ""))
        print(processed)
        return processed
    
    
    def sendBigData(self, data):
        # Diese Funktion dient zum senden größerer Datenmengen (>~250 Bytes), da diese nicht auf einmal übertragen werden können.
        # Mehr Informationen dazu lassen sich in helperClasses.py finden.
        # Das Senden eines SerialDataObjects dauert deutlich länger als das einer kurzen Nachricht, da es in Etappen passiert.
        # Diese Funktion sollte daher nur wenn nötig verwendet werden.

        # Daten werden im SerialDataObject "zerstückelt"
        dataObject = SerialDataObject(data)
        for chunk in dataObject:
            chunkResponse = self.send(chunk)
            # Nach jedem gesendeten Stück (Chunk) wird darauf gewartet, dass das andere Gerät den Chunk verarbeitet hat und eine Antwort schickt.
            # Ist die Antwort "next", so wird das nächste Stück geschickt. Ist die Nachricht nicht eindeutig identifizierbar, so ist
            # in der Übertragung etwas schiefgelaufen und die Funktion endet unerfolgreich. Wird der Timeout erreich, wird ein Error
            # erzeugt. Der Timeout ist in der "send"-Funktion mitinbegriffen
            if chunkResponse != "next":
                return False
        
        # Sind alle Daten gesendet, so wird dies mit einem "done" signalisiert
        response = self.send("done")
    

    def findPortAndConnect(self, port):
        # Diese Funktion versucht sich mit allen zur Verfügung stehenden seriellen Ports zu verbinden und eine
        # Synchronisierung durchzuführen, um zu testen, ob das Gerät auch tatsächlich die Setzlingsanlage ist.
        # Zum Überschreiben der automatischen Portsuche kann der port im Vorhinein als Parameter gesetzt werden

        availablePorts = serial.tools.list_ports.comports()
        availablePorts.reverse()

        if not port == None:
            # Ist ein Port bereits gegeben wird dieser verwendet
            self.connection.port = port
            self.connection.open()
            self.connection.reset_input_buffer()
            self.testConnection()
            return True
        else:
            # Wir testen jeden verfügbaren Port. Wenn beim Verbindungsaufbau ein Fehler auftritt, gehen wir zum nächsten weiter
            for avPort in availablePorts:
                self.connection.port = avPort.device
                print(self.connection.port)
                try:
                    self.connection.open()
                    self.testConnection()
                    # Ist bis hierhin kein Fehler aufgetreten, ist die Verbindung erfolgreich aufgebaut
                    return True
                
                except Exception as e:
                    print(e)
                    self.disconnect()
                    
            # Sind wir hier angekommen, heißt das, dass keine zufriedenstellende Verbindung aufgebaut werden konnte
            return False


    def testConnection(self):
        # Dient zum Testen der Verbindung. Der PC schickt ein "sync" und erwartet darauf ein "sync" vom Raspi. Erhält er das,
        # wird die Verbindung als funktionierend bzw. "synchronisiert" angesehen.
        response = self.send("sync")
        if not response == "sync":
            raise ConnectionError


    def disconnect(self):
        self.connection.close()
        # Diese Flagge muss immer gesetzt werden, damit das GUI den Status der Verbindung anzeigen kann.
        self.__statusFlags["connected"] = False
    

    def waitTillTimeout(self, timeout):
        # Eine Funktion um auf Daten im Input-Buffer zu warten. Natürlich mit Timeout, um den Programmcode nicht zu blockieren.
        # Gibt in Form eines bool zurück, ob der Timeout erreicht wurde oder nicht
        startTime = time.monotonic()
        while self.connection.in_waiting == 0:
            currentTime = time.monotonic()
            if (currentTime - startTime) >= timeout:
                return False
        return True