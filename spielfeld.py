import pyglet
from enemy import Enemy
from defender import Defender
from basic_elements import Ressources, make_image_sprite, make_text_label
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
    spiel.türme = []
    spiel.pfeile = []
    global ressources
    ressources = res
    spiel.landschaftstypen.append(make_landschaftstyp("Baum", True, res.images.baum))
    spiel.landschaftstypen.append(make_landschaftstyp("Erde", False, res.images.erde))
    spiel.landschaftstypen.append(make_landschaftstyp("Turm", False, res.images.turm))
    spiel.landschaftstypen.append(make_landschaftstyp("Gras", True, res.images.gras))
    spiel.landschaftstypen.append(make_landschaftstyp("Weg", False, res.images.weg))
    spiel.landschaftstypen.append(make_landschaftstyp("Goldturm", False, res.images.goldturm)) # Bilder laden
    spiel.landschaftstypen.append(make_landschaftstyp("turm2", False, res.images.turm2))
    
    spielBatch = pyglet.graphics.Batch()
    spiel.batch = spielBatch # grafik auf den Spielbatch laden

    generator = LandschaftGenerator()
    spiel.landschaft = generator.make_spiel_landschaft(zeilen, spalten, spiel.landschaftstypen)

    # Schleife durch die Karte: Sprites erstellen UND den Start-Goldturm aktivieren
    for zeile in spiel.landschaft.zeilen:
        y = spiel.landschaft.zeilen.index(zeile)
        screen_y = y * 100
        for spalte in zeile.spalten:
            x = zeile.spalten.index(spalte)
            spalte.sprite = make_image_sprite(x * 100, screen_y, 100, 100, spalte.landschaftstyp.image, spiel.batch)
            if spalte.landschaftstyp.name == "Goldturm":
                from turm import GoldTurm
                neuer_goldturm = GoldTurm(spalte)
                spiel.türme.append(neuer_goldturm)

    spiel.spieler = Spieler()
    spiel.spieler.muenzen_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 300, "Münzen: 0", spiel.batch)
    spiel.turm_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 400, "Turm: 40", spiel.batch)
    spiel.turm_leben = 40 # turm leben anpassen
    spiel.könig_label = make_text_label(spalten * 100 + 10, zeilen * 100 - 500, "König: 20", spiel.batch)

    spiel.enemies = []
    warte = 0.0
    for i in range(50): # anzahl enemies
        enemy = Enemy(spiel.landschaft, spiel.batch, res.images.rittergeg_ani, warte_zeit= warte)
        spiel.enemies.append(enemy)
        warte += random.uniform(1.0, 3.0)  # zufälliger Abstand zwischen 1 und 3 Sekunden
    koenig = König(spiel.landschaft, spiel.batch, res.images.könig_ani, res.sounds3, warte_zeit=60.0)
    spiel.enemies.append(koenig)  # läuft dann automatisch mit
    
    spiel.defenders = []
    warte = 0.0
    for i in range(50): # anzahl defender
        defender = Defender(spiel.landschaft, spiel.batch, res.images.ritterdef_ani, warte_zeit= warte)
        spiel.defenders.append(defender)
        warte += random.uniform(4.0, 6.0)

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
        # 1. Alle Einheiten updaten
        for enemy in spiel.enemies:
            enemy.update(dt)
        for defender in spiel.defenders:
            defender.update(dt)

        # 2. Alle platzierten Türme updaten (Normal- und Goldtürme)
        if hasattr(spiel, 'türme'):
            for turm in spiel.türme:
                turm.update(dt, spiel, res)

        # 3. Alle fliegenden Pfeile updaten
        if hasattr(spiel, 'pfeile'):
            for pfeil in spiel.pfeile[:]:
                pfeil.update(dt, spiel)
                if pfeil.tot:
                    spiel.pfeile.remove(pfeil)

        # 5. Schaden am Spielerturm berechnen, wenn Gegner das Ende erreichen
        for enemy in spiel.enemies:
            if enemy.reached_end:
                enemy.schaden_timer += dt
                intervall = 1.0 if hasattr(enemy, 'ist_könig') else 2.0
                if enemy.schaden_timer >= intervall:
                    enemy.schaden_timer = 0.0
                    if spiel.turm_leben > 0:
                        spiel.turm_leben -= 1
                        spiel.turm_label.text = f"Turm: {spiel.turm_leben}"
                        if hasattr(res, 'sounds6') and res.sounds6:
                            res.sounds6.play()

        # 6. Game Over prüfen
        if spiel.turm_leben <= 0:
            if not hasattr(spiel, 'game_over') or not spiel.game_over:
                spiel.game_over = True
                spiel.game_over_sprite = pyglet.sprite.Sprite(res.images.gameover, 0, 0, batch=spiel.batch, group=pyglet.graphics.Group(order=100))
                spiel.game_over_sprite.scale_x = 1920 / res.images.gameover.width
                spiel.game_over_sprite.scale_y = 1080 / res.images.gameover.height

        # 7. Siegbedingung prüfen (Gibt es noch einen König?)
        for enemy in spiel.enemies:
            if hasattr(enemy, 'ist_könig'):
                break
        else:
            if not hasattr(spiel, 'you_win') or not spiel.you_win:
                spiel.you_win = True
                spiel.you_win_sprite = pyglet.sprite.Sprite(res.images.youwin, 0, 0, batch=spiel.batch, group=pyglet.graphics.Group(order=100))
                spiel.you_win_sprite.scale_x = 1920 / res.images.youwin.width
                spiel.you_win_sprite.scale_y = 1080 / res.images.youwin.height
                
        # 8. Kollision zwischen Verteidigern (Defenders) und Gegnern prüfen
        for enemy in spiel.enemies[:]:
            if not enemy.sprite.visible:
                continue
            if hasattr(enemy, 'aktiv') and not enemy.aktiv:
                continue
            könig_getroffen_diesen_frame = False
            for defender in spiel.defenders[:]:
                if not defender.sprite.visible:
                    continue
                if defender not in spiel.defenders:
                    continue
                dx = enemy.x - defender.x
                dy = enemy.y - defender.y
                abstand = math.sqrt(dx * dx + dy * dy)

                if abstand < 40:
                    if defender.sprite._vertex_list is not None:
                        defender.sprite.delete()
                    if defender in spiel.defenders:
                        spiel.defenders.remove(defender)

                    if hasattr(enemy, 'ist_könig'):
                        if not könig_getroffen_diesen_frame:
                            res.sounds2.play()
                            enemy.leben -= 1
                            könig_getroffen_diesen_frame = True
                            spiel.könig_label.text = f"König: {enemy.leben}"
                            if enemy.leben <= 0:
                                if enemy in spiel.enemies:
                                    if enemy.sprite._vertex_list is not None:
                                        enemy.sprite.delete()
                                    spiel.enemies.remove(enemy)
                                    mehr_muenzen(spiel)
                    else:
                        if enemy in spiel.enemies:
                            res.sounds2.play()
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

