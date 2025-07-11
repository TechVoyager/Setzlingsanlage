import json


class SerialDataObject:
    # Der Input-Buffer der seriellen Schnittstelle in Circuitpython ist lediglich 255 Byte groß, was in manchen Fällen nicht ausreicht.
    # Diese Klasse dient dazu auch größere Datenmengen sicher übertragen zu können.
    # Größere Datenmengen werden bei der Initialisierung in eine Liste mit "Chunks" umgewandelt, die jeweils das Format
    # [index]//[JSON Sub-String]// haben. Diese können daraufhin Stück für Stück gesendet werden.

    def __init__(self, data="", chunkSize = 200):
        self.chunks = []

        if data != "":
            # Wir nutzen das json Format, da es uns einen integrierten Parser bietet, um den json-String am Ende wieder in
            # ein Python-Objekt umzuwandeln
            dataString = json.dumps(data)

            index = 0
            for chunkStart in range(0, len(dataString), chunkSize):
                # Umwandlung des json-Strings in Chunks
                chunk = str(index) + "//" + dataString[chunkStart:chunkStart+chunkSize] + "//"
                self.chunks.append(chunk)
                index += 1
    
    def appendChunk(self, chunk: str):
        # Empfangene Chunks können mit dieser Funktion zu einem unvollständigen SerialDataObject hinzugefügt werden

        splitString = chunk.split("//")
        index = int(splitString[0])

        # Rudimentäre Prüfung, ob der gegebene Chunk im aktuellen Kontext Sinn ergibt (ein Chunk, welcher einen kleineren
        # Index als bereits gespeicherte Chunks aufweist, ist kein gutes Zeichen)
        if index == len(self.chunks):
            self.chunks.append(chunk)
            return True
        else:
            print("Chunk doesn't have correct index")
            return False
    
    def parseToPyObj(self, chunks=[]):
        # Dient dazu, die gespeicherten Chunks wieder in eine Python-Objekt umzuwandeln. Bei Bedarf kann auch direkt
        # eine Liste an Chunks übergeben werden

        parsedString = ""
        chunksToParse = chunks
        if len(chunks) == 0:
            chunksToParse = self.chunks
            
        for chunk in chunksToParse:
            splitString = chunk.split("//")
            data = splitString[1]

            parsedString += data

        # der json-Parser nimmt uns die Arbeit ab
        PyObject = json.loads(parsedString)
        return PyObject

    def __iter__(self):
        # Dunder-Funktion, um die Klasse iterable zu machen

        # Index muss bei -1 Starten, damit beim ersten __next__-Aufruf diesr auf 0 gesetzt wird
        self.index = -1
        return self
    
    def __next__(self):
        # Dunder-Funktion, um die Klasse iterable zu machen

        # Bei jedem Aufruf wird lediglich das nächste Element zurückgegeben
        self.index += 1
        if self.index < len(self.chunks):
            return self.chunks[self.index]
        else:
            raise StopIteration