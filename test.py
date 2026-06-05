import pyglet
from basic_elements import *
from menu import *
from spielfeld import *

game_window = pyglet.window.Window(1920, 1080, fullscreen=True)



res = load_static_ressources()
spielBatch = pyglet.graphics.Batch()
sprite = make_image_sprite(0,0,300,300, res.images.rittergeg2, spielBatch)

ani_sprite = make_image_sprite(300, 300, 500, 500, res.images.rittergeg_ani, spielBatch)
ani2_sprite = make_image_sprite(700, 300, 500, 500, res.images.ritterdef_ani, spielBatch)
ani3_sprite = make_image_sprite(1100, 300, 500, 500, res.images.könig_ani, spielBatch)

def rittergeg_nach_links(x):
    ani_sprite.x -= x

def rittergeg_nach_oben(x):
    ani_sprite.y += x

def rittergeg_nach_rechts(x):
    ani2_sprite.x += x

def rittergeg_nach_unten(x):
    ani_sprite.y += x

def ritterdef_nach_links(x):
    ani2_sprite.x -= x

def ritterdef_nach_oben(x):
    ani2_sprite.y += x

def ritterdef_nach_rechts(x):
    ani2_sprite.x += x

def ritterdef_nach_unten(x):
    ani2_sprite.y += x

def ritterdef_drehen_rechts(x):
     ani2_sprite.rotation = x


def ritterdef_drehen_links(x):
     ani2_sprite.rotation = -x


def rittergeg_drehen_rechts(x):
     ani_sprite.rotation = x


def rittergeg_drehen_rechts(x):
     ani_sprite.rotation = -x

     






@game_window.event
def on_draw():
    ritterdef_nach_rechts(5)
    rittergeg_drehen_rechts(90)
    game_window.clear()
    spielBatch.draw()

if __name__ == "__main__":
    pyglet.app.run()    



