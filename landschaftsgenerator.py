from dataclasses import dataclass
from typing import List
import random
from spiel_lelements import SpielLandschaft, RasterFeld, Landschaftstyp, SpielZeile

@dataclass
class LandschaftGenerator:
    
    def auswahl_random(self, typen: List[Landschaftstyp]) -> Landschaftstyp:
        random_typen = filter(lambda x: x.is_random is True, typen)
        selected = random.choice(list(random_typen))
        return selected
    
    def mache_weg(self, spielLandschaft: SpielLandschaft, weg_typ: Landschaftstyp) -> None:
        start_zeile = random.randint(0, spielLandschaft.anzahl_zeilen - 1)
        start_spalte = 0
        spielLandschaft.zeilen[start_zeile].spalten[start_spalte].landschaftstyp = weg_typ
        while True: 
            nachbarn = self.bestimme_weg_nachbarn(spielLandschaft, start_zeile, start_spalte, weg_typ)
            if len(nachbarn) == 0:
                return
            else:
                weg_feld = random.choice(nachbarn)
                weg_feld.landschaftstyp = weg_typ
                start_zeile = weg_feld.index_y
                start_spalte = weg_feld.index_x


    def bestimme_weg_nachbarn(self, spielLandschaft: SpielLandschaft, zeile: int, spalte: int, weg_typ: Landschaftstyp) -> List[RasterFeld]:
        nachbarn = []
        if spalte == (spielLandschaft.anzahl_spalten - 1):
            return nachbarn
        else:
            nachbarn.append(spielLandschaft.zeilen[zeile].spalten[spalte + 1])
        if zeile > 0:
            #oberer Nachbar
            if (spalte == 0) or (spielLandschaft.zeilen[zeile - 1].spalten[spalte-1].landschaftstyp != weg_typ):
                nachbarn.append(spielLandschaft.zeilen[zeile - 1].spalten[spalte])
        if zeile < (spielLandschaft.anzahl_zeilen - 1):
            #unterer Nachbar
            if (spalte == 0) or (spielLandschaft.zeilen[zeile + 1].spalten[spalte-1].landschaftstyp != weg_typ):
                nachbarn.append(spielLandschaft.zeilen[zeile + 1].spalten[spalte])
        return nachbarn
    
    def make_spiel_landschaft(self, zeilen: int, spalten: int, typen: List[Landschaftstyp]) -> SpielLandschaft:
        spielLandschaft = SpielLandschaft()
        spielLandschaft.anzahl_spalten = spalten
        spielLandschaft.anzahl_zeilen = zeilen
        for zeile in range(0, zeilen):
            spielzeile = SpielZeile()
            spielLandschaft.zeilen.append(spielzeile)
            for spalte in range(0, spalten):
                rasterfeld = RasterFeld()
                rasterfeld.index_x = spalte
                rasterfeld.index_y = zeile
                rasterfeld.landschaftstyp = self.auswahl_random(typen)
                spielzeile.spalten.append(rasterfeld)
        weg_typ = next(x for x in typen if x.name == "Weg")
        self.mache_weg(spielLandschaft, weg_typ)
        return spielLandschaft