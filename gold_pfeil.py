import pyglet
import math
from pfeil import Pfeil  # Wir erben vom normalen Pfeil

class GoldPfeil(Pfeil):
    def __init__(self, start_x, start_y, ziel_gegner, batch, res):
        # Ruft zuerst den normalen Pfeil auf
        super().__init__(start_x, start_y, ziel_gegner, batch, res)
        
        # Jetzt überschreiben wir das Bild mit dem goldenen Pfeil
        try:
            self.image = pyglet.resource.image('gold_pfeil.png') # Dein goldenes Pfeilbild
            self.image.anchor_x = self.image.width // 2
            self.image.anchor_y = self.image.height // 2
            self.sprite.image = self.image
        except Exception as e:
            print("Goldener Pfeil Bild nicht gefunden, benutze Standardgrafik:", e)
        self.geschwindigkeit = 600.0  # Fliegt schneller als der normale Pfeil