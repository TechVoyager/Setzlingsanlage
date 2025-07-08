# Modul für Klassen zum Pflanzenprofil-Management
import csv
import os

class Pflanzenprofil():
    # Funktion liest csv-Datei ein und schreibt die Werte in ein Dictionary
    def __init__(self):
        self.Pflanzen_dict = {} # Dictionary zum speichern der Pflanzenwerte
        self.einlesen_csv()


    #Funktion liest csv-Datei ein
    def einlesen_csv(self):
        dirName = os.path.dirname(__file__)
        #__file__ gibt den Pfad bis einschlieslich der Datei an
        # os.path.dirname() gibt den Ordnerpfad bis zur dem Ordner, in dem die Datei drin ist
        # dirName gibt den Ordner an, in dem die Datei liegt, die ausgeführt wird
        # csv-Datei wird wieder geschlossen nach with
        with open(os.path.join(dirName, "Data", "Pflanzenprofile.csv"), mode='r', encoding='utf-8-sig', newline='') as csvdatei:
        # DAVOR: with open(dirName + "/Data/Pflanzenprofile.csv",mode='r', encoding='utf-8-sig', newline='') as csvdatei: 
        # -> besser mit join(): verbindet Pfadbestandteile korrekt und betriebssystemunabhängig
            #encoding='utf-8' -> damit Soonderzeichen gelesen werden können besser utf-8-sig, damit am Anfang keine anderen 
            # Buchstaben sind
            #newline='' -> damit die Zeilenumbrüche richtig eingelesen werden -> genau wie bei der csv-Datei
            csv_reader_object = csv.DictReader(csvdatei, delimiter=';') 
            # csv.DictReader liest csv-Datei als Dict ein
            # delimiter: Trennzeichen in der csv_Datei
            for zeile in csv_reader_object: # jede Zeile ist ein dict
                schluessel = zeile[csv_reader_object.fieldnames[0]] # .fieldnames: Liste mit allen "Überschriften"; [0]:erste Spalte
                                                                    # zeile['Pflanzenprofil'] gibt in der Zeile den Wert zum 
                                                                    # Schlüssel 'Pflanzenprofil' -> Erdbeeren 
                str_to_int = {} 
                for schlüssel, wert in zeile.items():   #Schleife über alle Schlüssel-Wert-Paare in Pflanzenwerte
                                                        # .items() gibt alle Einträge aus dem dict
                    if schlüssel == csv_reader_object.fieldnames[0]:
                        str_to_int[schlüssel] = wert # bleibt string
                    else:
                        try: # probiert string zu int zu konvertieren
                            str_to_int[schlüssel] = int(wert) # Werte als int speichern
                        except ValueError: # falls Konvertierung nicht möglich ist/ falls eine Fehlermeldung kommen sollte
                            str_to_int[schlüssel] = wert # falls Konvertierung nicht möglich bleibt es ein string

                self.Pflanzen_dict[schluessel] = str_to_int # speichert die ganze neue Zeile, mit den int-Werten,unter dem Namen 
                                                            # schlüssel also bspw. Pflanzenart

    # Funktion gibt die Werte der gewünschten Pflanze zurück
    def gib_Pflanzenwerte(self, Pflanze, Wachstum):
        Pflanzenwerte = self.Pflanzen_dict.get(Pflanze)
        if not Pflanzenwerte:
            #falls es die Pflanzenart nicht in der csv-Datei gibt wird "Pflanze nicht gefunden" zurückgegeben
            return f"Pflanze '{Pflanze}' nicht gefunden"
        dict_aktuel = {}
        dict_aktuel["Pflanzenart"] = Pflanzenwerte['Pflanzenart'] # Pflanzenart immer drin, egal ob seed True oder False
        for schlüssel, wert in Pflanzenwerte.items():   #Schleife über alle Schlüssel-Wert-Paare in Pflanzenwerte
                                                        # .items() gibt alle Einträge aus dem dict
            if Wachstum and schlüssel.startswith("S_"):  # wenn Wachstum ==True und schlüssel mit S startet
                dict_aktuel[schlüssel.replace("S_", "")] = wert
            elif not Wachstum and schlüssel.startswith("P_"):
                dict_aktuel[schlüssel.replace("P_", "")] = wert
        return dict_aktuel

    #string mit Name und dict mit Werten als Übergabe bei neuer Pflanzenart
    def neue_Pflanzenart(self, Name, Pflanzendict):
        # Werteliste = list(Pflanzendict.values())
        dirName = os.path.dirname(__file__)
        neues_profil ={"Pflanzenart": Name, **Pflanzendict}
        # **Pflanzendict : Pflanzendict hinzugefügt; falls "Pflanzenart" schon drin wäre: überschreiben
        with open(os.path.join(dirName, "Data", "Pflanzenprofile.csv"), mode='r', encoding='utf-8-sig', newline='') as csvdatei:
            reader = csv.DictReader(csvdatei, delimiter=';')
            Bezeichner = reader.fieldnames  # z.B. ['Tagdauer', ...]
            alle_zeilen = list(reader) # restliche Zeilen werden als Liste von Dictionaries gespeichert
        if Name not in self.Pflanzen_dict:
            #Datei öffnen und Werte hinzufügen mit append
            with open(os.path.join(dirName, "Data", "Pflanzenprofile.csv"), mode='a', encoding='utf-8-sig', newline= '') as csvdatei:
                writer_object = csv.DictWriter(csvdatei, fieldnames=Bezeichner, delimiter= ';') # Delimiter ; damit Liste richtig umgesetzt wird in der csv_Datei
                writer_object.writerow(neues_profil) # neue Zeile im dict wird hinzugefügt
            self.einlesen_csv() #csv-Datei wieder einlesen mit neuer Pflanzenart
            return "Neue Pflanzenart hinzugefügt"
        else:
            # wenn Name in self.Pflanzen_dict:
            # gewünschte Zeile/Pflanzenart ändern bzw. einfach die bestehende Pflanzenart überschreiben
            for i, zeile in enumerate(alle_zeilen): 
                #i : jeder Index der Liste (welche Zeile)
                #zeile: dict mit den Werten der Zeile
                #enumerate(): gibt index und Werte
                if zeile["Pflanzenart"] == Name: # wenn die Pflanzenart in dem dict dem Namen der übergebenen Pflanzenart entspricht
                    alle_zeilen[i] = neues_profil # neue Werte zuweisen; alte werden ersetzt für diese Zeile wenn "Pflanzenart" == Name
                    break
            # Datei neu schreiben
            with open(os.path.join(dirName, "Data", "Pflanzenprofile.csv"), mode='w', encoding='utf-8-sig', newline= '') as csvdatei:
                writer = csv.DictWriter(csvdatei, fieldnames = Bezeichner, delimiter=';')
                writer.writeheader() # erste Zeile schreiben
                writer.writerows(alle_zeilen) # restliche Zeilen schreiben
            self.einlesen_csv()
            return "Pfanzenwerte verändert"

    


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
#Beispiel 1: Alle Profilwerte (erste 8 Spalten) für Erdbeeren
#werte_profil = profil.gib_Pflanzenwerte("Erdbeeren", Wachstum=False)
#print("Profilwerte:", werte_profil)

#Beispiel 2: Nur Wachstumswerte (letzte 7 Spalten + Pflanzenart) für Erdbeeren
#werte_wachstum = profil.gib_Pflanzenwerte("Erdbeeren", Wachstum=True)
#print("Wachstumswerte:", werte_wachstum)

# Beispiel 3: Pflanze, die nicht existiert
#werte_unbekannt = profil.gib_Pflanzenwerte("Bananen", Wachstum=False)
#print(werte_unbekannt)  # Gibt "Pflanze 'Bananen' nicht gefunden" zurück