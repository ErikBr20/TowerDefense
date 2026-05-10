import pyglet

from dataclasses import dataclass, field
from typing import Callable, List, Union

from basic_elements import make_rectangle, make_label_button, make_text_label

@dataclass
class MenuItem:
    text: str = None
    handler: Callable[[], None] = None
    labelButton: Union[pyglet.text.Label, pyglet.gui.PushButton] = None


@dataclass
class Menu:
    title: pyglet.text.Label = None
    items: List[MenuItem] = field(default_factory=list)
    rect: pyglet.shapes.Rectangle = None
    frame: pyglet.gui.frame = None
    batch: pyglet.graphics.Batch = None

def make_menu(title: str, window: pyglet.window) -> Menu:
    menu = Menu()
    menu.batch = pyglet.graphics.Batch()
    menu.title = make_text_label(window.width/2 - 100, window.height/2 + 100, title, menu.batch)
    menu.rect = make_rectangle(window.width/2 - 100 - 20, window.height/2 + 100 + 20, 300, -350,  color=(50, 50, 50), batch= menu.batch)
    menu.frame = pyglet.gui.Frame(window, order=4)
    return menu

def add_menu_item(menu: Menu, text: str, image: pyglet.image.Texture | pyglet.image.TextureRegion, handler: Callable[[], None]) -> MenuItem:
    item = MenuItem()
    item.text = text
    item.handler = handler
    item.labelButton = make_label_button(menu.rect.x + 10, menu.rect.y - len(menu.items)*60 - 70, 280, 30, text=text, image=image, push_handler=handler, frame=menu.frame, batch=menu.batch)
    menu.items.append(item)
    return item

def draw_menu(menu: Menu):
    if menu:
        menu.batch.draw()