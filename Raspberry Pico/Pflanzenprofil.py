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
        with open(dirName + "/Data/Pflanzenprofile.csv",encoding='utf-8-sig', newline='') as csvdatei:
            #encoding='utf-8' -> damit Soonderzeichen gelesen werden können besser utf-8-sig, damit am Anfang keine anderen Buchstaben sind
            #newline='' -> damit die Zeilenumbrüche richtig eingelesen werden
            csv_reader_object = csv.DictReader(csvdatei, delimiter=';') # delimiter: Trennzeichen in der csv_Datei
            for zeile in csv_reader_object: # jede Zeile ist ein dict
                schluessel = zeile[csv_reader_object.fieldnames[0]] # = row['Pflanzenprofil'] gibt in der Zeile den Wert zum Schlüssel 'flanzenprofil' -> Erdbeeren 
                self.Pflanzen_dict[schluessel] = zeile # speichert die ganze Zeile unter dem namen Schluessel
    # Funktion liest csv-Datei ein und schreibt die Werte in ein Dictionary
    def __init__(self):
        self.einlesen_csv()
        """dirName = os.path.dirname(__file__)
        #__file__ gibt den Pfad bis einschlieslich der Datei an
        # os.path.dirname() gibt den Ordnerpfad ohne den Dateinamen
        # Datei wird wieder geachlossen nach with
        with open(dirName + "/Data/Pflanzenprofile.csv",encoding='utf-8-sig', newline='') as csvdatei:
            #encoding='utf-8' -> damit Soonderzeichen gelesen werden können besser utf-8-sig, damit am Anfang keine anderen Buchstaben sind
            #newline='' -> damit die Zeilenumbrüche richtig eingelesen werden
            csv_reader_object = csv.DictReader(csvdatei, delimiter=';') # delimiter: Trennzeichen in der csv_Datei
            for zeile in csv_reader_object: # jede Zeile ist ein dict
                schluessel = zeile[csv_reader_object.fieldnames[0]] # = row['Pflanzenprofil'] gibt in der Zeile den Wert zum Schlüssel 'flanzenprofil' -> Erdbeeren 
                self.Pflanzen_dict[schluessel] = zeile # speichert die ganze Zeile unter dem namen Schluessel"""

    # Funktion gibt die Werte der gewünschten Pflanze zurück
    def gib_Pflanzenwerte(self, Pflanze):
        return self.Pflanzen_dict.get(Pflanze, f"Pflanze '{Pflanze}' nicht gefunden") 
        # falls es die Pflanze nicht gibt, wird "Pflanze nicht gefunden" zurückgegeben
    
    # Funktion schreibt neue Werte in die CSV-Datei
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
        self.einlesen_csv() #csv-Datei wieder einlesen mit neuer Pflanzenart
        return "Neue Pflanzenart hinzugefügt"

"""Pflanze = Pflanzenprofil()
print(Pflanze.Pflanzen_dict)
print(Pflanze.gib_Pflanzenwerte("Erdbeeren"))
print(Pflanze.gib_Pflanzenwerte("Salat"))
print(Pflanze.neue_Pflanzenart('Karotte',2,3,4,5,6,7,8, 9))
print(Pflanze.gib_Pflanzenwerte("Karotte"))
"""