import math
from spiel_lelements import Spiel, RasterFeld

class TurmLogik:
    #Der normale Standard-Turm (Stufe 1)
    def __init__(self, raster_feld: RasterFeld):
        self.raster_feld = raster_feld
        self.index_x = raster_feld.index_x
        self.index_y = raster_feld.index_y
        
        # Einstellungen für den normalen Turm
        self.schaden = 1
        self.angriff_cooldown = 4.0  # Schießt alle 4 Sekunden
        self.timer = 0.0

    def update(self, dt: float, spiel: Spiel, res):
        if self.timer > 0:
            self.timer -= dt
        if self.timer > 0:
            return

        nahe_gegner = self.finde_nahe_gegner(spiel)

        if nahe_gegner:
            self.schiesse_auf(nahe_gegner[0], spiel, res)
            self.timer = self.angriff_cooldown

    def finde_nahe_gegner(self, spiel: Spiel):
        nahe_gegner = []
        for enemy in spiel.enemies:
            if not enemy.sprite.visible:
                continue
            if hasattr(enemy, 'aktiv') and not enemy.aktiv:
                continue

            enemy_grid_x = int(enemy.x / 100)
            enemy_grid_y = int(enemy.y / 100)

            dx = abs(self.index_x - enemy_grid_x)
            dy = abs(self.index_y - enemy_grid_y)

            if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                nahe_gegner.append(enemy)
        return nahe_gegner

    def schiesse_auf(self, enemy, spiel: Spiel, res):
        """Verschießt einen normalen Pfeil."""
        if hasattr(res, 'sounds5') and res.sounds5:
            res.sounds5.play() 

        turm_center_x = self.index_x * 100 + 50
        turm_center_y = self.index_y * 100 + 50

        from pfeil import Pfeil
        neuer_pfeil = Pfeil(turm_center_x, turm_center_y, enemy, spiel.batch, res)
        neuer_pfeil.schaden = self.schaden
        
        if not hasattr(spiel, 'pfeile'):
            spiel.pfeile = []
        spiel.pfeile.append(neuer_pfeil)

    def upgrade(self, neues_bild):
        #Turm 2 Upgraden
        self.schaden = 2              # Mehr Schaden für Turm 2
        self.angriff_cooldown = 3.0   # Schießt doppelt so schnell (alle 2 Sekunden)
        self.raster_feld.sprite.image = neues_bild


class GoldTurm(TurmLogik):
    def __init__(self, raster_feld: RasterFeld):
        super().__init__(raster_feld)
        self.schaden = 3
        self.angriff_cooldown = 5.0  # Schießt alle 2 Sekunden

    def schiesse_auf(self, enemy, spiel: Spiel, res):
        if hasattr(res, 'sounds5') and res.sounds5:
            res.sounds5.play() 

        turm_center_x = self.index_x * 100 + 50
        turm_center_y = self.index_y * 100 + 50

        from gold_pfeil import GoldPfeil
        neuer_pfeil = GoldPfeil(turm_center_x, turm_center_y, enemy, spiel.batch, res)
        neuer_pfeil.schaden = self.schaden
        
        if not hasattr(spiel, 'pfeile'):
            spiel.pfeile = []
        spiel.pfeile.append(neuer_pfeil)