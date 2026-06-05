import pyglet
from basic_elements import *
from menu import *
from spielfeld import *

game_window = pyglet.window.Window(1920, 1080, fullscreen=True)


menu: Menu = make_menu('Spielmenu', game_window)

def exit_handler(widget=None):
    pyglet.app.exit()


#Hauptmenu

#Spielfeld

#Spieler

end_press = False

res = load_static_ressources()
spiel: Spiel = None
#game Starten
def start_game(widget=None):
    global menu
    global spiel
    menu = None
    spiel = initialisiere_spiel(16, 11, res, False)

#Menu machen
add_menu_item(menu, 'Starte Spiel', res.images.button_frame, start_game)

add_menu_item(menu, 'Exit', res.images.button_frame, exit_handler)

#mouse drücken
@game_window.event
def on_mouse_press(x, y, button, modifiers):
    global end_press
    if end_press:
        pyglet.app.exit()
    if menu:
        menu.frame.on_mouse_press(x,y, button, modifiers)
    elif spiel and spiel.popup_active:
        spiel.popup_active = False
        for el in spiel.popup_elements:
            try:
                el.delete()
            except Exception:
                pass
        spiel.popup_elements = []
        spiel.ereignisse_runde = []
        update_spiel_info(spiel)
    elif spiel:
        spielende = press_spiel(spiel, x, y, game_window)
        if spielende:
            end_press = True
    return True
#menu zeichnen
@game_window.event
def on_draw():
    game_window.clear()
    draw_menu(menu)
    draw_spiel(spiel)

if __name__ == "__main__":
    pyglet.app.run()    
