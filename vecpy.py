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
    #@self.vecpy.event
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            if self.circle.bounds(x, y) or self.drag_status:
                self.circle.x += dx
                self.circle.y += dy
                self.circle.speed_gravity = 0
                self.circle.speed_x = dx
                self.circle.speed_y = -dy
                self.drag_status = True


    #@self.vecpy.event
    def on_mouse_release(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.drag_status:
                self.drag_status = False


class Sim:
    def __init__(self):
        self.shapes = []
        self.drag_status = False
        self.init_render_objects()

        self.quadtree = QuadTree(0, 0, self.width, self.height)

        

    def init_render_objects(self):
        self.main_batch = pyglet.graphics.Batch()
        self.counter = pyglet.window.FPSDisplay(window=self)
        self.label = pyglet.text.Label("", color=(122, 122, 122, 255),
                          font_size=36,
                          x=400, y=300,
                          anchor_x='center', anchor_y='center')
        self.ground = Rect(x=0, y=0, width=800, height=20, color=(93,23,222,89))
        self.circle = Circ(x=100, y=150, radius=100, color=(50, 225, 30))
        self.midcircle = Circ(x=100, y=150, radius=2, color=(245, 40, 145, 120))

        self.torender = [self.main_batch, self.counter, self.label, self.ground, self.circle, self.midcircle]

    #@self.event
    def on_draw(self):
        self.clear()
        for _ in self.torender:
            _.draw()


    def update(self, dt):
        if not self.drag_status:
            self.circle.speed_gravity += self.circle.gravity * dt * 100
            self.circle.speed_y -= (self.circle.speed_y + self.circle.speed_gravity) * dt * 100
            self.circle.y += self.circle.speed_y
            self.circle.speed_x *= 0.999
            self.circle.x += self.circle.speed_x * dt * 100

        self.midcircle.x, self.midcircle.y = self.circle.x, self.circle.y
        self.label.text = f"x: {int(self.circle.x)} y:{int(self.circle.y)} dx:{int(self.circle.speed_x)} dy:{int(self.circle.speed_y)}"

    
class Wind(Sim, Events, pyglet.window.Window):
    def __init__(self, *args, **kwargs):    
        # Création de la fenêtre
        pyglet.window.Window.__init__(self, *args, **kwargs)
        Sim.__init__(self)
        Events.__init__(self)

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        pyglet.app.run()
        
    # Initiallizer SIM puis les EVENTS POUR CALL LES DECORATORS EVENTS AVEC SELF





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
    fsim = Wind(width=800, height=600)
