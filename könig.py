import math
import pyglet
import random
from collections import deque
from spiel_lelements import SpielLandschaft

class König:
    def __init__(self, landschaft: SpielLandschaft, batch: pyglet.graphics.Batch, animation, sounds3, sounds7, warte_zeit: float = 0.0):
        self.leben = 20
        self.aktiv = False
        self.schaden_timer = 0.0
        self.sound = sounds3
        self.sound2 = sounds7
        self.ist_könig = True

        # Weg berechnen
        self.path = self._extrahiere_weg(landschaft)

        # Zufälligen Startpunkt auf dem Weg wählen
        start_index = random.randint(0, len(self.path) - 2)
        self.x = float(self.path[start_index][0])
        self.y = float(self.path[start_index][1])
        self.path_index = start_index + 1

        self.speed = 150
        self.reached_end = False
        self.warte_zeit = warte_zeit

        self.fixed_width = max(f.image.width for f in animation.frames)

        self.sprite = pyglet.sprite.Sprite(
            animation,
            x=self.x,
            y=self.y,
            batch=batch,
            group=pyglet.graphics.Group(order=1),
            subpixel=True,
        )
        self.sprite.scale = 100 / self.fixed_width
        self.sprite.visible = False

        dx = self.path[self.path_index][0] - self.x
        dy = self.path[self.path_index][1] - self.y
        self._aktualisiere_drehung(dx, dy)

    def _extrahiere_weg(self, landschaft: SpielLandschaft):
        TILE = 100

        weg_dict = {}
        for zeile in landschaft.zeilen:
            for feld in zeile.spalten:
                if feld.landschaftstyp.name == "Weg":
                    weg_dict[(feld.index_x, feld.index_y)] = feld

        start_felder = [f for f in weg_dict.values() if f.index_x == 0]
        start = start_felder[0]
        for f in start_felder:
            nachbarn = sum([
                (f.index_x + 1, f.index_y) in weg_dict,
                (f.index_x, f.index_y + 1) in weg_dict,
                (f.index_x, f.index_y - 1) in weg_dict,
            ])
            if nachbarn == 1:
                start = f
                break

        queue = deque()
        queue.append([(start.index_x, start.index_y)])
        besucht = {(start.index_x, start.index_y)}
        bester_pfad = [(start.index_x, start.index_y)]

        while queue:
            pfad = queue.popleft()
            aktuell = pfad[-1]

            if aktuell[0] > bester_pfad[-1][0]:
                bester_pfad = pfad

            for dx, dy in [(1, 0), (0, 1), (0, -1)]:
                nachbar = (aktuell[0] + dx, aktuell[1] + dy)
                if nachbar in weg_dict and nachbar not in besucht:
                    besucht.add(nachbar)
                    queue.append(pfad + [nachbar])

        return [
            (x * TILE + TILE // 2, y * TILE + TILE // 2)
            for (x, y) in bester_pfad
        ]

    def _aktualisiere_drehung(self, dx: float, dy: float):
        if abs(dx) > abs(dy):
            self.sprite.rotation = 270 if dx > 0 else 90
        else:
            self.sprite.rotation = 180 if dy > 0 else 0

    def update(self, dt: float, spiel=None):
        # Wartezeit herunterzählen
        if self.warte_zeit > 0:
            self.warte_zeit -= dt
            return
    
        # Sichtbar machen
        if not self.sprite.visible:
            self.sprite.visible = True
            self.aktiv = True
            self.sound2.volume = 1
            self.sound.play()
            self.sound2.play()

        # Ende des Weges erreicht, stehen bleiben aber nicht despawnen
        if self.path_index >= len(self.path):
            self.reached_end = True
            self.sprite.x = self.x
            self.sprite.y = self.y
            return

        # Nächsten Wegpunkt ansteuern
        ziel_x, ziel_y = self.path[self.path_index]
        dx = ziel_x - self.x
        dy = ziel_y - self.y
        distanz = math.sqrt(dx * dx + dy * dy)
        schritt = self.speed * dt

        if distanz <= schritt:
            self.x = float(ziel_x)
            self.y = float(ziel_y)
            self.path_index += 1
        else:
            self.x += (dx / distanz) * schritt
            self.y += (dy / distanz) * schritt

        self._aktualisiere_drehung(dx, dy)
        self.sprite.x = self.x
        self.sprite.y = self.y

    def entfernen(self):
        self.sprite.delete()

    def entfernen(self):
        self.sprite.delete()