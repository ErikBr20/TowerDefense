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
        raise AttributeError("f'NamedImages' object has no attribute '{name}'")


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
        "goldturm": "goldturm.png",
        "rittergeg1": "ritter_1.png",
        "rittergeg2": "ritter_2.png",
        "rittergeg3": "ritter_3.png",
        "rittergeg4": "ritter_4.png",
        "rittergeg5": "ritter_5.png", 
        "rittergeg6": "ritter_6.png",
        "rittergeg7": "ritter_7.png",
        "rittergeg8": "ritter_8.png",
        "rittergeg9": "ritter_9.png",
        "rittergeg10": "ritter_10.png",
        "ritter_def1": "ritterdef1.png",
        "ritter_def2": "ritterdef2.png",
        "ritter_def3": "ritterdef3.png",
        "ritter_def4": "ritterdef4.png",
        "ritter_def5": "ritterdef5.png",
        "ritter_def6": "ritterdef6.png",
        "ritter_def7": "ritterdef7.png",
        "ritter_def8": "ritterdef8.png",
        "ritter_def9": "ritterdef9.png",
        "ritter_def10": "ritterdef10.png"
}

    # Load each image dynamically
    for var_name, file_name in images_to_load.items():
        load_image(res, var_name, file_name)

    images = [res.images.rittergeg2,
          res.images.rittergeg1,
          res.images.rittergeg4,
          res.images.rittergeg10,
          res.images.rittergeg5,
          res.images.rittergeg9,
          res.images.rittergeg7,
          res.images.rittergeg6,
          res.images.rittergeg8
    ] 
    cloned_images = []
    for img in images:
        clone = img.get_region(0, 0, img.width, img.height)
        clone.anchor_x = clone.width // 2
        clone.anchor_y = clone.height // 2
        cloned_images.append(clone)
    rittergeg_ani = pyglet.image.Animation.from_image_sequence(cloned_images, duration=0.1, loop=True)
    res.images.add_image("rittergeg_ani", rittergeg_ani)

    

    for var_name, file_name in images_to_load.items():
        load_image(res, var_name, file_name)

    images = [res.images.ritter_def10,
          res.images.ritter_def7,
          res.images.ritter_def4,
          res.images.ritter_def9,
          res.images.ritter_def5,
          res.images.ritter_def6,
          res.images.ritter_def8,
          res.images.ritter_def9
    ]
    cloned_images = []
    for img in images:
        clone = img.get_region(0, 0, img.width, img.height)
        clone.anchor_x = clone.width // 2
        clone.anchor_y = clone.height // 2
        cloned_images.append(clone)
    ritterdef_ani = pyglet.image.Animation.from_image_sequence(cloned_images, duration=0.1, loop=True)
    res.images.add_image("ritterdef_ani", ritterdef_ani)

    return res