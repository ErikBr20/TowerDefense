import pyglet
from enemy import Enemy
from defender import Defender
from basic_elements import Ressources, make_circle, make_box, make_image_sprite, make_text_label, make_rectangle
from landschaftsgenerator import LandschaftGenerator
from spiel_lelements import *
import random
import math
from könig import König

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
    spiel.turm_leben = 300 #turm leben anpassen
    spiel.könig_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 500, "König: 20", spiel.batch)

    spiel.enemies = []
    warte = 0.0
    for i in range(11): #anzahl enemies
        enemy = Enemy(spiel.landschaft, spiel.batch, res.images.rittergeg_ani, warte_zeit= warte)
        spiel.enemies.append(enemy)
        warte += random.uniform(1.0, 3.0)  # zufälliger Abstand zwischen 1 und 3 Sekunden
    koenig = König(spiel.landschaft, spiel.batch, res.images.könig_ani, res.sounds3, warte_zeit=5.0)
    spiel.enemies.append(koenig)  # läuft dann automatisch mit
    
    spiel.defenders = []
    warte = 0.0
    for i in range(300): #anzahl defender
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
            enemy.update(dt)
        for defender in spiel.defenders:
            defender.update(dt)
            # Defender Timer zurücksetzen wenn König spawnt
        for enemy in spiel.enemies:
            if hasattr(enemy, 'ist_könig') and enemy.sprite.visible and enemy.aktiv:
                for defender in spiel.defenders:
                    if defender.angriff_timer <= 0:
                        defender.angriff_timer = random.uniform(0.5, 3.0)

        # Treffer Timer runterzählen
        for enemy in spiel.enemies:
            if hasattr(enemy, 'treffer_timer') and enemy.treffer_timer > 0:
                enemy.treffer_timer -= dt

        # Goldturm Schaden
        for enemy in spiel.enemies:
            if enemy.reached_end:
                enemy.schaden_timer += dt
                intervall = 1.0 if hasattr(enemy, 'ist_könig') else 2.0
                if enemy.schaden_timer >= intervall:
                    enemy.schaden_timer = 0.0
                    if spiel.turm_leben > 0:
                        spiel.turm_leben -= 1
                        spiel.turm_label.text = f"Turm: {spiel.turm_leben}"

        # Game Over prüfen
        if spiel.turm_leben <= 0:
            if not hasattr(spiel, 'game_over') or not spiel.game_over:
                spiel.game_over = True
                spiel.game_over_sprite = pyglet.sprite.Sprite(res.images.gameover, 0, 0, batch=spiel.batch, group=pyglet.graphics.Group(order=100))
                spiel.game_over_sprite.scale_x = 1920 / res.images.gameover.width
                spiel.game_over_sprite.scale_y = 1080 / res.images.gameover.height
        
        # Kollision prüfen
        for enemy in spiel.enemies[:]:
            if not enemy.sprite.visible:
                continue
            if hasattr(enemy, 'aktiv') and not enemy.aktiv:
                continue
            for defender in spiel.defenders[:]:
                dx = enemy.x - defender.x
                dy = enemy.y - defender.y
                abstand = math.sqrt(dx * dx + dy * dy)
                
                if abstand < 40:
                    if hasattr(enemy, 'ist_könig'):
                        if defender.angriff_timer <= 0:
                            res.sounds2.play()
                            enemy.leben -= 1
                            defender.angriff_timer = 1.0
                            spiel.könig_label.text = f"König: {enemy.leben}"
                            if enemy.leben <= 0:
                                if enemy in spiel.enemies:
                                    if enemy.sprite._vertex_list is not None:
                                        enemy.sprite.delete()
                                    spiel.enemies.remove(enemy)
                                break
                    else:
                        res.sounds2.play()
                        if defender in spiel.defenders:
                            if defender.sprite._vertex_list is not None:
                                defender.sprite.delete()
                            spiel.defenders.remove(defender)
                        if enemy in spiel.enemies:
                            if enemy.sprite._vertex_list is not None:
                                enemy.sprite.delete()
                            spiel.enemies.remove(enemy)
                            mehr_muenzen(spiel)
                        break

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

def mouse_press_spiel(spiel: Spiel, x: int, y: int, res:Ressources): 
        rasterFeld = get_spiel_rasterfeld(spiel, x, y)
        if rasterFeld.landschaftstyp.name == "Erde" and spiel.spieler.muenzen >= 2: #geld für turm
            turm_typ = next(x for x in spiel.landschaftstypen if x.name == "Turm")
            rasterFeld.landschaftstyp = turm_typ
            rasterFeld.sprite.image = rasterFeld.landschaftstyp.image
            rasterFeld.sprite.scale_x = 100 / rasterFeld.sprite.image.width
            rasterFeld.sprite.scale_y = 100 / rasterFeld.sprite.image.height
            res.sounds.play()
            spiel.spieler.muenzen -= 2