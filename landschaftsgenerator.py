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
        return spielLandschaft