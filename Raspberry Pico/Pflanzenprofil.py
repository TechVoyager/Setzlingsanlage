# Modul für Klassen zum Pflanzenprofil-Management
import csv
import os

class Pflanzenprofil():
    Pflanzen_dict = {} # Dictionary zum speichern der Pflanzenwerte

    #Funktion liest csv-Datei ein
    def einlesen_csv(self):
        dirName = os.path.dirname(__file__)
        #__file__ gibt den Pfad bis einschlieslich der Datei an
        # os.path.dirname() gibt den Ordnerpfad bis zur dem Ordner, in dem die Datei drin ist
        # dirName gibt den Ordner an, in dem die Datei liegt, die ausgeführt wird
        # csv-Datei wird wieder geschlossen nach with
        with open(dirName + "/Data/Pflanzenprofile.csv",mode='r', encoding='utf-8-sig', newline='') as csvdatei:
            #encoding='utf-8' -> damit Soonderzeichen gelesen werden können besser utf-8-sig, damit am Anfang keine anderen Buchstaben sind
            #newline='' -> damit die Zeilenumbrüche richtig eingelesen werden -> genau wie bei der csv-Datei
            csv_reader_object = csv.DictReader(csvdatei, delimiter=';') 
            # csv.DictReader liest csv-Datei als Dict ein
            # delimiter: Trennzeichen in der csv_Datei
            for zeile in csv_reader_object: # jede Zeile ist ein dict
                schluessel = zeile[csv_reader_object.fieldnames[0]] # = zeile['Pflanzenprofil'] gibt in der Zeile den Wert zum Schlüssel 'Pflanzenprofil' -> Erdbeeren 
                self.Pflanzen_dict[schluessel] = zeile # speichert die ganze Zeile unter dem Namen Schluessel, also der Pflanzenart

    # Funktion liest csv-Datei ein und schreibt die Werte in ein Dictionary
    def __init__(self):
        self.einlesen_csv()

    # Funktion gibt die Werte der gewünschten Pflanze zurück
    def gib_Pflanzenwerte(self, Pflanze, Wachstum):
        Pflanzenwerte = self.Pflanzen_dict.get(Pflanze)
        if not Pflanzenwerte:
            #falls es die Pflanzenart nicht in der csv-Datei gibt wird "Pflanze nicht gefunden" zurückgegeben
            return f"Pflanze '{Pflanze}' nicht gefunden"
        dict_aktuel = {}
        dict_aktuel["Pflanzenart"] = Pflanzenwerte['Pflanzenart'] # Pflanzenart immer drin, egal ob seed True oder False
        for schlüssel, wert in Pflanzenwerte.items():   #Schleife über alle Schlüssel-Wert-Paare in Pflanzenerte
                                                         # .items() gibt alle Einträge aus dem dict
            if Wachstum and schlüssel.startswith("S_"):  # wenn Wachstum ==True und schlüssel mit S startet
                dict_aktuel[schlüssel] = wert 
            elif not Wachstum and schlüssel.startswith("P_"):
                dict_aktuel[schlüssel] = wert
        return dict_aktuel

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
                Bezeichner = reader.fieldnames  # z.B. ['Pflanzenprofil', 'Tagdauer'...]
                alle_zeilen = list(reader) # restliche Zeilen werden als Liste von Dictionaries gespeichert
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
    


#neuesPflanzendict = {"Pflanzenart" : "Salat", "P_Tagdauer": 2, "P_Nachtdauer": 3,
#                   "P_Bodentemperatur_tag": 4, "P_Bodentemperatur_nacht": 5, "P_Lufttemperatur": 6, 
#                   "P_Luftfeuchte": 7, "P_Bodenfeuchte": 8}
#verbessertesPflanzendict = {"Pflanzenart" : "Salat", "Tagdauer": 7, "Nachtdauer": 6,
#                   "Bodentemperatur_tag": 5, "Bodentemperatur_nacht": 4, "Lufttemperatur": 3, 
#                   "Luftfeuchte": 2, "Bodenfeuchte": 1}
#print(neuesPflanzendict)
#Pflanze = Pflanzenprofil()
#print(Pflanze.Pflanzen_dict)
#print(Pflanze.gib_Pflanzenwerte("Erdbeeren"))
# Ausgabe: {'Pflanzenart': 'Erdbeeren', 'Tagdauer': '10', 'Nachtdauer': '8', 
#           'Bodentemperatur Tag': '20', 'Bodentemperatur Nacht': '10', 'Lufttemperatur': '20', 
#           'Luftfeuchte': '70', 'Bodenfeuchte': '0'}
#print(Pflanze.gib_Pflanzenwerte("Salat"))
#print(Pflanze.neue_Pflanzenart('Karotte',2,3,4,5,6,7,8, 9))
#print(Pflanze.gib_Pflanzenwerte("Karotte"))
#print(Pflanze.neue_Pflanzenart("Salat", neuesPflanzendict))
#print(Pflanze.neue_Pflanzenart("Salat", verbessertesPflanzendict))
#profil = Pflanzenprofil()
# Beispiel 1: Alle Profilwerte (erste 8 Spalten) für Erdbeeren
#werte_profil = profil.gib_Pflanzenwerte("Erdbeeren", Wachstum=False)
#print("Profilwerte:", werte_profil)

# Beispiel 2: Nur Wachstumswerte (letzte 7 Spalten + Pflanzenart) für Erdbeeren
#werte_wachstum = profil.gib_Pflanzenwerte("Erdbeeren", Wachstum=True)
#print("Wachstumswerte:", werte_wachstum)

# Beispiel 3: Pflanze, die nicht existiert
#werte_unbekannt = profil.gib_Pflanzenwerte("Bananen", Wachstum=False)
#print(werte_unbekannt)  # Gibt "Pflanze 'Bananen' nicht gefunden" zurück