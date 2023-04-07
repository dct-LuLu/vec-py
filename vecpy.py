import math
from random import randint

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse
import numpy as np


class PhysicalObject():
    instances: set = set()

    def __init__(self, movable, draggable, velocity=[0, 0], acceleration=[0, 0]):
        self.velocity = velocity
        self.acceleration = acceleration
        self.movable = movable
        self.draggable = draggable
        PhysicalObject.instances.add(self)

    @classmethod
    def get_instances(cls):
        return cls.instances

    def get_tag(self) -> str:
        return f"{self.__class__.__name__} x: {int(self.x)} y:{int(self.y)} col:{self.color[0], self.color[1], self.color[2]}"

    def colision(self, obj1, obj2):
        obj1.velocity = np.array(obj1.velocity)
        obj2.velocity = np.array(obj2.velocity)

        coord1 = np.array([obj1.x, obj1.y])
        coord2 = np.array([obj2.x, obj2.y])

        r = math.sqrt(sum((coord1-coord2)**2))

        n = (coord2-coord1) / r
        t = np.array(-n[1], n[0])

        v1n = np.dot(obj1.velocity, n)
        v1t = np.dot(obj1.velocity, t)
        v2n = np.dot(obj2.velocity, n)
        v2t = np.dot(obj2.velocity, t)

        u1n = (v1n * (obj1.mass-obj2.mass) + 2 * obj2.mass * v2n) / (obj1.mass+obj2.mass)
        u2n = (v2n * (obj2.mass-obj1.mass) + 2 * obj1.mass * v1n) / (obj1.mass+obj2.mass)

        u1t = v1t
        u2t = v2t

        if obj1 != self.drag_object:
            obj1.velocity = u1n * n + u1t * t

        if obj2 != self.drag_object:
            obj2.velocity = u2n * n + u2t * t


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
        self.cue = False
        self.cursorpos = [0, 0]
        self.target = None

    # FIRST HIT
    def on_mouse_press(self, x, y, button, modifiers):
        self.cursorpos = [x, y]
        if button in (mouse.LEFT, mouse.RIGHT):
            for _ in PhysicalObject.get_instances():
                if _.bounds(x, y) and _.draggable and self.drag_object is None:
                    self.drag_object = _
                    self.target = self.drag_object
                    #self.drag_object.speed_gravity = 0
                    if button == mouse.LEFT:
                        self.drag_object.velocity = [0, 0]

                    elif button == mouse.RIGHT:
                        self.cue = True

    # WHILE
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.drag_object is not None: # On peut potentiellement aussi calculer la distance entre le curseur et le point central de l'objet et le modifier en gardant cette distance
            if buttons & mouse.LEFT:
                self.drag_object.x += dx
                self.drag_object.y += dy
                self.drag_object.velocity = [dx*100, dy*100]

            if buttons & mouse.RIGHT:
                self.cursorpos = [x, y]
                


    # AFTER
    def on_mouse_release(self, x, y, button, modifiers):
        if self.drag_object is not None:
            if button & mouse.LEFT:
                self.drag_object = None

            elif button & mouse.RIGHT:
                self.drag_object.velocity[0] = 5 * (self.drag_object.x - x)
                self.drag_object.velocity[1] = 5 * (self.drag_object.y - y)
                self.cue = False
                self.drag_object = None


