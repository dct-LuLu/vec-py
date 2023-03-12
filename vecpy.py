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

class PhysicsObject:
    def __init__(self, obj: shapes):
        self.obj = obj
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.05
        self.speed_gravity = 0


circle = PhysicsObject(shapes.Circle(x=100, y=150, radius=100, color=(50, 225, 30)))

midcircle = shapes.Circle(x=100, y=150, radius=2, color=(245, 40, 145, 120))

inn = False


def init():
    pass


def reset_plane():
    pass


@game_window.event
def on_mouse_motion(x, y, dx, dy):
    label.text = f'x:{x} y:{y}'

    if circle.obj.radius > math.sqrt((x-circle.obj.x)**2+(y-circle.obj.y)**2):
        label.color = (255, 0, 255, 255)
    else:
        label.color = (122, 122, 122, 255)


@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global inn
    if buttons & mouse.LEFT:
        if circle.obj.radius > math.sqrt((x-circle.obj.x)**2+(y-circle.obj.y)**2) or inn:
            circle.obj.x += dx
            circle.obj.y += dy
            circle.speed_gravity = 0
            circle.speed_x = dx
            circle.speed_y = dy
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
        circle.obj.x += circle.speed_x
        circle.obj.y -= circle.speed_y + circle.speed_gravity

    circle.obj.draw()
    midcircle.x, midcircle.y = circle.obj.x, circle.obj.y
    midcircle.draw()


def update(dt):
    pass


if __name__ == "__main__":
    init()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
