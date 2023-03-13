import math

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse

# Création de la fenêtre
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

counter = pyglet.window.FPSDisplay(window=game_window)

label = pyglet.text.Label("", color=(122, 122, 122, 255),
                          font_size=36,
                          x=400, y=300,
                          anchor_x='center', anchor_y='center')


class PhysicalObject():
    def __init__(self):
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.05
        self.speed_gravity = 0

    def contact(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_gravity = 0

class Rect(PhysicalObject, shapes.Rectangle):
    def __init__(self, *args, **kwargs):
        shapes.Rectangle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self)

class Circ(PhysicalObject, shapes.Circle):
    def __init__(self, *args, **kwargs):
        shapes.Circle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self)

f = Rect(x=100, y=150, width=100, height=200, color=(93,23,222,89))

circle = Circ(x=100, y=150, radius=100, color=(50, 225, 30))

midcircle = Circ(x=100, y=150, radius=2, color=(245, 40, 145, 120))

inn = False


def init():
    pass


def reset_plane():
    pass


@game_window.event
def on_mouse_motion(x, y, dx, dy):
    label.text = f'x:{x} y:{y}'

    if circle.radius > math.sqrt((x-circle.x)**2+(y-circle.y)**2):
        label.color = (255, 0, 255, 255)
    else:
        label.color = (122, 122, 122, 255)


@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global inn
    if buttons & mouse.LEFT:
        if circle.radius > math.sqrt((x-circle.x)**2+(y-circle.y)**2) or inn:
            circle.x += dx
            circle.y += dy
            circle.speed_gravity = 0
            circle.speed_x = dx
            circle.speed_y = -dy
            inn = True


@game_window.event
def on_mouse_release(x, y, button, modifiers):
    global inn
    if button & mouse.LEFT:
        if inn:
            inn = False


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()
    counter.draw()
    label.draw()
    if not inn:
        circle.speed_gravity += circle.gravity
        circle.x += circle.speed_x
        circle.y -= circle.speed_y + circle.speed_gravity

    circle.draw()
    midcircle.x, midcircle.y = circle.x, circle.y
    midcircle.draw()


def update(dt):
    pass


if __name__ == "__main__":
    init()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
