import math
from random import randint

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse
import numpy as np


class PhysicalObject():
    def __init__(self, movable, draggable, velocity=[0, 0], acceleration=[0, 0]):
        self.velocity = velocity
        self.acceleration = acceleration
        self.movable = movable
        self.draggable = draggable

    def get_tag(self) -> str:
        return f"{self.__class__.__name__} x: {int(self.x)} y:{int(self.y)} col:{self.color[0], self.color[1], self.color[2]}"

    def colision(obj1, obj2, dt):
        #print(f"BEFORE1: {obj1.velocity}\nBEFORE2: {obj2.velocity}\n")
        obj1.velocity = np.array(obj1.velocity)
        obj2.velocity = np.array(obj2.velocity)

        coord1 = np.array([obj1.x, obj1.y])
        coord2 = np.array([obj2.x, obj2.y])

        r = math.sqrt(sum((coord1-coord2)**2))
        n = (coord2-coord1)/r
        t = np.array(-n[1], n[0])

        v1n = np.dot(obj1.velocity, n)
        v1t = np.dot(obj1.velocity, t)
        v2n = np.dot(obj2.velocity, n)
        v2t = np.dot(obj2.velocity, t)

        u1n = (v1n * (obj1.mass-obj2.mass) + 2 * obj2.mass * v2n) / (obj1.mass+obj2.mass)
        u2n = (v2n * (obj2.mass-obj1.mass) + 2 * obj1.mass * v1n) / (obj1.mass+obj2.mass)

        u1t = v1t
        u2t = v2t

        obj1.velocity = (u1n * n + u1t * t) * dt
        obj2.velocity = (u2n * n + u2t * t) * dt

        #print(f"AFTER1: {obj1.velocity}\nAFTER2: {obj2.velocity}\n")


class Rect(PhysicalObject, shapes.Rectangle):
    def __init__(self, draggable=True, movable=True, velocity=[0, 0], acceleration=[0, 0], density=7850, *args, **kwargs):
        shapes.Rectangle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable, velocity, acceleration)
        self.density = density
        self.mass = self.width * self.height * self.density

    def bounds(self, cx, cy) -> bool:
        return (self.x <= cx <= self.x + self.width) and (self.y <= cy <= self.y + self.height)

class Circ(PhysicalObject, shapes.Circle):
    def __init__(self, draggable=True, movable=True, velocity=[0, 0], acceleration=[0, 0], density=7850 , *args, **kwargs):
        shapes.Circle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable, velocity, acceleration)
        self.density = density
        self.mass = math.pi * self.radius * self.density

    def bounds(self, cx, cy) -> bool:
        return self.radius >= math.sqrt((cx-self.x)**2+(cy-self.y)**2)

