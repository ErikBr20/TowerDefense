from dataclasses import dataclass, field
from typing import List
import pyglet

@dataclass
class Landschaftstyp:
    name: str = None
    is_random: bool = False
    image: pyglet.image.Texture | pyglet.image.TextureRegion = None

@dataclass
class Spieler:
    name: str = "Spieler"
    muenzen: int = 0
    muenzen_label: pyglet.text.Label = None

@dataclass
class RasterFeld:
    landschaftstyp: Landschaftstyp = None
    sprite: pyglet.sprite.Sprite = None
    index_x: int = None
    index_y: int = None

@dataclass
class SpielZeile:
    spalten: List[RasterFeld] = field(default_factory=list)

@dataclass
class SpielLandschaft:
    anzahl_zeilen: int = None
    anzahl_spalten: int = None
    zeilen: List[SpielZeile] = field(default_factory=list)

@dataclass
class Spiel:
    spieler: Spieler = None
    landschaft: SpielLandschaft = None
    landschaftstypen: List[Landschaftstyp] = field(default_factory=list)
    batch: pyglet.graphics.Batch = None
    turm_label: pyglet.text.Label = None
    könig_label: pyglet.text.Label = None
