import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import math
import serial
import serial.serialutil
import serial.tools.list_ports
import platform
import time


class GUI:
    # Schriftstile, die in verschiedenen Funktionen gebraucht werden
    global smallText, bigLabel, dirName
    smallText = ("System", "9")
    bigLabel = ("System", "16", "bold")

    dirName = os.path.dirname(__file__)


    def __init__(self, curValues, progValues, availableProfiles, selectedPlant, statusFlags, updateInterval):
        # Die meisten Parameter werden hier sowohl als "regulärer" Python-Datentyp, als auch als TK-Datentyp gespeichert.
        # Der Grund dafür ist die Kommunikation mit dem Pico: Das GUI wird am Ende in einem Thread laufen, die
        # serielle Schnittstelle in einem anderen. Um Daten zwischen den Threads auszutauschen, werden diese als globale
        # Variablen im Heap gespeichert. Alle Daten, die zwischen den Threads ausgetauscht werden, werden als Referenz
        # an diese Klasse übergeben, damit Änderungen direkt im Heap passieren.
        # Da nur Listen(-ähnliche) Datentypen als Referenz übergeben werden, werden alle andere Datentypen in einer
        # list oder einem dict verpackt.

        self.__updateInterval = updateInterval
        # Dictionary für die Ist-Werte
        self.__curValues = curValues
        # Dictionary für die programmierten bzw. Soll-Werte
        self.__progValues = progValues
        self._plantList = availableProfiles
        self._selectedPlant = selectedPlant

        # dict welches die Zustände des aktuellen Programms enthält: 
        # "auto" für den Automatikmodus, "unsentData" als Signal, dass Daten zum Raspi übertragen werden sollen
        # "connected" für den Zustand der seriellen Schnittstelle, "running" für den Zustand des GUIs
        self.__statusFlags = statusFlags

        
        # Initialisierung des des Fensters
        self.root = tk.Tk()
        self.root.title("SetzlingsUI")

        # Variablen müssen außerdem auch als tk-Variablen definiert werden, damit sie im Widget angezeigt werden können
        self.__TKcurTemperature = tk.IntVar(self.root, value=curValues["airTemp"])
        self.__TKcurHumidity = tk.IntVar(self.root, value=curValues["humidity"])
        self.__TKcurMoisture = tk.IntVar(self.root, value=curValues["moisture"])
        self.__TKcurLightState = tk.StringVar(self.root, value=curValues["lightState"])
        self.__TKauto = tk.BooleanVar(self.root, value=self.__statusFlags["auto"])

        # Enthält die Eingabe in das Such-Feld bei der Auswahl des Pflanzenprofils
        self.__TKplantEntryVar = tk.StringVar(self.root, value=selectedPlant[0])

        # Diese Art von Styling kann erst nach Initialisierung vorgenommen werden
        # Wir verwenden ein vorgefertigtes Tkinter-Theme von rdbende, zu finden unter https://github.com/rdbende/Forest-ttk-theme
        self.root.tk.call('source', dirName+'/theme/forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        ttk.Style().configure("Red.TLabel", foreground="red")
        ttk.Style().configure("Green.TLabel", foreground="green")

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky="nsew")
        
        # Vertikale und horizontale Trennlinien
        ttk.Frame(mainframe, style="Card", width=1).grid(row=0, column=1, rowspan=100, sticky="ns")
        ttk.Frame(mainframe, style="Card", height=1).grid(row=1, column=0, columnspan=100, sticky="ew")

        # Überschriften-Bereich
        monitorFrame = ttk.Frame(mainframe)
        monitorFrame.grid(column=0, row=0, sticky="nsew")
        monitorFrame.columnconfigure(0, weight=1)
        ttk.Label(monitorFrame, text="Monitor", font=bigLabel, padding=10).grid(column=0, row=0, sticky="nsew")
        self.__connectionStatusField = ttk.Label(monitorFrame, text="...", padding=10)
        self.__connectionStatusField.grid(column=1, row=0, sticky="e")
        helperFrame = ttk.Frame(mainframe)
        helperFrame.grid(column=2, row=0, sticky="nsew")
        helperFrame.columnconfigure(1, weight=1)
        ttk.Label(helperFrame, text="Programm", font=bigLabel, padding=10).grid(column=0, row=0, sticky="w")
        # Schalter für den Automatik bzw. Manuellen Modus
        switchFrame = ttk.Frame(helperFrame, padding=10)
        switchFrame.grid(column=1, row=0, sticky="e")
        ttk.Label(switchFrame, text="Manuell", padding="0 0 5 0").grid(column=1, row=0, sticky="e")
        ttk.Checkbutton(switchFrame, text='Auto', style='Switch', variable=self.__TKauto, command=self.toggleEntryFields).grid(column=2, row=0, sticky="e")

        # "Monitor"-Bereich, zum Anzeigen der aktuellen Messwerte
        monitorFrame = ttk.Frame(mainframe, padding=10)
        monitorFrame.grid(column=0, row=2)
        self.dataField(monitorFrame, "Lufttemperatur:", self.__TKcurTemperature, "°C", "./imgs/dark_temp.png", 0)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=1)
        self.dataField(monitorFrame, "Luftfeuchtigkeit:", self.__TKcurHumidity, "%", "./imgs/dark_luft.png", 2)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=3)
        self.dataField(monitorFrame, "Bodenfeuchtigkeit:", self.__TKcurMoisture, "%", "./imgs/dark_tropfen.png", 4)
        ttk.Frame(monitorFrame, height=10).grid(column=0, row=5)
        self.dataField(monitorFrame, "Beleuchtung:", self.__TKcurLightState, "", "./imgs/dark_sonne.png", 6)

        # "Programm"-Bereich, zum Anzeigen der Soll-Werte
        programFrame = ttk.Frame(mainframe, padding=10)
        programFrame.grid(column=2, row=2, sticky="nw")
        plantSelectSection = self.scrollableSelection(programFrame, self.__TKplantEntryVar)
        plantSelectSection.grid(column=0, row=0, sticky="nw")
        # TO-DO: Platzhalter gegen echte Werte austauschen
        tilingFrame, entryFields = self.tiledDataField(parentFrame=programFrame, descriptors=range(6), variables=range(6), addInfo=range(6), columns=2)
        tilingFrame.grid(column=1, row=0)

        # Die Eingabefelder für die Soll-Werte werden in einer Liste gespeichert, damit sie einfach gesperrt bzw. entsperrt werden können
        self.__entryFields = entryFields
        

        self.update()
        self.root.mainloop()
        self.__statusFlags["running"] = False
        print("closing")


    def update(self):
        self.__TKcurTemperature.set(self.__curValues["airTemp"])
        self.__TKcurHumidity.set(self.__curValues["humidity"])
        self.__TKcurMoisture.set(self.__curValues["moisture"])
        self.__TKcurLightState.set(self.__curValues["lightState"])

        if self.__statusFlags["connected"]:
            self.__connectionStatusField.config(text="Verbunden", style="Green.TLabel")
        else:
            self.__connectionStatusField.config(text="Getrennt", style="Red.TLabel")

        # Die update-Funktion scheduled sich selbst, um nach bestimmter Zeit erneut ausgeführt zu werden
        self.root.after(self.__updateInterval, self.update)
    

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
        self.__statusFlags["auto"] = self.__TKauto.get()

        for field in self.__entryFields:
            if self.__statusFlags["auto"]:
                field.config(state="disabled")
            else:
                field.config(state="normal")
    

    def scrollableSelection(self, parentFrame, entryFieldVar):
        # Ein zusammengesetztes Widget für die Pflanzen-Auswahl, enthält ein Such-Feld, eine Liste der verfügbaren Profile
        # und ein Bestätigungs-Button.
        
        # TO-DO: Suchalgorithmus implementieren

        container = ttk.Frame(parentFrame, padding="0 5 5 0", width=100)
        # Suchfeld
        ttk.Entry(container, textvariable=entryFieldVar).grid(column=0, row=0, sticky="ew")
        # Abstandhalter
        ttk.Frame(container, height=5).grid(column=0, row=1)

        # show="" sorgt dafür, dass der Tabellenkopf ausgeblendet wird, "height" gibt die Anzahl an angezeigten Elementen an
        self.__plantSelectionBox = ttk.Treeview(container, columns=["Name"], show="", height=5)
        self.__plantSelectionBox.grid(column=0, row=2, sticky="ew")
        self.__plantSelectionBox.column("0", minwidth=0, width=100)
        for plantName in self._plantList:
            self.__plantSelectionBox.insert('', index="end", values=plantName)
        
        self.__plantSelectionBox.bind("<<TreeviewSelect>>", self.plantSelected)

        # Abstandhalter
        ttk.Frame(container, height=5).grid(column=0, row=3)
        ttk.Button(container, text="Profil anwenden", style="Accent.TButton", command=self.profileToPico).grid(column=0, row=4, sticky="nsew")
        
        # Container wird für weiteres Styling zurückgegeben
        return container
    

    def plantSelected(self, event):
        selected_row = self.__plantSelectionBox.selection()[0]
        # Es müssen immer beide Variablen aktualisiert werden!
        self._selectedPlant[0] = self.__plantSelectionBox.item(selected_row, "values")[0]
        self.__TKplantEntryVar.set(self._selectedPlant[0])

    
    def profileToPico(self):
        # Schickt das aktuell ausgewählte Pflanzenprofil und die Soll-Werte zum Pico
        plantToSend = self.__TKplantEntryVar.get()
        if not self.__statusFlags["connected"]:
            messagebox.showerror("Verbindung getrennt", "Es besteht keine Verbindung zur Setzlingsanlage. Überprüfen sie das Kabel und die Verbindungseinstellungen.")
            return
        
        if plantToSend not in self._plantList:
            messagebox.showerror("Kein Pflanzenprofil ausgewählt", "Bitte schreiben Sie den vollständigen Namen eines gespeicherten Pflanzenprofils in das Eingabefeld oder wählen Sie ein Profil aus der Liste aus.")
            return

        if not self.__statusFlags["unsentData"]:
            self.__statusFlags["unsentData"] = True
        else:
            messagebox.showerror("Zu viele Daten", "Es wurden noch nicht alle Daten auf die Setzlingsanlage übertragen. Bitte versuchen Sie es gleich erneut.")


