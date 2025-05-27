# Modul für Klassen zum Pflanzenprofil-Management
import csv
import os

class Pflanzenprofil():

    def __init__(self):

        dirName = os.path.dirname(__file__)
        # nach with-Block wird die Datei wieder geschlossen
        with open(dirName + "/Data/Pflanzenprofile.csv") as csvdatei:
            csv_reader_object = csv.reader(csvdatei, delimiter=";")
            # delimiter: Info mit was die csv-Datei die Teile trennt
            self.Liste = list(csv_reader_object)
            self.Erdbeere = self.Liste[1]
            self.Rosen = self.Liste[2]
            self.Gerbera = self.Liste[3]
            self.Lilien = self.Liste[4]
            # self.liste["Erdbeere"]

    # gibt Infos der einzelnen Pflanzen
    def Pflanzen_Info(self, pflanze):
        i = pflanze
        print(f"Pflanze: {self.Liste[i][0]}")
        print(f"Wassermenge(in l): {self.Liste[i][1]}, Gießhäufigkeit(pro Woche): {self.Liste[i][2]}, ") 
        print(f"Tagdauer(in h): {self.Liste[i][3]}, Nachtdauer(in h): {self.Liste[i][4]}, ")
        print(f"Bodentemperatur Tag(inC): {self.Liste[i][5]}, Bodentemperatur Nacht(in°C): {self.Liste[i][6]}, ") 
        print(f"Luftfeuchtigkeit(in%RH): {self.Liste[i][7]}")
        print()

    # gibt die ganze Liste aus
    def gib_Liste(self):
        i = 1
        while i < len(self.Liste):
            print(f"Pflanze: {self.Liste[i][0]}, Wassermenge: {self.Liste[i][1]}, Gießhäufigkeit: {self.Liste[i][2]}, Tagdauer: {self.Liste[i][3]}")
            print(f"Nachtdauer: {self.Liste[i][4]},  Bodentemperatur Tag: {self.Liste[i][5]}, Bodentemperatur Nacht: {self.Liste[i][6]}, Luftfeuchtigkeit: {self.Liste[i][7]}")
            print()         
            i += 1

    # alte Infos nicht mehr nötig
    def gib_Infos(self):
        # aus der csv-Datei lesen
        with open('./Data/Pflanzenprofile.csv') as csvdatei:
                csv_reader_object = csv.reader(csvdatei, delimiter=';')
                # delimiter: Info mit was die csv-Datei die Teile trennt
                kopfzeile = next(csv_reader_object)
                # Kopfzeile wird überstprungen und in kopfzeile gespeichert
                for row in csv_reader_object:
                    print("----- Neue Pflanze -----")
                    print(f"Pflanze: {row[0]}, Wassermenge: {row[1]}, Gießhäufigkeit: {row[2]}, Tagdauer: {row[3]}")
                    print(f"Nachtdauer: {row[4]},  Bodentemperatur: {row[5]}, Luftfeuchtifkeit: {row[6]} ")
                    print()  # Leerzeile für bessere Lesbarkeit

                
    def gib_Pflanzenart(self, pflanze):
        return self.Liste[pflanze][0]

    # gibt Wassermenge zurück mit Zahlenangabe zur Pflanzenartbestimmung
    def gib_Wassermenge(self, pflanze):
        Wassermenge = self.Liste[pflanze][1]
        return Wassermenge
    
    def gib_Gießhäufigkeit(self, pflanze):
        return self.Liste[pflanze][2]
    
    def gib_Tagdauer(self, pflanze):
        return self.Liste[pflanze][3]

    def gib_Nachtdauer(self, pflanze):
        return self.Liste[pflanze][4]
    
    def gib_BodentemperaturTag(self, pflanze):
        return self.Liste[pflanze][5]
    
    def gib_BodentemperaturNacht(self, pflanze):
        return self.Liste[pflanze][6]
    
    def gib_Luftfeuchtigkeit(self, pflanze):
        return self.Liste[pflanze][7]

Pflanze = Pflanzenprofil()
print("Pflanzenart: ", Pflanze.gib_Pflanzenart(3))
print("Wassermenge: ", Pflanze.gib_Wassermenge(3))
print("Gießhäufigkeit: ", Pflanze.gib_Gießhäufigkeit(3))
print("Tagdauer: ", Pflanze.gib_Tagdauer(3))
print("Nachtdauer: ", Pflanze.gib_Nachtdauer(3))
print("Bodentemperatur Tag: ", Pflanze.gib_BodentemperaturTag(3))
print("Bodentemperatur Nacht: ", Pflanze.gib_BodentemperaturNacht(3))
print("Luftfeuchtigkeit: ", Pflanze.gib_Luftfeuchtigkeit(3))
Pflanze.gib_Liste()
Pflanze.Pflanzen_Info(2)