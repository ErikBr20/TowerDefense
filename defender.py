import math
import pyglet
from collections import deque
from spiel_lelements import SpielLandschaft

class Defender:
    def __init__(self, landschaft: SpielLandschaft, batch: pyglet.graphics.Batch, animation, warte_zeit: float = 0.0):
        # Wo soll der Verteidiger laufen?
        self.path = self._extrahiere_weg(landschaft)
        self.angriff_timer = 0.0
        
        # Verteidiger fängt beim letzten Wegpunkt an (Ziel), läuft richtung vorletzten wegpunkt(path_index)
        self.path_index = len(self.path) - 2 
        self.x = float(self.path[-1][0])
        self.y = float(self.path[-1][1])
        
        # Geschwindigkeit in Pixel pro Sekunde
        self.speed = 140
        
        # True wenn der Verteidiger den Start erreicht hat
        self.reached_end = False
        
        # Wartezeit bevor der Verteidiger losläuft
        self.warte_zeit = warte_zeit

        # Grösste Framebreite nehmen damit der Scale nie wechselt
        self.fixed_width = max(f.image.width for f in animation.frames)
        
        # Verteidiger erstellen
        self.sprite = pyglet.sprite.Sprite(animation, x=self.x, y=self.y, batch=batch, group=pyglet.graphics.Group(order=1), subpixel=True)
        
        # Scale einmal setzen
        self.sprite.scale = 60 / self.fixed_width
        
        # Unsichtbar bis Wartezeit abgelaufen
        self.sprite.visible = False

        # Startausrichtung bestimmen basierend auf erstem Schritt
        if len(self.path) > 1:
            dx = self.path[-2][0] - self.path[-1][0]
            dy = self.path[-2][1] - self.path[-1][1]
            self._aktualisiere_drehung(dx, dy)

    def _extrahiere_weg(self, landschaft: SpielLandschaft):
        # Ein Feld ist 100 Pixel gross
        TILE = 100
        
        # Alle Wegfelder sammeln
        weg_dict = {}
        for zeile in landschaft.zeilen:
            for feld in zeile.spalten:
                if feld.landschaftstyp.name == "Weg":
                    weg_dict[(feld.index_x, feld.index_y)] = feld
        
        # Startfeld: Feld in Spalte 0 mit genau 1 Wegfeld-Nachbarn
        start_felder = [f for f in weg_dict.values() if f.index_x == 0]
        start = start_felder[0]
        for f in start_felder:
            nachbarn = 0
            if (f.index_x + 1, f.index_y) in weg_dict: nachbarn += 1
            if (f.index_x, f.index_y + 1) in weg_dict: nachbarn += 1
            if (f.index_x, f.index_y - 1) in weg_dict: nachbarn += 1
            # Genau 1 Nachbar = echter Startpunkt
            if nachbarn == 1:
                start = f
                break
        
        # Weg von links nach rechts suchen
        queue = deque()
        queue.append([(start.index_x, start.index_y)])
        besucht = {(start.index_x, start.index_y)}
        bester_pfad = [(start.index_x, start.index_y)]

        while queue:
            pfad = queue.popleft()
            aktuell = pfad[-1]
            
            # Weiter rechts = besserer Pfad
            if aktuell[0] > bester_pfad[-1][0]:
                bester_pfad = pfad
            
            # Nachbarn rechts, oben und unten prüfen
            for dx, dy in [(1, 0), (0, 1), (0, -1)]:
                nachbar = (aktuell[0] + dx, aktuell[1] + dy)
                if nachbar in weg_dict and nachbar not in besucht:
                    besucht.add(nachbar)
                    queue.append(pfad + [nachbar])
        
        return [
            (
                x * TILE + TILE // 2,
                y * TILE + TILE // 2
            )
            for (x, y) in bester_pfad
        ]

    def _aktualisiere_drehung(self, dx: float, dy: float):
        # Verteidiger dreht sich je nach Richtung in die er läuft
        if abs(dx) > abs(dy):
            if dx > 0:
                self.sprite.rotation = 270  # rechts
            else:
                self.sprite.rotation = 90   # links
        else:
            if dy > 0:
                self.sprite.rotation = 180  # oben
            else:
                self.sprite.rotation = 0    # unten

    def update(self, dt: float):
        # Angriff Timer immer runterzählen
        if self.angriff_timer > 0:
            self.angriff_timer -= dt

        # Warten bis die Wartezeit abgelaufen ist
        if self.warte_zeit > 0:
            self.warte_zeit -= dt
            return
        
        # Sichtbar machen wenn Wartezeit abgelaufen
        if not self.sprite.visible:
            self.sprite.visible = True

        # Nichts tun wenn Start erreicht
        if self.reached_end or self.path_index < 0:
            self.reached_end = True
            return

        # Nächsten Wegpunkt holen (rückwärts)
        ziel_x, ziel_y = self.path[self.path_index]

        # Richtung und Distanz berechnen
        dx = ziel_x - self.x
        dy = ziel_y - self.y
        distanz = math.sqrt(dx * dx + dy * dy)

        # Schrittweite für diesen Frame
        schritt = self.speed * dt

        if distanz <= schritt:
            self.x, self.y = float(ziel_x), float(ziel_y)
            self.path_index -= 1
        else:
            self.x += (dx / distanz) * schritt
            self.y += (dy / distanz) * schritt

        self._aktualisiere_drehung(dx, dy)
        self.sprite.x = self.x
        self.sprite.y = self.y