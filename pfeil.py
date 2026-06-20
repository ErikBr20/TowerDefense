import pyglet
import math

class Pfeil:
    def __init__(self, start_x, start_y, ziel_gegner, batch, res):
        self.x = start_x
        self.y = start_y
        self.ziel_gegner = ziel_gegner
        self.res = res
        
        # Pfeil-Bild laden (Falls kein pfeil.png existiert, nutzen wir ein Fallback)
        try:
            self.image = pyglet.resource.image('pfeil.png')
            self.image.anchor_x = self.image.width // 2
            self.image.anchor_y = self.image.height // 2
        except:
            # Fallback: Wenn kein Bild da ist, nehmen wir ein anderes kleines Bild aus deinen Ressourcen
            self.image = res.images.baum 
            
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y, batch=batch)
        self.sprite.scale = 0.08 # Pfeil etwas kleiner machen
        
        self.geschwindigkeit = 400.0 # Pixel pro Sekunde
        self.tot = False
        self.schaden = 1

    def update(self, dt, spiel):
        if self.tot:
            return

        # Prüfen, ob der Gegner in der Zwischenzeit schon gestorben ist
        if self.ziel_gegner not in spiel.enemies or not self.ziel_gegner.sprite.visible:
            self.zerstoeren()
            return

        # Vektor zum Gegner berechnen
        dx = self.ziel_gegner.x - self.x
        dy = self.ziel_gegner.y - self.y
        abstand = math.sqrt(dx * dx + dy * dy)

        # Wenn der Pfeil den Gegner fast erreicht hat (Abstand < 15 Pixel)
        if abstand < 15:
            self.treffer(spiel)
            return

        # Richtung normalisieren und fliegen
        if abstand > 0:
            self.x += (dx / abstand) * self.geschwindigkeit * dt
            self.y += (dy / abstand) * self.geschwindigkeit * dt
            
            # Sprite-Position aktualisieren
            self.sprite.x = self.x
            self.sprite.y = self.y
            
            # Pfeil in Flugrichtung rotieren (in Grad)
            winkel_rad = math.atan2(dy, dx)
            self.sprite.rotation = -math.degrees(winkel_rad)

    def treffer(self, spiel):
        if hasattr(self.res, 'sounds') and hasattr(self.res.sounds, 'einschlag'):
            self.res.sounds.einschlag.play()
        # Fallback: Dein bisheriger Sound2, falls der spezifische nicht existiert
        elif hasattr(self.res, 'sounds3') and self.res.sounds4:
            self.res.sounds4.play()
    
        # Sound abspielen
        if hasattr(self.res, 'sounds2') and self.res.sounds2:
            self.res.sounds2.play()

        # Schaden anwenden
        enemy = self.ziel_gegner
        if hasattr(enemy, 'ist_könig'):
            enemy.leben -= self.schaden
            spiel.könig_label.text = f"König: {enemy.leben}"
            if enemy.leben <= 0:
                if enemy in spiel.enemies:
                    if enemy.sprite._vertex_list is not None:
                        enemy.sprite.delete()
                    spiel.enemies.remove(enemy)
                    from spielfeld import mehr_muenzen
                    mehr_muenzen(spiel)
        else:
            if enemy in spiel.enemies:
                if enemy.sprite._vertex_list is not None:
                    enemy.sprite.delete()
                spiel.enemies.remove(enemy)
                from spielfeld import mehr_muenzen
                mehr_muenzen(spiel)

        self.zerstoeren()

    def zerstoeren(self):
        self.tot = True
        if self.sprite._vertex_list is not None:
            self.sprite.delete()