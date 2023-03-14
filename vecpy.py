import math

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse


class PhysicalObject():
    def __init__(self, speed_x=0, speed_y=0, gravity=0.05, speed_gravity=0):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.speed_gravity = speed_gravity

    def contact(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_gravity = 0

    def touch(self, other) -> bool:
        pass


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
        if self.radius > math.sqrt((cx-self.x)**2+(cy-self.y)**2):
            return True
        return False

class Events:
    @self.vecpy.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        global inn
        if buttons & mouse.LEFT:
            if self.circle.bounds(x, y) or inn:
                circle.x += dx
                circle.y += dy
                circle.speed_gravity = 0
                circle.speed_x = dx
                circle.speed_y = -dy
                inn = True


    @self.vecpy.event
    def on_mouse_release(x, y, button, modifiers):
        global inn
        if button & mouse.LEFT:
            if inn:
                inn = False


    
class Feur(Sim, Events):
    def __init__(self, width, height):    
        self.width = width
        self.height = height
        # Création de la fenêtre
        self.vecpy = pyglet.window.Window(width, height)
        
    # Initiallizer SIM puis les EVENTS POUR CALL LES DECORATORS EVENTS AVEC SELF



class Sim:
    def __init__(self, width, height):

        
        super().__init__(Events)
        self.shapes = []
        self.drag_status = False
        self.init_render_objects()

        self.quadtree = QuadTree(0, 0, self.width, self.height)

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        pyglet.app.run()

    def init_render_objects(self):
        self.main_batch = pyglet.graphics.Batch()
        self.counter = pyglet.window.FPSDisplay(window=self.vecpy)
        self.label = pyglet.text.Label("", color=(122, 122, 122, 255),
                          font_size=36,
                          x=400, y=300,
                          anchor_x='center', anchor_y='center')
        self.ground = Rect(x=0, y=0, width=800, height=20, color=(93,23,222,89))
        self.circle = Circ(x=100, y=150, radius=100, color=(50, 225, 30))
        self.midcircle = Circ(x=100, y=150, radius=2, color=(245, 40, 145, 120))

        self.torender = [self.main_batch, self.counter, self.label, self.ground, self.circle, self.midcircle]

    @vecpy.event
    def on_draw():
        vecpy.clear()
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

class QuadTree:
    def __init__(self, x, y, width, height, capacity=4, level=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.level = level
        self.shapes = []
        self.children = None

    def subdivide(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width/2
        y2 = self.y + self.height/2
        x3 = self.x + self.width/2
        y3 = self.y
        x4 = self.x
        y4 = self.y + self.height/2
        self.children = [QuadTree(x1, y1, self.width/2, self.height/2, self.capacity, self.level+1),
                         QuadTree(x2, y2, self.width/2, self.height/2, self.capacity, self.level+1),
                         QuadTree(x3, y3, self.width/2, self.height/2, self.capacity, self.level+1),
                         QuadTree(x4, y4, self.width/2, self.height/2, self.capacity, self.level+1)]

    def insert(self, shape: PhysicalObject):
        if not self.contains(shape):
            return False

        if len(self.shapes) < self.capacity:
            self.shapes.append(shape)
            return True
        else:
            if self.children is None:
                self.subdivide()
            for child in self.children:
                if child.insert(shape):
                    return True
        return False

    def contains(self, shape: PhysicalObject):
        return shape.x >= self.x and shape.x + shape.width <= self.x + self.width \
               and shape.y >= self.y and shape.y + shape.height <= self.y + self.height

    def query(self, shape: PhysicalObject):
        results = []
        if not self.contains(shape):
            return results

        for s in self.shapes:
            if s is not shape:
                results.append(s)

        if self.children is not None:
            for child in self.children:
                results.extend(child.query(shape))
        return results



if __name__ == "__main__":
    fsim = Sim()
