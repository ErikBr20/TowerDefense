import pyglet
from enemy import Enemy
from defender import Defender
from basic_elements import Ressources, make_circle, make_box, make_image_sprite, make_text_label, make_rectangle
from landschaftsgenerator import LandschaftGenerator
from spiel_lelements import *
import random

def initialisiere_spiel(spalten: int, zeilen: int, res: Ressources, dritter_spieler: bool) -> Spiel:

    spiel = Spiel()
    spiel.landschaftstypen.append(make_landschaftstyp("Baum", True, res.images.baum))
    spiel.landschaftstypen.append(make_landschaftstyp("Erde", False, res.images.erde))
    spiel.landschaftstypen.append(make_landschaftstyp("Turm", False, res.images.turm))
    spiel.landschaftstypen.append(make_landschaftstyp("Gras", True, res.images.gras))
    spiel.landschaftstypen.append(make_landschaftstyp("Weg", False, res.images.weg))
    spiel.landschaftstypen.append(make_landschaftstyp("Goldturm", False, res.images.goldturm)) #Bilder laden

    
    spielBatch = pyglet.graphics.Batch()
    spiel.batch = spielBatch #grafik auf en Spielbatch laden

    generator = LandschaftGenerator()
    spiel.landschaft = generator.make_spiel_landschaft(zeilen, spalten, spiel.landschaftstypen)


    for zeile in spiel.landschaft.zeilen:
        y = spiel.landschaft.zeilen.index(zeile)
        screen_y = (spiel.landschaft.anzahl_zeilen - 1 - y) * 100  # Y spiegeln
        for spalte in zeile.spalten:
            x = zeile.spalten.index(spalte)
            spalte.sprite = make_image_sprite(x * 100, screen_y, 100, 100, spalte.landschaftstyp.image, spiel.batch)

    spiel.spieler_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 10, "i", spiel.batch)
    spiel.info_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 400, "i", spiel.batch)
   
    spiel.enemies = []
    warte = 0.0
    for i in range(5): #anzahl enemies
        enemy = Enemy(spiel.landschaft, spiel.batch, res.images.rittergeg_ani, warte_zeit= warte)
        spiel.enemies.append(enemy)
        warte += random.uniform(1.0, 3.0)  # zufälliger Abstand zwischen 1 und 3 Sekunden
    
    spiel.defenders = []
    warte = 0.0
    for i in range(5): #anzahl defender
        defender = Defender(spiel.landschaft, spiel.batch, res.images.ritterdef_ani, warte_zeit= warte)
        spiel.defenders.append(defender)
        warte += random.uniform(1.0, 3.0)
    return spiel

def make_landschaftstyp(name: str, is_random: bool, image: pyglet.image.Texture | pyglet.image.TextureRegion) -> Landschaftstyp:
    landschaftstyp = Landschaftstyp()
    landschaftstyp.name = name
    landschaftstyp.is_random = is_random
    landschaftstyp.image = image
    return landschaftstyp

def draw_spiel(spiel: Spiel):
    if spiel:
        spiel.batch.draw()