class Sim:
    def __init__(self):
        self.init_render_objects()


        self.quadtree = QuadTree(0, 0, self.width, self.height) # TODO: setup la quadtree map
        self.quadtree.check()

    def init_render_objects(self):
        main_batch = pyglet.graphics.Batch()
        ground = Rect(x=0, y=0, width=self.width, height=int(1/30*self.height), color=(93,23,222,89), movable=False, draggable=False)
        counter = pyglet.window.FPSDisplay(window=self)
        label = pyglet.text.Label("", color=(122, 122, 122, 255), font_size=36, x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center')
        cue_line = shapes.Line(0, 0, 0, 0, 0, color = (120, 35, 120, 120), batch = main_batch)
        self.sp = {n: v for n, v in vars().items() if n != "self"}
        #print(self.sp)

        #self.circle = Circ(x=self.width//2, y=self.height//2, radius=100, color=(50, 225, 30))
        [Circ(x=randint(100, self.width-100), y=randint(100, self.height-100), radius=randint(5,80), color=(randint(0,255), randint(0,255), randint(0,255), 255), velocity=[randint(-1000,1000), randint(-1000,1000)]) for x in range(randint(2, 10))]

    def get_sim_attributes(self):
        sim_attributes = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('__')}
        return sim_attributes

    # EVENT
    def on_draw(self):
        self.clear()
        for _ in PhysicalObject.get_instances():
            _.draw()

        for _ in self.sp.values():
            _.draw()

        #self.quadtree.check()
        for _ in self.quadtree.get_quadtree_divisions():
            _.draw()


    def update(self, dt):
        if self.cue:
            self.sp["cue_line"].x = self.drag_object.x
            self.sp["cue_line"].y = self.drag_object.y
            self.sp["cue_line"].x2 = self.cursorpos[0]
            self.sp["cue_line"].y2 = self.cursorpos[1]
            self.sp["cue_line"]._width = 5
        else:
            self.sp["cue_line"].x = 0
            self.sp["cue_line"].y = 0
            self.sp["cue_line"].x2 = 0
            self.sp["cue_line"].y2 = 0
            self.sp["cue_line"]._width = 0

        for shape in PhysicalObject.get_instances():
            if shape.movable and not (shape == self.drag_object and not self.cue):

                shape.acceleration[0] = -shape.velocity[0] * 0.8
                shape.acceleration[1] = -shape.velocity[1] * 0.8
                shape.velocity[0] += shape.acceleration[0] * dt
                shape.velocity[1] += shape.acceleration[1] * dt

                if shape.x + shape.radius >= self.width:
                    shape.velocity[0] = -shape.velocity[0]
                    shape.x = self.width - shape.radius

                if shape.x - shape.radius <= 0:
                    shape.velocity[0] = -shape.velocity[0]
                    shape.x = shape.radius

                if shape.y + shape.radius >= self.height:
                    shape.velocity[1] = -shape.velocity[1]
                    shape.y = self.height - shape.radius

                if shape.y - shape.radius <= 0:
                    shape.velocity[1] = -shape.velocity[1]
                    shape.y = shape.radius
 
                shape.x += shape.velocity[0] * dt
                shape.y += shape.velocity[1] * dt

                if abs(shape.velocity[0]**2 + shape.velocity[1]**2) < 0.01:
                    shape.velocity = [0, 0]
        
        if self.target is not None:
            self.sp["label"].text = f"nb: {len(PhysicalObject.get_instances())} x: {int(self.target.x)} y:{int(self.target.y)} dx:{int(self.target.velocity[0])} dy:{int(self.target.velocity[1])}"

        objects = PhysicalObject.get_instances()
        for shape_a in objects:
            if shape_a.movable and shape_a.draggable:
                for shape_b in objects:
                    if shape_b.movable and shape_b.draggable:# bouze temporaire en attendant l'imple du quadtree
                        if shape_b != shape_a:
                            if (shape_a.x-shape_b.x)**2 + (shape_a.y-shape_b.y)**2 <= (shape_a.radius + shape_b.radius)**2: # plus rapide sans la racine carré
                                distance = math.sqrt((shape_a.x-shape_b.x)**2 + (shape_a.y-shape_b.y)**2) # par contre là on est obligé lol
                                overlap = distance - shape_a.radius - shape_b.radius
                                if self.drag_object not in (shape_a, shape_b):
                                    overlap *= 0.5
                                else:
                                    overlap *= 2 # A CHANGER

                                if shape_a != self.drag_object:
                                    shape_a.x -= overlap * (shape_a.x - shape_b.x) / distance
                                    shape_a.y -= overlap * (shape_a.y - shape_b.y) / distance

                                if shape_b != self.drag_object:
                                    shape_b.x -= overlap * (shape_b.x - shape_a.x) / distance
                                    shape_b.y -= overlap * (shape_b.y - shape_a.y) / distance

                                self.sp["label"].color = (255,255,100, 255)
                                PhysicalObject.colision(self, shape_a, shape_b)
                            else:
                                self.sp["label"].color = (122, 122, 122, 255)


class Wind(Sim, Events, pyglet.window.Window):
    def __init__(self, *args, **kwargs):    
        # Création de la fenêtre
        pyglet.window.Window.__init__(self, *args, **kwargs) # la fenêtre c'est self ... lol.
        #self.mousebuttons = mouse.MouseStateHandler()
        #self.push_handlers(self.mousebuttons)
        Sim.__init__(self)
        Events.__init__(self)

        pyglet.clock.schedule_interval(self.update, 1 / 1200.0)
        pyglet.app.run()



class QuadTree:
    __MAX_OBJECTS = 2
    __MAX_LEVELS = 6
    
    def __init__(self, x, y, width, height, phy_obj=[], level=0):
        print(x, y, level)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.phy_obj = phy_obj
        self.children = [None] * 4
    
    def check(self):
        sub_QuadTree = [[]] * 4
        half_width, half_height = self.width/2, self.height/2
        x1, y1 = self.x, self.y
        x2, y2 = self.x + half_width, self.y + half_height
        x3, y3 = self.x + self.width, self.y + self.height

        for phy_obj in PhysicalObject.get_instances():
            if (x1 <= phy_obj.x <= x2) and (y1 <= phy_obj.y <= y2):
                sub_QuadTree[0].append(phy_obj)
            elif (x2 <= phy_obj.x <= x3) and (y1 <= phy_obj.y <= y2):
                sub_QuadTree[1].append(phy_obj)
            elif (x1 <= phy_obj.x <= x2) and (y2 <= phy_obj.y <= y3):
                sub_QuadTree[2].append(phy_obj)
            elif (x2 <= phy_obj.x <= x3) and (y2 <= phy_obj.y <= y3):
                sub_QuadTree[3].append(phy_obj)


        for i, sub_phy_obj in enumerate(sub_QuadTree):
            if len(sub_phy_obj) >= self.__MAX_OBJECTS and self.level < self.__MAX_LEVELS:
                self.children[i] = QuadTree(*self.get_sub_quadtree_coords(i), sub_phy_obj, self.level+1)
                self.children[i].check()
            else:
                self.children[i] = None

    def get_quadtree_divisions(self):
        sub = []
        for child in self.children:
            if child is not None:
                sub.append(Rect(x=child.x, y=child.y, width=child.width, height=child.height, color=(5*self.level,222,102, 10*self.level), movable=False, draggable=False))
                sub += child.get_quadtree_divisions()
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