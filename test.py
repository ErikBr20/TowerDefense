import pyglet
from basic_elements import *
from menu import *
from spielfeld import *

game_window = pyglet.window.Window(1920, 1080, fullscreen=True)
game_window.clear()


res = load_static_ressources()
spielBatch = pyglet.graphics.Batch()
sprite = make_image_sprite(0,0,300,300, res.images.rittergeg2, spielBatch)

ani_sprite = make_image_sprite(300, 300, 300, 300, res.images.rittergeg_ani, spielBatch)


@game_window.event
def on_draw():
    spielBatch.draw()

if __name__ == "__main__":
    pyglet.app.run()    
