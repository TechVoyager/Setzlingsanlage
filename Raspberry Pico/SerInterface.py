# Modul für die serielle Kommunikation mit der Desktopanwendung
import time
import usb_cdc
from helperClasses import SerialDataObject
import json


class SerialInterface:
    def __init__(self):
        # Der Raspi hat zwei Serielle Schnittstellen: Console und Data. Die Konsole schickt selbst Daten, welche
        # unsere Datenübetragung stören würde, daher nutzen wir die Data-Schnittstelle
        self.connection = usb_cdc.data


    def read(self):
        data = ""
        # Wir lesen Daten, bis keine mehr im Buffer sind. Diese Methode war bisher am zuverlässigsten und funktioniert auch,
        # Wenn die Funktion aufgerufen wurde, bevor der PC alle Daten in den Buffer geschrieben hat.
        while self.connection.in_waiting > 0:
            data += self.connection.read(1).decode("utf-8")

        # Wir entfernen noch alle unnötigen Formatierungszeichen
        processed = data.replace("\r","").replace("\n","")

        return processed
    

    def send(self, data):
        # Wandelt die Daten zu Bytes um und schreibt diese in den Buffer
        datastring = ""

        if type(data) == str:
            datastring = data
        else:
            datastring = "json:" + str(json.dumps(data))
        processed = bytes(datastring, "utf-8")
        self.connection.write(processed)
    

    def checkForCommands(self):
        # TO-DO: Entfernen, sobald alles in main.py integriert ist
        # Funktion zum Testen dieser Klasse

        if self.connection.in_waiting > 0:
            command = self.read()

            if command == "sync":
                self.send("sync")
            elif command == "setProfile":
                profile = self.readBigData()
                self.send(profile.keys())
            elif command == "sendProfiles":
                self.send()
            else:
                self.send("unprocessed:"+command)
    

    def readBigData(self):
        # Diese Funktion dient zum Empfangen größerer Datenmengen in Form eines SerialDataObjects. Dieses besteht aus Chunks,
        # die einzeln übertragen und zum Schluss zusammengesetzt werden.

        data = SerialDataObject()
        # Signalisiert dem anderen Gerät, dass das aktuelle Gerät bereit für die Übertragung ist
        self.send("begin")

        # Bei der Übertragung des SerialDataObjects wird der Einfachheit halber nicht die Anzahl an Chunks übetragen, sondern
        # so lange Chunks "gesammelt", bis das "done" Signal vom anderen Gerät kommt. Damit diese Schleife nicht unendlich lang
        # läuft, hat sie einen Timeout
        transmissionStart = time.monotonic()
        while (float(time.monotonic()) - transmissionStart) <= 1:
            # Dieser zweite Timeout ist für die Übertragung jedes einzelnen Chunks angesetzt. Es wird gewartet, bis Daten im
            # Input-Buffer erscheinen
            self.waitTillTimeout(0.5)
            
            recievedPacket = self.read()
            if recievedPacket == "done":
                # Ist die Übertragung beendet, wird aus dem SerialDataObject ein Python-Objekt gemacht
                return data.parseToPyObj()
            else:
                # Standardmäßig wird das empfangene Datenpaket als Chunk gewertet und dem SerialDataObject angefügt.
                # "success" ist hierbei ein bool, welches Auskunft darüber gibt, ob das Datenpaket tatsächlich ein
                # Chunk war und angefügt wurde
                success = data.appendChunk(recievedPacket)
                if success:
                    # Hat alles geklappt, wird nach dem nächsten Datenpaket/ Chunk gefragt
                    self.send("next")
                else:
                    return {}
        

    def waitTillTimeout(self, timeout):
        # Eine Funktion um auf Daten im Input-Buffer zu warten. Natürlich mit Timeout, um den Programmcode nicht zu blockieren.
        # Gibt in Form eines bool zurück, ob der Timeout erreicht wurde oder nicht
        startTime = time.monotonic()
        while self.connection.in_waiting == 0:
            currentTime = time.monotonic()
            if (currentTime - startTime) >= timeout:
                return True
        return False