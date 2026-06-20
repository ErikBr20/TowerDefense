import math
from spiel_lelements import Spiel, RasterFeld

class TurmLogik:
    def __init__(self, raster_feld: RasterFeld):
        self.raster_feld = raster_feld
        self.index_x = raster_feld.index_x
        self.index_y = raster_feld.index_y
        
        # Angriffs-Einstellungen
        self.schaden = 1
        self.angriff_cooldown = 1.0  # Schießt alle 1.0 Sekunden
        self.timer = 0.0

    def update(self, dt: float, spiel: Spiel, res):
        """Wird in jedem Frame aufgerufen, um zu prüfen, ob der Turm schießen kann."""
        if self.timer > 0:
            self.timer -= dt
            return

        # Finde alle Gegner, die sich auf den direkt angrenzenden Feldern befinden
        nahe_gegner = []
        
        for enemy in spiel.enemies:
            # Nur lebendige, sichtbare Gegner angreifen
            if not enemy.sprite.visible:
                continue
            if hasattr(enemy, 'aktiv') and not enemy.aktiv:
                continue

            # Berechne, auf welchem Grid-Feld der Gegner gerade steht (Felder sind 100x100 Pixel groß)
            enemy_grid_x = int(enemy.x / 100)
            enemy_grid_y = int(enemy.y / 100)

            # Prüfen, ob das Feld direkt daneben ist (Abstand im Raster genau 1 oder diagonal/direkt auf dem Turmfeld)
            # dx und dy messen die Feld-Distanz
            dx = abs(self.index_x - enemy_grid_x)
            dy = abs(self.index_y - enemy_grid_y)

            # Direkt daneben bedeutet: Entweder (dx == 1 und dy == 0) oder (dx == 0 und dy == 1)
            if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                nahe_gegner.append(enemy)

        # Wenn Gegner in der Nähe sind, greife den ersten an
        if nahe_gegner:
            ziel_gegner = nahe_gegner[0]
            self.schiesse_auf(ziel_gegner, spiel, res)
            self.timer = self.angriff_cooldown  # Cooldown zurücksetzen

    def schiesse_auf(self, enemy, spiel: Spiel, res):
        # --- HIER NEU: Abschuss-Sound abspielen ---
        # Ersetze 'sounds' oder füge dein richtiges Sound-Objekt ein (z. B. res.sounds.abschuss)
        if hasattr(res, 'sounds') and hasattr(res.sounds, 'abschuss'):
            res.sounds.abschuss.play()
        # Falls du einfach einen vorhandenen Sound testen willst, nimm z. B. res.sounds.play()
        elif hasattr(res, 'sounds') and res.sounds:
            res.sounds5.play() 

        # Zentrum des Turm-Feldes berechnen
        turm_center_x = self.index_x * 100 + 50
        turm_center_y = self.index_y * 100 + 50

        # Importiere die Pfeil-Klasse
        from pfeil import Pfeil
        
        # Pfeil erstellen und der Spielliste hinzufügen
        neuer_pfeil = Pfeil(turm_center_x, turm_center_y, enemy, spiel.batch, res)
        
        if not hasattr(spiel, 'pfeile'):
            spiel.pfeile = []
        spiel.pfeile.append(neuer_pfeil)