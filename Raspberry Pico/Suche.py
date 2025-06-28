# Suchfunktion, die Liste mit Pflanzen und einen unfertigen string übergeben bekommt. 
# Gibt eine Liste mit den Pflanzenartren zurück, die den string enthalten

class Suche:
     def __init__(self):
          self.passendePflanzenarten = []

    # soll alle Pflanzenarten zurückgeben, die die Suche enthalten
    # Suche ist ein string, der übergeben wird
    # Liste, die durchsucht wird, wird übergeben
     def Suche_Pflanzenart(self, Suchstring, Suchliste):
        self.passendePflanzenarten.clear() # Liste jedes Mal bei einer neuen Suche leeren
        # passendePflanzenarten = [] in __init() erstellt
        for Pflanze in Suchliste:
            if Suchstring.lower() in Pflanze.lower(): # .lower() damit Groß-/Kleinbuchstaben egal sind
                self.passendePflanzenarten.append(Pflanze)
        if len(self.passendePflanzenarten) == 0:
            return []
        return self.passendePflanzenarten