# Modul für Klassen zum Pflanzenprofil-Management
import csv
import os

class Pflanzenprofil():
    Pflanzen_dict = {} # Dictionary zum speichern der Pflanzenwerte
    #Funktion liest csv-Datei ein
    def einlesen_csv(self):
        dirName = os.path.dirname(__file__)
        #__file__ gibt den Pfad bis einschlieslich der Datei an
        # os.path.dirname() gibt den Ordnerpfad ohne den Dateinamen
        # Datei wird wieder geachlossen nach with
        with open(dirName + "/Data/Pflanzenprofile.csv",mode='r', encoding='utf-8-sig', newline='') as csvdatei:
            #encoding='utf-8' -> damit Soonderzeichen gelesen werden können besser utf-8-sig, damit am Anfang keine anderen Buchstaben sind
            #newline='' -> damit die Zeilenumbrüche richtig eingelesen werden
            csv_reader_object = csv.DictReader(csvdatei, delimiter=';') # delimiter: Trennzeichen in der csv_Datei
            for zeile in csv_reader_object: # jede Zeile ist ein dict
                schluessel = zeile[csv_reader_object.fieldnames[0]] # = zeile['Pflanzenprofil'] gibt in der Zeile den Wert zum Schlüssel 'Pflanzenprofil' -> Erdbeeren 
                self.Pflanzen_dict[schluessel] = zeile # speichert die ganze Zeile unter dem Namen Schluessel
    # Funktion liest csv-Datei ein und schreibt die Werte in ein Dictionary
    def __init__(self):
        self.einlesen_csv()

    # Funktion gibt die Werte der gewünschten Pflanze zurück
    def gib_Pflanzenwerte(self, Pflanze):
        return self.Pflanzen_dict.get(Pflanze, f"Pflanze '{Pflanze}' nicht gefunden") 
        # falls es die Pflanze nicht gibt, wird "Pflanze nicht gefunden" zurückgegeben

    #string mit Name und dict mit Werten als Übergabe bei neuer Pflanzenart
    def neue_Pflanzenart(self, Name, Pflanzendict):
        Werteliste = list(Pflanzendict.values())
        dirName = os.path.dirname(__file__)
        if Name not in self.Pflanzen_dict:
            #Datei öffnen und Werte hinzufügen mit append
            with open(dirName + "/Data/Pflanzenprofile.csv", mode='a', encoding='utf-8-sig', newline= '') as csvdatei:
                writer_object = csv.writer(csvdatei, delimiter= ';') # Delimiter ; damit Liste richtig umgesetzt wird in der csv_Datei
                writer_object.writerow(Werteliste)
        elif Name in self.Pflanzen_dict:
             # Bestehende CSV-Datei einlesen
            with open(dirName + "/Data/Pflanzenprofile.csv", mode='r', encoding='utf-8-sig', newline='') as csvdatei:
                reader = csv.DictReader(csvdatei, delimiter=';')
                Bezeichner = reader.fieldnames  # z.B. ['Pflanzenprofil', 'Gießhaeufigkeit (pro Woche)', ...]
                alle_zeilen = list(reader) # restliche Zeilen werden als Liste von Dictionaries gespeicher
            # gewünschte Zeile ändern
            for i, zeile in enumerate(alle_zeilen): 
                #i : jeder Index der Liste(welche Zeile)
                #zeile: dict mit den Werten der Zeile
                #enumerate(): gibt index und Werte
                if zeile[Bezeichner[0]] == Name: # wenn das Pflanzenprofil dem Name entspricht
                    alle_zeilen[i] = Pflanzendict # neue Werte zuweisen
                    break
            # Datei neu schreiben
            with open(dirName + "/Data/Pflanzenprofile.csv", mode='w', encoding='utf-8-sig', newline= '') as csvdatei:
                writer = csv.DictWriter(csvdatei, fieldnames = Bezeichner, delimiter=';')
                writer.writeheader() # erste Zeile schreiben
                writer.writerows(alle_zeilen) # restliche Zeilen schreiben
            return "Pfanzenwerte verändert"
        self.einlesen_csv() #csv-Datei wieder einlesen mit neuer Pflanzenart
        return "Neue Pflanzenart hinzugefügt"
    
"""    # Funktion schreibt neue Werte in die CSV-Datei
    def neue_Pflanzenart(self, Pflanzenart, Gießhaeufigkeit, Tagdauer, Nachtdauer, 
                         BodentempTag, BodentempNacht, Lufttemp, Luftfeuchte, Bodenfeuchte):
        Werteliste = [Pflanzenart, Gießhaeufigkeit, Tagdauer, Nachtdauer, 
                         BodentempTag, BodentempNacht, Lufttemp, Luftfeuchte, Bodenfeuchte]
        dirName = os.path.dirname(__file__)
        if Pflanzenart not in self.Pflanzen_dict:
            #Datei öffnen
            with open(dirName + "/Data/Pflanzenprofile.csv", mode='a', encoding='utf-8-sig', newline= '') as csvdatei:
                writer_object = csv.writer(csvdatei, delimiter= ';') # Delimiter ; damit Liste richtig umgesetzt wird in der csv_Datei
                writer_object.writerow(Werteliste)
        elif Pflanzenart in self.Pflanzen_dict:
            with open(dirName + "/Data/Pflanzenprofile.csv", mode='w', encoding='utf-8-sig', newline= '') as csvdatei:
                writer_object = csv.writer(csvdatei, delimiter= ';') # Delimiter ; damit Liste richtig umgesetzt wird in der csv_Datei
                writer_object.writerow(Werteliste)
        # elif pflanzenart in dict -> in self.pflanzendict neue werte schreiben mit w
        self.einlesen_csv() #csv-Datei wieder einlesen mit neuer Pflanzenart
        return "Neue Pflanzenart hinzugefügt"
"""    

neuesPflanzendict = {"Pflanzenprofil" : "Salat","Gießhaeufigkeit (pro Woche)": 1, "Tagdauer (in h)": 2, "Nachtdauer (in h)": 3,
                   "Bodentemperatur Tag (in °C)": 4, "Bodentemperatur Nacht (in °C)": 5, "Lufttemperatur (in °C)": 6, 
                   "Luftfeuchte (in %RH)": 7, "Bodenfeuchte (in %RH)": 8}
verbessertesPflanzendict = {"Pflanzenprofil" : "Salat","Gießhaeufigkeit (pro Woche)": 8, "Tagdauer (in h)": 7, "Nachtdauer (in h)": 6,
                   "Bodentemperatur Tag (in °C)": 5, "Bodentemperatur Nacht (in °C)": 4, "Lufttemperatur (in °C)": 3, 
                   "Luftfeuchte (in %RH)": 2, "Bodenfeuchte (in %RH)": 1}
print(neuesPflanzendict)
Pflanze = Pflanzenprofil()
#print(Pflanze.Pflanzen_dict)
#print(Pflanze.gib_Pflanzenwerte("Erdbeeren"))
#print(Pflanze.gib_Pflanzenwerte("Salat"))
#print(Pflanze.neue_Pflanzenart('Karotte',2,3,4,5,6,7,8, 9))
#print(Pflanze.gib_Pflanzenwerte("Karotte"))
print(Pflanze.neue_Pflanzenart("Salat", neuesPflanzendict))
print(Pflanze.neue_Pflanzenart("Salat", verbessertesPflanzendict))