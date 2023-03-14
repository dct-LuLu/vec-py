import math

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse


class PhysicalObject():
    def __init__(self, movable, draggable, speed_x=0, speed_y=0, gravity=0.5, speed_gravity=0):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.speed_gravity = speed_gravity
        self.movable = movable
        self.draggable = draggable

    def contact(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_gravity = 0

    def touch(self, other) -> bool:
        pass


class Rect(PhysicalObject, shapes.Rectangle):
    def __init__(self, draggable=True, movable=True, *args, **kwargs):
        shapes.Rectangle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable)

    def bounds(self, cx, cy) -> bool:
        if (self.x <= cx <= self.x + self.width) and (self.y <= cy <= self.y + self.height):
            return True
        return False


class Circ(PhysicalObject, shapes.Circle):
    def __init__(self, draggable=True, movable=True, *args, **kwargs):
        shapes.Circle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable)

    def bounds(self, cx, cy) -> bool:
        if self.radius >= math.sqrt((cx-self.x)**2+(cy-self.y)**2):
            return True
        return False

class Events:
    def __init__(self):
        self.drag_object = None

    # EVENT
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            if self.drag_object is not None: # On peut potentiellement aussi calculer la distance entre le curseur et le point central de l'objet et le modifier en gardant cette distance
                self.drag_object.x += dx
                self.drag_object.y += dy
                self.drag_object.speed_x = dx
                self.drag_object.speed_y = dy

    # EVENT
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            for _ in self.shapes:
                if _.bounds(x, y) and _.draggable and self.drag_object is None:
                    self.drag_object = _
                    self.drag_object.speed_gravity = 0
                    self.drag_object.speed_x = 0
                    self.drag_object.speed_y = 0

    # EVENT
    def on_mouse_release(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            print(f"speed_x: {self.drag_object.speed_x}, speed_y: {self.drag_object.speed_y}")
            self.drag_object = None


class Sim:
    def __init__(self):
        self.init_render_objects()
        #Faire un truc qui choppe auto les draggable et movables
        self.shapes = [self.circle, self.midcircle, self.ground] # TODO: ne pas utiliser de liste et aller chercher directement dans les instances de PhysicalObject
        self.quadtree = QuadTree(0, 0, self.width, self.height) # TODO: setup la quadtree map

        

    def init_render_objects(self):
        self.main_batch = pyglet.graphics.Batch()
        self.counter = pyglet.window.FPSDisplay(window=self)
        self.label = pyglet.text.Label("", color=(122, 122, 122, 255),
                          font_size=36,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center')
        self.circle = Circ(x=self.width//2, y=850, radius=100, color=(50, 225, 30))
        self.midcircle = Circ(x=self.circle.x, y=self.circle.y, radius=2, color=(245, 40, 145, 120), draggable=False)
        self.ground = Rect(x=0, y=0, width=self.width, height=int(1/30*self.height), color=(93,23,222,89), movable=False, draggable=False)

        self.torender = [self.main_batch, self.counter, self.label, self.ground, self.circle, self.midcircle]

    # EVENT
    def on_draw(self):
        self.clear()
        for _ in self.torender:
            _.draw()


    def update(self, dt):
        for _ in self.shapes:
            if _.movable and _ != self.drag_object:
                _.speed_gravity += _.gravity * dt
                _.speed_y -= _.speed_gravity * dt
                _.y += _.speed_y * dt * 100

                _.speed_x *= 0.999
                _.x += _.speed_x * dt * 100



        self.midcircle.x, self.midcircle.y = self.circle.x, self.circle.y
        
        self.label.text = f"x: {int(self.circle.x)} y:{int(self.circle.y)} dx:{int(self.circle.speed_x)} dy:{int(self.circle.speed_y)}"

    
class Wind(Sim, Events, pyglet.window.Window):
    def __init__(self, *args, **kwargs):    
        # Création de la fenêtre
        pyglet.window.Window.__init__(self, *args, **kwargs) # la fenêtre c'est self ... lol.
        self.mousebuttons = mouse.MouseStateHandler()
        self.push_handlers(self.mousebuttons)
        Sim.__init__(self)
        Events.__init__(self)

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        pyglet.app.run()




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
    fsim = Wind(width=1920, height=1080) # 800 , 600
