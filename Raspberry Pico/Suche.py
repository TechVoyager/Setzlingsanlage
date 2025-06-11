# Suchfunktion, die Liste mit Pflanzen und einen unfertigen string übergeben bekommt. 
# Gibt eine Liste mit den Pflanzenartren zurück, die den string enthalten
import csv
import os

class Suche:
     def __init__(self):
          self.Pflanzenarten = self.Pflanzenarten_Liste()
          self.passendePflanzenarten = []
          
     def Pflanzenarten_Liste(self):
            dirName = os.path.dirname(__file__)
            #__file__ gibt den Pfad bis einschlieslich der Datei an
            # os.path.dirname() gibt den Ordnerpfad ohne den Dateinamen
            Pflanzen_liste = [] # nötig, damit keine Fehler beim erstellen den Attributs auftritt
            #print(Pflanzenarten)
            # Datei wird wieder geschlossen nach with
            with open(dirName + "/Data/Pflanzenprofile.csv",mode='r', encoding='utf-8-sig', newline='') as csvdatei:
                #encoding='utf-8' -> damit Soonderzeichen gelesen werden können besser utf-8-sig, damit am Anfang keine anderen Buchstaben sind
                #newline='' -> damit die Zeilenumbrüche richtig eingelesen werden
                csv_reader_object = csv.DictReader(csvdatei, delimiter=';') # delimiter: Trennzeichen in der csv_Datei
                for zeile in csv_reader_object: # jede Zeile ist ein dict
                    if zeile: # prüfen,, ob die Zeile nicht leer ist
                        Pflanzen_liste.append(zeile['Pflanzenart']) # Liste erstellen mit den Pflanzenarten
                    #print("erstellte Pflanzenliste", Pflanzen_liste)
            return Pflanzen_liste

    # soll alle Pflanzenarten zurückgeben, die die Suche enthalten
    # Suche ist ein string, der übergeben wird
     def Suche_Pflanzenart(self, Suchstring):
        self.passendePflanzenarten.clear() # Liste jedes Mal bei einer neuen Suche leeren
        #self.Pflanzenarten = self.Pflanzenarten_Liste() -> nicht mehr nötig da in __init die Liste verändert wird
        #print("Suche_Pflanzenart: self.Pflanzenarten", self.Pflanzenarten)
        #print("Suche_Pflanzenart: self.passendePflanzenarten", self.passendePflanzenarten)
        #print("Suche_Pflanzenart: Suchstring", Suchstring)
        # passendePflanzenarten = [] in __init() erstellt
        for Pflanze in self.Pflanzenarten:
            if Suchstring.lower() in Pflanze.lower(): # .lower() damit Groß-/Kleinbuchstaben egal sind
                self.passendePflanzenarten.append(Pflanze)
        if len(self.passendePflanzenarten) == 0:
            self.passendePflanzenarten.append ("keine passende Pflanzenart gefunden")
        return self.passendePflanzenarten

KlassenelementSuche = Suche()
print("1", KlassenelementSuche.Pflanzenarten)
print("2", KlassenelementSuche.passendePflanzenarten)
print("3", KlassenelementSuche.Suche_Pflanzenart("Beere"))
print("4", KlassenelementSuche.Suche_Pflanzenart("salat"))
