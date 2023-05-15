import math
from random import randint

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse
import numpy as np


class PhysicalObject():
    instances: set = set()

    def __init__(self, movable: bool, draggable: bool, velocity: list[int, int], acceleration: list[int, int], rotation: float):
        self.velocity = velocity
        self.acceleration = acceleration
        self.movable = movable
        self.draggable = draggable
        self.rotation = abs(rotation)%360
        PhysicalObject.instances.add(self)

    @classmethod
    def get_movables(cls): #IF DRAGGABLE AND MOVABLE
        return [i for i in cls.instances if i.movable]

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
    def __init__(self, movable: bool = True, draggable: bool = True, velocity: list[int, int]=[0, 0], acceleration: list[int, int]=[0, 0], rotation: float=0, density: int=7850, *args, **kwargs):
        shapes.Rectangle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable, velocity, acceleration, rotation)
        self.density = density
        self.radius = 2 # FEURUURURUR
        self.mass = self.width * self.height * self.density
        if movable: self.anchor_position = (self.width/2, self.height/2)

    def get_corners(self) -> list:
        r = math.radians(self.rotation+90%360)
        u = (math.cos(r), -math.sin(r))
        v = (-math.sin(r), -math.cos(r))
        h, w = self.height/2, self.width/2
        a = (self.x -h*u[0] +w*v[0], self.y -h*u[1] +w*v[1])
        b = (self.x -h*u[0] -w*v[0], self.y -h*u[1] -w*v[1])
        c = (self.x +h*u[0] -w*v[0], self.y +h*u[1] -w*v[1])
        d = (self.x +h*u[0] +w*v[0], self.y +h*u[1] +w*v[1])
        return [a, b ,c ,d]

    def get_min_max(self) -> list:
        a,b,c,d = self.get_corners()
        min_x = min(a[0], b[0], c[0], d[0])
        min_y = min(a[1], b[1], c[1], d[1])

        max_x = max(a[0], b[0], c[0], d[0])
        max_y = max(a[1], b[1], c[1], d[1])

        return [min_x, min_y, max_x, max_y]

    def get_aabb(self) -> list:
        #axis-aligned bounding box
        min_x, min_y, max_x, max_y = self.get_min_max()
        return [[min_x, min_y], [max_x, min_y], [min_x, max_y], [max_x, max_y]]




    def wtf(self, deff) -> list[int]:
        a, b = self.width, self.height
        alpha = math.radians((self.rotation+deff)%360)
        coords = (b/2*math.tan(alpha-3*math.pi/2), -b/2)
        if   (abs(alpha) < math.atan2(b, a)) or (abs(alpha - 2*math.pi) < math.atan2(b, a)):
            coords = (a/2, a/2*math.tan(alpha))
        elif (abs(alpha-(math.pi/2)) < math.atan2(a, b)):
            coords = (-(b/2)*math.tan(alpha-(math.pi/2)), b/2)
        elif (abs(alpha-math.pi) < math.atan2(b, a)):
            coords = (-a/2, -a/2*math.tan(alpha-math.pi))
        elif (abs(alpha-3*math.pi/2) < math.atan2(a, b)):
            coords = (b/2*math.tan(alpha-3*math.pi/2), -b/2)

        return coords


    def bounds(self, cx, cy) -> bool:
        def vectorize(p1, p2):
            return [p2[0]-p1[0], p2[1]-p1[1]]

        a, b, c, _ = self.get_corners()

        AB, AM, BC, BM = vectorize(a, b), vectorize(a, [cx, cy]), vectorize(b, c), vectorize(a, [cx, cy]) 

        return (0 <= np.dot(AB, AM) <= np.dot(AB, AB)) and (0 <= np.dot(BC, BM) <= np.dot(BC, BC))




