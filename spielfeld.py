import pyglet
from enemy import Enemy
from defender import Defender
from basic_elements import Ressources, make_circle, make_box, make_image_sprite, make_text_label, make_rectangle
from landschaftsgenerator import LandschaftGenerator
from spiel_lelements import *
import random
import math

spiel: Spiel = None
ressources: Ressources = None

def update(dt):
    spiel_update(spiel, dt, ressources)

def initialisiere_spiel(spalten: int, zeilen: int, res: Ressources, dritter_spieler: bool) -> Spiel:

    global spiel
    spiel = Spiel()
    global ressources
    ressources = res
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
        screen_y = y * 100
        for spalte in zeile.spalten:
            x = zeile.spalten.index(spalte)
            spalte.sprite = make_image_sprite(x * 100, screen_y, 100, 100, spalte.landschaftstyp.image, spiel.batch)
    spiel.spieler = Spieler()
    spiel.spieler.muenzen_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 300, "Münzen: 0", spiel.batch)
    spiel.turm_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 400, "Turm: 300", spiel.batch)
   
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

    pyglet.clock.schedule_interval(update, 1/60)
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

def mehr_muenzen(spiel: Spiel):
    spiel.spieler.muenzen += 1
    spiel.spieler.muenzen_label.text = "Münzen: " + str(spiel.spieler.muenzen)

def spiel_update(spiel: Spiel, dt: float, res: Ressources):
    if spiel:
        for enemy in spiel.enemies:
            #print(f"pos=({enemy.x:.0f},{enemy.y:.0f})")
            enemy.update(dt)
        for defender in spiel.defenders:
            defender.update(dt)

    # Kollision prüfen
        for enemy in spiel.enemies[:]:
            for defender in spiel.defenders[:]:
                # Abstand zwischen enemy und defender berechnen
                dx = enemy.x - defender.x
                dy = enemy.y - defender.y
                abstand = math.sqrt(dx * dx + dy * dy)
                
                # Wenn sie sich berühren (näher als 40 Pixel)
                if abstand < 40:
                    res.sounds.play()
                    # Beide vom Bildschirm entfernen
                    enemy.sprite.delete()
                    defender.sprite.delete()
                    spiel.enemies.remove(enemy)
                    spiel.defenders.remove(defender)
                    mehr_muenzen(spiel)

def get_spiel_rasterfeld(spiel: Spiel, x: int, y: int) -> RasterFeld:
    index_x = int(x / 100)
    index_y = int(y / 100)
    print("spalte "+str(index_x)+" zeile "+str(index_y))
    if spiel:
        if index_y >= 0 and index_y < len(spiel.landschaft.zeilen):
            zeile = spiel.landschaft.zeilen[index_y]
            if index_x >= 0 and index_x < len(zeile.spalten):
                return zeile.spalten[index_x]
    return None