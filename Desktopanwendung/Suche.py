# Suchfunktion, die Liste mit Pflanzen und einen unfertigen string übergeben bekommt. 
# Gibt eine Liste mit den Pflanzenartren zurück, die den string enthalten

class Suche:
     def __init__(self):
          self.passendePflanzenarten = []

    # soll alle Pflanzenarten zurückgeben, die die Suche enthalten
    # Suche ist ein string, der übergeben wird
    # Suchliste, die durchsucht wird, wird übergeben
     def Suche_Pflanzenart(self, suchstring, suchliste):
         self.passendePflanzenarten.clear() # Liste leeren
         suchstring = suchstring.lower() # alles auf Kleinbuchstaben setzten
         for pflanze in suchliste: # jedes Element der Liste wird geprüft
             pflanze_lower = pflanze.lower()
             if self.ist_Enthalten(suchstring, pflanze_lower): # falls string enthalten: True
                 self.passendePflanzenarten.append(pflanze) # Pflanze wird zur Liste hinzugefügt
         if len(self.passendePflanzenarten) == 0:
             return []
         return self.passendePflanzenarten
     
     def ist_Enthalten(self, suchstring, suchbereich):
         enthalten = True
         len_suchstring = len(suchstring)
         len_suchbereich = len(suchbereich)
         if len_suchstring > len_suchbereich: # wenn der Suchstring länger als der Suchbereich ist -> nicht enthalten
             enthalten = False 
         for start in range(len_suchbereich - len_suchstring + 1):
             # range(7): start von 0 bis 6
             # so lange der suchstring noch ganz im suchbereich enthalten sein kann, wird die Schleife ausgeführt
             # start ist immer der Startpunkt für den suchstring; ab da wird verglichen
             # strat: mögliche Startwerte im Suchbereich
             enthalten = True # damit man weiß, ob die innere for-Schleife abgebrochen (suche nicht enthalten) wurde oder nicht
             for buchstabe in range(len_suchstring):
                 # jeder Buchstabe des suchstrings wird geprüft
                 # range(len_suche): von 0 bis zur Länge des suchstrings
                 if suchstring[buchstabe] != suchbereich[start + buchstabe]: # Buchstabe vom suchstring stimmt nicht mit 
                 # suchstring[buchstabe]: ein buchstabe im suchstring
                 # suchbereich[start + buchstabe]: + buchstabe: iteriert über jeden Buchstaben vom möglichen Startwert (bis zum Ende)
                     enthalten = False
                     break # innere Schleife wird abgebrochen, da suchstring nicht enthalten ist (sobald ein Buchstabe nicht passt)
         # wenn die Schleife ganz durch ist und kein "nicht-enthalten" gefunden wurde
             if enthalten:
                 return True # ganzer suchstring wurde gefunden
         return False # falls die ganze Schleife durchgegangen wurde, aber nichts gefunden wurde 
            # Bsp.: Baum in Rosengarten; äußere Schleife läuft durch, aber es wird nichts gefunden 

#suche = Suche()
#suchliste = ["Baum", "Rosengarten", "Tag"]
#print(suche.Suche_Pflanzenart("Rosen", suchliste))
#print(suche.Suche_Pflanzenart("Salat", suchliste))