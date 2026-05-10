import pyglet

from basic_elements import Ressources, make_circle, make_box, make_image_sprite, make_text_label, make_rectangle
from landschaftsgenerator import LandschaftGenerator
from spiel_lelements import *

def initialisiere_spiel(spalten: int, zeilen: int, res: Ressources, dritter_spieler: bool) -> Spiel:

    spiel = Spiel()
    spiel.landschaftstypen.append(make_landschaftstyp("Baum", res.images.baum))
    spiel.landschaftstypen.append(make_landschaftstyp("Erde", res.images.erde))
    spiel.landschaftstypen.append(make_landschaftstyp("Turm", res.images.turm))
    spiel.landschaftstypen.append(make_landschaftstyp("Gras", res.images.gras))
    spiel.landschaftstypen.append(make_landschaftstyp("Weg", res.images.weg))

    
    spielBatch = pyglet.graphics.Batch()
    spiel.batch = spielBatch

    generator = LandschaftGenerator()
    spiel.landschaft = generator.make_spiel_landschaft(zeilen, spalten, spiel.landschaftstypen)


    for zeile in spiel.landschaft.zeilen:
        y = spiel.landschaft.zeilen.index(zeile)
        for spalte in zeile.spalten:
            x = zeile.spalten.index(spalte)
            spalte.sprite = make_image_sprite(x * 100, y * 100 , 100, 100, spalte.landschaftstyp.image, spiel.batch)
    
    spiel.spieler_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 10, "i", spiel.batch)
    spiel.info_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 400, "i", spiel.batch)
    return spiel

def make_landschaftstyp(name: str, image: pyglet.image.Texture | pyglet.image.TextureRegion) -> Landschaftstyp:
    landschaftstyp = Landschaftstyp()
    landschaftstyp.name = name
    landschaftstyp.image = image
    return landschaftstyp

def draw_spiel(spiel: Spiel):
    if spiel:
        spiel.batch.draw()