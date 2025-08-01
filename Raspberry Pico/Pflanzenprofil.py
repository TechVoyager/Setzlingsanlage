# Modul für Klassen zum Pflanzenprofil-Management
import circuitpython_csv as csv

class Pflanzenprofil():
    # Funktion liest csv-Datei ein und schreibt die Werte in ein Dictionary
    def __init__(self):
        self.Pflanzen_dict = {} # Dictionary zum speichern der Pflanzenwerte
        self.einlesen_csv()


    #Funktion liest csv-Datei ein
    def einlesen_csv(self):
        # csv-Datei wird wieder geschlossen nach with
        with open("Data/Pflanzenprofile.csv", mode='r', encoding='utf-8-sig') as csvdatei:
            csv_reader_object = csv.DictReader(csvdatei, delimiter=';') 
            # csv.DictReader liest csv-Datei als Dict ein
            # delimiter: Trennzeichen in der csv_Datei
            for zeile in csv_reader_object: # jede Zeile ist ein dict

                # Anmerkung von Nicolas: Wenn ein Wert None ist (z.B. in der letzten Zeile) führt das zu sehr eigenartig geformten
                # Dictionaries (bei denen die Keys nicht vollstädnig von Anführungszeichen umgeben sind).
                # Solche Zeilen müssen übersprungen werden! Das zu Finden war echt viel Arbeit
                if zeile[csv_reader_object.fieldnames[0]] is None:
                    continue

                schluessel = zeile[csv_reader_object.fieldnames[0]] # .fieldnames: Liste mit allen "Überschriften"; [0]:erste Spalte
                                                                    # zeile['Pflanzenprofil'] gibt in der Zeile den Wert zum 
                                                                    # Schlüssel 'Pflanzenprofil' -> Erdbeeren 
                str_to_int = {} 
                for schlüssel, wert in zeile.items():   #Schleife über alle Schlüssel-Wert-Paare in Pflanzenwerte
                                                        # .items() gibt alle Einträge aus dem dict
                    if schlüssel == csv_reader_object.fieldnames[0]:
                        str_to_int[str(schlüssel).strip()] = wert # bleibt string
                    else:
                        try: # probiert string zu int zu konvertieren
                            str_to_int[str(schlüssel).strip()] = int(wert) # Werte als int speichern
                        except ValueError: # falls Konvertierung nicht möglich ist/ falls eine Fehlermeldung kommen sollte
                            str_to_int[str(schlüssel).strip()] = wert # falls Konvertierung nicht möglich bleibt es ein string
                print(str_to_int.keys())

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
        neues_profil ={"Pflanzenart": Name}
        for key in Pflanzendict:
            neues_profil[key] = Pflanzendict[key]
        # **Pflanzendict : Pflanzendict hinzugefügt; falls "Pflanzenart" schon drin wäre: überschreiben
        # Anmerkung von Nicolas: der Syntax **Pflanzendict funktioniert unter Circuitpython nicht. Habe die Zeile daher angepasst.
        with open("Data/Pflanzenprofile.csv", mode='r', encoding='utf-8-sig', newline= '') as csvdatei:
            reader = csv.DictReader(csvdatei, delimiter=';')
            Bezeichner = reader.fieldnames  # z.B. ['Tagdauer', ...]
            alle_zeilen = list(reader) # restliche Zeilen werden als Liste von Dictionaries gespeichert
        if Name not in self.Pflanzen_dict:
            #Datei öffnen und Werte hinzufügen mit append
            with open("Data/Pflanzenprofile.csv", mode='a', encoding='utf-8-sig', newline= '') as csvdatei:
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
            with open("Data/Pflanzenprofile.csv", mode='w', encoding='utf-8-sig', newline= '') as csvdatei:
                writer = csv.DictWriter(csvdatei, fieldnames = Bezeichner, delimiter=';')
                writer.writeheader() # erste Zeile schreiben
                writer.writerows(alle_zeilen) # restliche Zeilen schreiben
            self.einlesen_csv()
            return "Pfanzenwerte verändert"

    


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