class Events:
    def __init__(self):
        self.drag_object = None

    # FIRST HIT
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            for _ in self.shapes:
                if _.bounds(x, y) and _.draggable and self.drag_object is None:
                    self.drag_object = _
                    self.target = self.drag_object
                    #self.drag_object.speed_gravity = 0
                    self.drag_object.velocity = [0, 0]

    # WHILE
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            if self.drag_object is not None: # On peut potentiellement aussi calculer la distance entre le curseur et le point central de l'objet et le modifier en gardant cette distance
                self.drag_object.x += dx
                self.drag_object.y += dy
                #self.drag_object.speed_x = dx
                #self.drag_object.speed_y = dy
                self.drag_object.velocity = [dx, dy]

    # AFTER
    def on_mouse_release(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.drag_object is not None:
                #print(f"speed_x: {self.drag_object.speed_x}, speed_y: {self.drag_object.speed_y}")
                self.drag_object = None


class Sim:
    def __init__(self):
        self.init_render_objects()
        #Faire un truc qui choppe auto les draggable et movables
        self.shapes = [self.circle, self.ground] + self.radoms # TODO: ne pas utiliser de liste et aller chercher directement dans les instances de PhysicalObject
        #self.quadtree = QuadTree(0, 0, self.width, self.height, self.shapes) # TODO: setup la quadtree map
        #self.quadtree.check()
        #self.not_shapes = self.quadtree.render_quadtree()

    def init_render_objects(self):
        self.main_batch = pyglet.graphics.Batch()
        self.counter = pyglet.window.FPSDisplay(window=self)
        self.label = pyglet.text.Label("", color=(122, 122, 122, 255),
                          font_size=36,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center')

        self.circle = Circ(x=self.width//2, y=self.height//2, radius=100, color=(50, 225, 30))

        self.ground = Rect(x=0, y=0, width=self.width, height=int(1/30*self.height), color=(93,23,222,89), movable=False, draggable=False)

        self.radoms = [Circ(x=randint(100, self.width-100),y=randint(100, self.height-100),radius=randint(10,60),color=(randint(0,255), randint(0,255), randint(0,255), 255),velocity=[randint(-5,5), randint(-5,5)]),
                       Circ(x=randint(100, self.width-200),y=randint(100, self.height-200),radius=randint(10,60),color=(randint(0,255), randint(0,255), randint(0,255), 255),velocity=[randint(-5,5), randint(-5,5)])]

        self.torender = [self.main_batch, self.counter, self.label, self.ground, self.circle] + self.radoms
        self.target = self.circle

    # EVENT
    def on_draw(self):
        self.clear()
        for _ in self.torender:
            _.draw()

        #self.not_shapes = self.quadtree.render_quadtree()
        #for _ in self.not_shapes:
        #    _.draw()


    def update(self, dt):
        dt *= 100
        #self.quadtree.check()
        #print(math.sqrt((self.radoms[0].x-self.radoms[1].x)**2 + (self.radoms[0].y-self.radoms[1].y)**2) - (self.radoms[0].radius + self.radoms[1].radius+5))
        for shape in self.shapes:
            if shape.movable and shape != self.drag_object:

                shape.velocity[0] += shape.acceleration[0] * dt
                shape.velocity[1] += shape.acceleration[1] * dt

                if shape.x + shape.radius >= self.width:
                    #print("droite")
                    shape.velocity[0] = -shape.velocity[0]
                    shape.x = self.width - shape.radius - 1

                if shape.x - shape.radius <= 0:
                    #print("gauche")

                    shape.velocity[0] = -shape.velocity[0]
                    shape.x = shape.radius + 1

                if shape.y + shape.radius >= self.height:
                    #print("haut")
                    shape.velocity[1] = -shape.velocity[1]
                    shape.y = self.height - shape.radius - 1

                if shape.y - shape.radius <= 0:
                    #print("bas")
                    shape.velocity[1] = -shape.velocity[1]
                    shape.y = shape.radius + 1
 
                shape.x += shape.velocity[0] * dt
                shape.y += shape.velocity[1] * dt
        
        self.label.text = f"nb: {len(self.shapes)} x: {int(self.target.x)} y:{int(self.target.y)} dx:{int(self.target.velocity[0])} dy:{int(self.target.velocity[1])}"

        if (int(math.sqrt((self.radoms[0].x-self.radoms[1].x)**2 + (self.radoms[0].y-self.radoms[1].y)**2)) <= (self.radoms[0].radius + self.radoms[1].radius+5)) :
            self.label.color = (255,255,100, 255)
            PhysicalObject.colision(self.radoms[0], self.radoms[1], dt)
        else:
            self.label.color = (122, 122, 122, 255)

    
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
    __MAX_OBJECTS = 2
    __MAX_LEVELS = 10
    
    def __init__(self, x, y, width, height, shapes=[], level=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.shapes = shapes
        self.children = [None] * 4
    
    def check(self):
        sub_QuadTree = [[]] * 4
        half_width, half_height = self.width/2, self.height/2
        x1, y1 = self.x, self.y
        x2, y2 = self.x + half_width, self.y + half_height
        x3, y3 = self.x + self.width, self.y + self.height

        for shape in self.shapes:
            if (x1 <= shape.x <= x2) and (y1 <= shape.y <= y2):
                sub_QuadTree[0].append(shape)
            elif (x2 <= shape.x <= x3) and (y1 <= shape.y <= y2):
                sub_QuadTree[1].append(shape)
            elif (x1 <= shape.x <= x2) and (y2 <= shape.y <= y3):
                sub_QuadTree[2].append(shape)
            elif (x2 <= shape.x <= x3) and (y2 <= shape.y <= y3):
                sub_QuadTree[3].append(shape)


        for i, sub_shapes in enumerate(sub_QuadTree):
            if len(sub_shapes) >= self.__MAX_OBJECTS and self.level < self.__MAX_LEVELS:
                self.children[i] = QuadTree(*self.get_sub_quadtree_coords(i), sub_shapes, self.level+1)
                self.children[i].check()
            else:
                self.children[i] = None

    def render_quadtree(self):
        sub = []
        for child in self.children:
            if child is not None:
                sub.append(Rect(x=child.x, y=child.y, width=child.width, height=child.height, color=(5*self.level,222,102, 10*self.level)))
                sub += child.render_quadtree()
        return sub
    
    def get_sub_quadtree_coords(self, index):
        half_width, half_height = self.width/2, self.height/2
        x1, y1 = self.x, self.y
        x2, y2 = self.x + half_width, self.y + half_height
        if index == 0:
            return x1, y1, half_width, half_height
        elif index == 1:
            return x2, y1, half_width, half_height
        elif index == 2:
            return x1, y2, half_width, half_height
        elif index == 3:
            return x2, y2, half_width, half_height

if __name__ == "__main__":
    fsim = Wind(width=800, height=600) # 800 , 600

# Mettez en cache les nœuds: Lorsque vous construisez le Quadtree, stockez les nœuds créés dans une liste ou un dictionnaire.
# Lorsque vous mettez à jour le Quadtree, utilisez les nœuds précédemment créés plutôt que de les recréer à chaque fois.

# Utilisez des méthodes d'insertion et de suppression: Si vous devez insérer ou supprimer des objets du Quadtree à chaque update,
# créez des méthodes spécifiques pour effectuer ces opérations plutôt que de reconstruire l'arbre à chaque fois. Cela permettra de minimiser le nombre de nœuds à créer ou à supprimer.

# Utilisez un système de marquage: Plutôt que de supprimer des objets du Quadtree lorsqu'ils ne sont plus nécessaires, marquez-les comme étant supprimés.
# Lors de la reconstruction du Quadtree, ignorez les objets marqués pour améliorer les performances.

# Évitez les subdivisions inutiles: Si les objets dans votre Quadtree ne se déplacent pas beaucoup, vous pouvez limiter le nombre de subdivisions en vérifiant si un nœud a suffisamment d'objets avant de le diviser.
# De même, si un nœud n'a plus d'objets, vous pouvez fusionner ses enfants.

# Utilisez un pool d'objets: Si vous avez besoin de créer ou de supprimer de nombreux objets à chaque update, utilisez un pool d'objets pour éviter de créer et de supprimer des objets à chaque fois.
# Au lieu de cela, vous pouvez simplement réutiliser des objets existants à partir du pool.

#En général, l'objectif est de minimiser le nombre d'opérations coûteuses à chaque update. En utilisant ces techniques, vous pouvez améliorer les performances de votre Quadtree et le rendre plus adapté
# à la gestion d'un grand nombre d'objets.