class SerialInterface:
    def __init__(self, curValues, progValues, availableProfiles, selectedPlant, statusFlags, port=str(serial.tools.list_ports.comports()[-1].device), baudrate=9600):
        self.__statusFlags = statusFlags
        
        
        # Serielle Verbindung konfigurieren
        self.connection = serial.Serial(timeout=.1)
        self.connection.baudrate = baudrate
        self.connection.port = port
        # Zeit in Sekunden, für die auf eine Antwort vom Raspi gewartet werden soll
        self.dataRecievingTimeOut = 3

        # Optionales Bestimmen des Betriebsystems, um bessere Fehlermeldungen auszugeben
        self.osType = platform.system()

        try:
            # Verbindungsaufbau
            self.connection.open()
            # Beim Testen mit einem anderen seriellen Gerät war eine Verzögerung zwischen dem Eröffnen der Verbindung und der ersten
            # Datenübertragung notwendig, sonst gingen Daten verloren. Warum? Keine Ahnung.
            time.sleep(2)
            self.testConnection()
            self.__statusFlags["connected"] = True

            while self.__statusFlags["running"]:
                print("running")
            print("disconnecting")
            self.sendData("disconnect", waitForResponse=False)
            self.disconnect()

        # Ausgabe von möglichen Fehlerszenarien, die beim Testen aufgetreten sind
        except serial.SerialTimeoutException:
            messagebox.showerror("Verbindung ausgelaufen", "Die Setzlingsanlage hat nicht innerhalb einer angemessenen Zeit geantwortet. Die Verbindung wurde unterbrochen.")
        except serial.serialutil.SerialException as e:
            if "Permission denied" in str(e) and self.osType == "Linux":
                messagebox.showerror("Fehler beim Verbindungsaufbau", str(e) + "\n\nHaben sie die nötigen Berechtigungen, um auf diesen Port zuzugreifen? Probieren Sie es mit: \n\nsudo chmod a+rw " + str(port))
            else:
                messagebox.showerror("Fehler beim Verbindungsaufbau", str(e) + "\n\nAuf Port:\n\n" + str(port))
        except ConnectionError as e:
            messagebox.showerror("Synchronisierung fehlgeschlagen", "Synchronisierung mit der Setzlingsanlage konnte nicht korrekt durchgeführt werden. Ist das richtige Gerät verbunden?")
    

    def sendData(self, data, waitForResponse=True):
        # Schickt Daten zum Raspberry Pico und wartet auf eine Antwort
        # Das Warten auf die Antwort blockiert zwar den aktuellen Thread, ist aber in den meisten Fällen sinnvoll/ nicht schlimm:
        # 1. Bei "Anfragen", also wenn Werte vom Raspi zum PC übertragen werden sollen, wird sowieso nur eine Anfrage gleichzeitig
        #    abgeschickt, da mehrere Anfragen zu Chaos und einem deutlichen komplizierteren Protokoll führen würden.
        # 2. Bei "Befehlen" bzw. dem Übertragen von Werten vom PC zum Raspi dient die Antwort vom Raspi als Bestätigung, dass die
        #    Verbindung noch am Leben ist.
        # Im Ausnahmefall kann mit "waitForResponse=False" auch auf das Warten verzichtet werden.

        # Es wird vor jede Nachricht der Prefix "pc:" angehängt, um das Zuordnen von Nachrichten und damit das Debugging einfacher
        # zu machen
        message = "pc:" + str(data)
        self.connection.write(bytes(message, "utf-8"))

        if waitForResponse:
            startTimeStamp = time.time()
            while self.connection.in_waiting == 0:
                # Kommt in einer angemessenen Zeit keine Antwort vom Raspi, deutet das auf ein Problem mit der Verbindung hin und
                # führt zu einem Timeout.
                if (time.time() - startTimeStamp) >= self.dataRecievingTimeOut:
                    self.disconnect()
                    raise serial.SerialTimeoutException
            
            if self.connection.in_waiting > 0:
                recieved = self.connection.readline().decode()
                return recieved.replace("\r","").replace("\n","")
    

    def testConnection(self):
        # Dient zum Testen der Verbindung. Der PC schickt ein "pc:sync" und erwartet darauf ein "sa:sync" vom Raspi. Erhält er das,
        # wird die Verbindung als funktionierend bzw. "synchronisiert" angesehen.
        response = self.sendData("sync")
        print(response)
        if not response == "sa:sync":
            self.disconnect()
            raise ConnectionError


    def disconnect(self):
        self.connection.close()
        self.__statusFlags["connected"] = False