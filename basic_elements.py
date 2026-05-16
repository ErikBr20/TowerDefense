import pyglet

from dataclasses import dataclass, field
from typing import Callable, Union, Dict, Optional

@dataclass
class NamedImages:
    images: Dict[str, pyglet.image.AbstractImage] = field(default_factory=dict)

    def add_image(self, name: str, image: pyglet.image.AbstractImage):
        self.images[name] = image

    def get_image(self, name: str) -> Optional[pyglet.image.AbstractImage]:
        return self.images.get(name, None)

    def __getattr__(self, name: str) -> Optional[pyglet.image.AbstractImage]:
        """Allow dynamic attribute-style access to images."""
        if name in self.images:
            return self.images[name]
        raise AttributeError(f"'NamedImages' object has no attribute '{name}'")


@dataclass
class Ressources:
    images: NamedImages = field(default_factory=NamedImages)

def make_label_button(x: int, y: int, w: int, h: int, text: str, image: pyglet.image.Texture | pyglet.image.TextureRegion, push_handler: Callable[[], None], frame: pyglet.gui.Frame, batch: pyglet.graphics.Batch) -> Union[pyglet.text.Label, pyglet.gui.PushButton]:
    image.width = w
    image.height = h
    push_button = pyglet.gui.PushButton(x, y, pressed=image, unpressed=image, batch=batch)
    push_button.set_handler('on_press', push_handler)
    label = pyglet.text.Label(text=text, x = x + (w * 0.23), y = y + (h * 0.24), batch=batch)
    frame.add_widget(push_button)
    return [label, push_button]

def make_image_button(x: int, y: int, w: int, h: int, image: pyglet.image.Texture | pyglet.image.TextureRegion, push_handler: Callable[[], None], batch: pyglet.graphics.Batch) -> pyglet.gui.PushButton:
    image.width = w
    image.height = h
    push_button = pyglet.gui.PushButton(x, y, pressed=image, unpressed=image, batch=batch)
    push_button.set_handler('on_press', push_handler)
    return push_button

def make_image_sprite(x: int, y: int, w: int, h: int, image: pyglet.image.Texture | pyglet.image.TextureRegion, batch: pyglet.graphics.Batch):
    image.width = w
    image.height = h
    return pyglet.sprite.Sprite(image, x, y, batch=batch)

def make_text_label(x, y, text, batch) -> pyglet.text.Label:
    return pyglet.text.Label(text=text, x=x, y=y, batch=batch)

def make_rectangle(x: int, y: int, w: int, h: int, color: (tuple[int, int, int, int] | tuple[int, int, int]), batch: pyglet.graphics.Batch) -> pyglet.shapes.Rectangle:
    return pyglet.shapes.Rectangle(x, y, width=w, height=h, color=color, batch=batch)

def make_box(x: int, y: int, w: int, h: int, thickness: int, color: (tuple[int, int, int, int] | tuple[int, int, int]), batch: pyglet.graphics.Batch) -> pyglet.shapes.Box:
    return pyglet.shapes.Box(x, y, width=w, height=h, thickness=thickness, color=color, batch=batch)

def make_circle(x: int, y: int, r: int, color: (tuple[int, int, int, int] | tuple[int, int, int]), batch: pyglet.graphics.Batch) -> pyglet.shapes.Circle:
    return pyglet.shapes.Circle(x=x, y=y, radius=r, color=color, batch=batch)

def load_image(res: Ressources, var_name: str, file_name: str):
    try:
        image = pyglet.resource.image(file_name)
        res.images.add_image(var_name, image)
    except pyglet.resource.ResourceNotFoundException:
        print(f"Error: File '{file_name}' not found for variable '{var_name}'.")

def load_static_ressources():
    pyglet.resource.path = ['./artwork']
    pyglet.resource.reindex()
    res = Ressources()

    images_to_load = {
        "button_frame": "button_frame.png",
        "baum": "baum.png",
        "erde": "erde.png",
        "gras": "gras.png",
        "schuetze": "schuetze.png",
        "turm": "turm.png",
        "weg": "weg.png",
        "goldturm": "goldturm.png"
    }

    # Load each image dynamically
    for var_name, file_name in images_to_load.items():
        load_image(res, var_name, file_name)
    return res