class Circ(PhysicalObject, shapes.Circle):
    def __init__(self, movable: bool = True, draggable: bool = True, velocity: list[int, int]=[0, 0], acceleration: list[int, int]=[0, 0], rotation: float=0, density: int=7850, *args, **kwargs):
        shapes.Circle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable, velocity, acceleration, rotation)
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
            for _ in PhysicalObject.get_movables():
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
        self.quad_shape=self.quadtree.get_quadtree_divisions()

    def init_render_objects(self):
        main_batch = pyglet.graphics.Batch()
        ground = Rect(x=0, y=0, width=self.width, height=int(1/30*self.height), color=(93,23,222,89), movable=False, draggable=False)
        counter = pyglet.window.FPSDisplay(window=self)
        label = pyglet.text.Label("", color=(122, 122, 122, 255), font_size=36, x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center')
        cue_line = shapes.Line(0, 0, 0, 0, 0, color = (120, 35, 120, 120), batch = main_batch)
        j = [shapes.Line(0, 0, 0, 0, color=(252, 82, 22, 255), width=3, batch = main_batch) for i in range(4)]
        l= Rect(x=200, y=200, width=135, height=280, color=(122, 122, 122, 255), rotation=0)#, angle=42)
        d= Rect(x=40, y=400, width=85, height=110, color=(122, 122, 122, 255), rotation=0)
        f=[shapes.Line(l.x, l.y, 0, 0, color = (i*6, i*6, i*6, 255), width=3, batch = main_batch) for i in range(36)]
        #f=[Circ(x=0, y=0, radius=5, color=(25, 8, 222, 255)) for i in range(4)]
        u = [[Circ(x=0, y=0, radius=5, color=(122, 100, 12, 255)), shapes.Line(0, 0, 0, 0, color=(122, 100, 12, 255), width=1, batch=main_batch)] for i in range(4)]

        self.sp = {n: v for n, v in vars().items() if n != "self"}
        #print(self.sp)

        #self.circle = Circ(x=self.width//2, y=self.height//2, radius=100, color=(50, 225, 30))
        #[Circ(x=randint(100, self.width-100), y=randint(100, self.height-100), radius=randint(5,80), color=(randint(0,255), randint(0,255), randint(0,255), 255), velocity=[randint(-1000,1000), randint(-1000,1000)]) for x in range(randint(2, 10))]



    def get_sim_attributes(self):
        sim_attributes = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('__')}
        return sim_attributes

    # EVENT
    def on_draw(self):
        a,b,c,d=self.sp["l"].get_aabb()
        self.sp["j"][0].x, self.sp["j"][0].y = a
        self.sp["j"][0].x2, self.sp["j"][0].y2 = b

        self.sp["j"][1].x, self.sp["j"][1].y = a
        self.sp["j"][1].x2, self.sp["j"][1].y2 = c

        self.sp["j"][2].x, self.sp["j"][2].y = b
        self.sp["j"][2].x2, self.sp["j"][2].y2 = d

        self.sp["j"][3].x, self.sp["j"][3].y = c
        self.sp["j"][3].x2, self.sp["j"][3].y2 = d

        #a, b, c, d = self.sp["l"].get_corners()
        #self.sp["f"][0].x, self.sp["f"][0].y = a
        #self.sp["f"][1].x, self.sp["f"][1].y = b
        #self.sp["f"][2].x, self.sp["f"][2].y = c
        #self.sp["f"][3].x, self.sp["f"][3].y = d

        angl = 0
        for _ in self.sp["f"]:
            a,b=self.sp["l"].wtf(angl)
            leng= math.sqrt(a**2 + b**2)
            _.x = self.sp["l"].x
            _.y = self.sp["l"].y
            _.x2 = self.sp["l"].x + leng *math.cos(math.radians(angl)) #1
            _.y2 = self.sp["l"].y + leng *math.sin(math.radians(angl)) #0
            angl+=10

        self.clear()
        for _ in PhysicalObject.get_movables():
            _.draw()

        for _ in self.sp.values():
            if isinstance(_, list):
                for i in _:
                    if isinstance(i, list):
                        for j in i:
                            j.draw()
                    else:
                        i.draw()
            else:
                _.draw()


        #self.quadtree.check()
        #self.quad_shape=self.quadtree.get_quadtree_divisions()
        #for _ in self.quad_shape:
        #    _.draw()

    def touched_reset(self, dt):
        for shape in PhysicalObject.get_movables():
            if shape.movable and not (shape == self.drag_object and not self.cue):
                if isinstance(shape, Rect):
                    if shape.color != (122, 122, 122, 255):
                        shape.color = (122, 122, 122, 255)
                else:
                    if shape.color != (255,255,100, 255):
                        self.sp["label"].color = (122, 122, 122, 255)

        for i in self.sp["u"]:
            for j in i:
                j.x = 0
                j.y = 0

    def feur(self, dt):
        self.sp["l"].rotation+=0.1

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

        for shape in PhysicalObject.get_movables():
            if shape.movable and not (shape == self.drag_object and not self.cue):

                # MOVE
                shape.acceleration[0] = -shape.velocity[0] * 0.8
                shape.acceleration[1] = -shape.velocity[1] * 0.8
                shape.velocity[0] += shape.acceleration[0] * dt
                shape.velocity[1] += shape.acceleration[1] * dt


                # ANTI OOB
                if isinstance(shape, Circ):
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

                elif isinstance(shape, Rect):
                    a, b, c, d = shape.get_aabb()

                    if d[0] >= self.width:
                        shape.color = (12, 222, 22, 255)
                        shape.velocity[0] = -shape.velocity[0]
                        shape.x = self.width - (b[0]-a[0])/2

                    if a[0] <= 0: 
                        shape.color = (12, 222, 22, 255)
                        shape.velocity[0] = -shape.velocity[0]
                        shape.x = (b[0]-a[0])/2


                    if d[1] >= self.height:
                        shape.color = (12, 222, 22, 255)
                        shape.velocity[1] = -shape.velocity[1]
                        shape.y = self.height-(d[1]-b[1])/2

                    if a[1] <= 0:
                        shape.color = (12, 222, 22, 255)
                        shape.velocity[1] = -shape.velocity[1]
                        shape.y = (d[1]-b[1])/2

 

                # SLOW DOWN
                shape.x += shape.velocity[0] * dt
                shape.y += shape.velocity[1] * dt

                if abs(shape.velocity[0]**2 + shape.velocity[1]**2) < 0.01:
                    shape.velocity = [0, 0]
        
        if self.target is not None:
            feur = len([i for i in PhysicalObject.get_movables() if i.draggable and i.movable])
            self.sp["label"].text = f"nb: {feur} x: {int(self.target.x)} y:{int(self.target.y)} dx:{int(self.target.velocity[0])} dy:{int(self.target.velocity[1])}"

        objects = PhysicalObject.get_movables()
        for shape_a in objects:
            for shape_b in objects:# bouze temporaire en attendant l'imple du quadtree
                if (shape_b != shape_a) and shape_a.movable and shape_a.draggable and shape_b.movable and shape_b.draggable:
                    if isinstance(shape_a, Circ) and isinstance(shape_b, Circ):
                        if (shape_a.x-shape_b.x)**2 + (shape_a.y-shape_b.y)**2 <= (shape_a.radius + shape_b.radius)**2: # plus rapide sans la racine carré
                            distance = math.sqrt((shape_a.x-shape_b.x)**2 + (shape_a.y-shape_b.y)**2) # par contre là on est obligé lol
                            overlap = distance - shape_a.radius - shape_b.radius
                            if self.drag_object not in (shape_a, shape_b):
                                overlap *= 0.5
                            else:
                                overlap *= 2 # A CHANGER

                            if distance == 0:distance = 1

                            if shape_a != self.drag_object:
                                shape_a.x -= overlap * (shape_a.x - shape_b.x) / distance
                                shape_a.y -= overlap * (shape_a.y - shape_b.y) / distance

                            if shape_b != self.drag_object:
                                shape_b.x -= overlap * (shape_b.x - shape_a.x) / distance
                                shape_b.y -= overlap * (shape_b.y - shape_a.y) / distance

                            self.sp["label"].color = (255,255,100, 255)
                            PhysicalObject.colision(self, shape_a, shape_b)

                    if isinstance(shape_a, Rect) and isinstance(shape_b, Rect):

                        def size(p1 , p2): return math.sqrt(((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2))
                        def angl(p1, p2):return math.atan2(p1[1]-p2[1], p1[0]-p2[0])

                        # test A
                        r = [[size([shape_a.x, shape_a.y], i), angl([shape_a.x, shape_a.y], i)] for i in shape_b.get_corners()]
                        print(len(r))
                        for i, _ in enumerate(r):
                            aa = shape_a.wtf(_[1])
                            d = size([shape_a.x, shape_a.y], aa)
                            self.sp["u"][0][i].x, self.sp["u"][0][i].y = aa
                            self.sp["u"][1][i].x, self.sp["u"][1][i].y  = shape_a.x, shape_a.y
                            self.sp["u"][1][i].x2, self.sp["u"][1][i].y2  = shape_b.get_corners()[i]


                            if 0 >= (_[0] - d):
                                print("feur")
                                shape_b.velocity[0] = -shape_b.velocity[0]
                                shape_b.velocity[1] = -shape_b.velocity[1]
                                shape_a.velocity[0] = -shape_a.velocity[0]
                                shape_a.velocity[1] = -shape_a.velocity[1] 



                        # test B
                        r = [[size([shape_b.x, shape_b.y], i), angl([shape_b.x, shape_b.y], i)] for i in shape_a.get_corners()]

                        for _ in r:
                            aa = shape_a.wtf(_[1])
                            d = size([shape_b.x, shape_b.y], aa)
                            if 0 >= (_[0] - d):
                                print("feur")
                                shape_b.velocity[0] = -shape_b.velocity[0]
                                shape_b.velocity[1] = -shape_b.velocity[1]
                                shape_a.velocity[0] = -shape_a.velocity[0]
                                shape_a.velocity[1] = -shape_a.velocity[1]  


class Wind(Sim, Events, pyglet.window.Window):
    def __init__(self, *args, **kwargs):    
        # Création de la fenêtre
        pyglet.window.Window.__init__(self, *args, **kwargs) # la fenêtre c'est self ... lol.
        #self.mousebuttons = mouse.MouseStateHandler()
        #self.push_handlers(self.mousebuttons)
        Sim.__init__(self)
        Events.__init__(self)

        pyglet.clock.schedule_interval(self.update, 1 / 1200.0)
        pyglet.clock.schedule_interval(self.feur, 1 / 120)
        pyglet.clock.schedule_interval(self.touched_reset, 1 / 6)
        pyglet.app.run()



class QuadTree:
    __MAX_LEVELS = 6
    
    def __init__(self):
        pass


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