def mouse_press_spiel(spiel: Spiel, x: int, y: int, res: Ressources): 
    rasterFeld = get_spiel_rasterfeld(spiel, x, y)
    
    if rasterFeld and rasterFeld.landschaftstyp:
        
        # --- 1. NORMALER TURM WIRD GEUPGRADET ---
        if rasterFeld.landschaftstyp.name == "Turm":
            if spiel.spieler.muenzen >= 5:  
                from turm import TurmLogik
                for turm in spiel.türme:
                    if turm.index_x == rasterFeld.index_x and turm.index_y == rasterFeld.index_y:
                        # Da es turm.stufe nicht mehr gibt, prüfen wir, ob es ein normaler Turm ist
                        if type(turm) == TurmLogik:
                            spiel.spieler.muenzen -= 5
                            spiel.spieler.muenzen_label.text = "Münzen: " + str(spiel.spieler.muenzen)
                            
                            res.sounds.play()
                            
                            # Grafiktyp auf turm2 wechseln
                            turm2_typ = next(x for x in spiel.landschaftstypen if x.name == "turm2")
                            rasterFeld.landschaftstyp = turm2_typ
                            
                            # Führt das Upgrade auf diesem einzelnen Turm durch
                            turm.upgrade(turm2_typ.image)
                            break
            else:
                print("Nicht genug Münzen für Upgrade! (5 benötigt)")

        # --- 2. ERDE: NORMALEN TURM KAUFEN ---
        elif rasterFeld.landschaftstyp.name == "Erde" and spiel.spieler.muenzen >= 2:
            turm_typ = next(x for x in spiel.landschaftstypen if x.name == "Turm")
            rasterFeld.landschaftstyp = turm_typ
            rasterFeld.sprite.image = rasterFeld.landschaftstyp.image
            rasterFeld.sprite.scale_x = 100 / rasterFeld.sprite.image.width
            rasterFeld.sprite.scale_y = 100 / rasterFeld.sprite.image.height
            
            from turm import TurmLogik
            neuer_turm = TurmLogik(rasterFeld)
            spiel.türme.append(neuer_turm)
            
            res.sounds.play()
            spiel.spieler.muenzen -= 2
            spiel.spieler.muenzen_label.text = "Münzen: " + str(spiel.spieler.muenzen)
            
        # --- 3. Klick auf den festen Goldturm blockieren (Er kann nicht gekauft/erweitert werden) ---
        elif rasterFeld.landschaftstyp.name == "Goldturm":
            print("Das ist der legendäre Goldturm. Er verteidigt das Ende des Weges vollautomatisch!")