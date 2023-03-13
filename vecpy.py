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

    def bounds(self, cx, cy) -> bool:
        if (self.x <= cx <= self.x + self.width) and (self.y <= cy <= self.y + self.height):
            return True
        return False

class Circ(PhysicalObject, shapes.Circle):
    def __init__(self, *args, **kwargs):
        shapes.Circle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self)

    def bounds(self, cx, cy) -> bool:
        if circle.radius > math.sqrt((cx-circle.x)**2+(cy-circle.y)**2):
            return True
        return False

f = Rect(x=0, y=0, width=800, height=20, color=(93,23,222,89))

circle = Circ(x=100, y=150, radius=100, color=(50, 225, 30))

midcircle = Circ(x=100, y=150, radius=2, color=(245, 40, 145, 120))

inn = False


def init():
    pass


def reset_plane():
    pass


@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global inn
    if buttons & mouse.LEFT:
        if circle.bounds(x, y) or inn:
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
    circle.draw()
    midcircle.draw()
    f.draw()


def update(dt):
    if not inn:
        circle.speed_gravity += circle.gravity * dt * 100
        circle.speed_y -= (circle.speed_y + circle.speed_gravity) * dt * 100
        circle.y += circle.speed_y
        circle.speed_x *= 0.999
        circle.x += circle.speed_x * dt * 100

    midcircle.x, midcircle.y = circle.x, circle.y
    label.text = f"x: {int(circle.x)} y:{int(circle.y)} dx:{int(circle.speed_x)} dy:{int(circle.speed_y)}"


if __name__ == "__main__":
    init()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
