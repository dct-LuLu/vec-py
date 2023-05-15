import math
from random import randint

import pyglet
import pyglet.shapes as shapes
from pyglet.window import mouse
import numpy as np



def vectorize(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Takes two points in argument and returns the vector between them"""
    return [p2[0]-p1[0], p2[1]-p1[1]]

def fast_fake_size(p1 , p2):
    """Calculates the size of the rectangle from two points (Faster for comparing distances)"""
    return ((p2[0]-p1[0])**2) + ((p2[1]-p1[1])**2)

def angl(p1, p2):
    return math.atan2(p1[1]-p2[1], p1[0]-p2[0])


class PhysicalObject():
    """
    Classe qui englobe les entitées-objets et qui contient toutes les informations nécessaires

    Attributs de la classe
    ----------
    `instances` : set
        Un set qui contient toutes les entitées existantes

    Attributs
    ----------
    `velocity` : tuple[float, float]
        Vecteur vitesse de l'objet

    `acceleration` : tuple[float, float]
        Vecteur accélération de l'objet

    `movable` : bool
        Si l'objet est amovible ou non

    `draggable` : bool
        Si l'objet est déplacable au cursuer ou non

    `rotation` : float
        L'angle de rotation de l'objet en degrées

    Methodes de la classe
    ----------
    `get_movables()` -> list[PhysicalObject]
        Returns the coordinates of the angles of the rectangle

    Methodes
    ----------
    `get_tag()` -> str
        Returns the tag of the object

    `elastic_colision(obj1: PhysicalObject, obj2: PhysicalObject)`
        Takes two objects in argument and makes them collide elastically by changing their velocities vectors
    """
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
        """Returns a list of all the movable objects"""
        return [i for i in cls.instances if i.movable]

    def get_tag(self) -> str:
        """Returns the tag of the object"""
        return f"{self.__class__.__name__} x: {int(self.x)} y:{int(self.y)} col:{self.color[0], self.color[1], self.color[2]}"

    def elastic_colision(self, obj1 , obj2):
        """Takes two objects in argument and makes them collide elastically by changing their velocities vectors"""
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
    """
    Classe qui englobe l'objet Rectangle de Pyglet et qui contient toutes les informations nécessaires

    Attributs
    ----------
    `density` : int
        la densité de l'objet (default 7850)

    `mass` : int
        la masse de l'objet calculée graçe à la densité et sa taille

    `anchor_position` : tuple[int, int]
        la position de l'ancre du rectangle (au milieu si c'est un props)

    Methodes
    ----------
    `get_corners()` -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]
        Returns the coordinates of the angles of the rectangle

    `get_min_max()` -> tuple[float, float, float, float]
        Returns the minimum x, minimum y, maximum x, maximum y values

    `get_aabb()` -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]
        Returns the coordinates of the Aligned-Axis Bounding Box

    `get_proj_coord(phi: float)` -> tuple[float, float]
        Takes an angle in degrees and returns the coordinates of the point projection from the center of the rectangle to its edge

    `bounds(cx, cy)` -> bool
        Takes coordinates in argument and returns True if the point is inside the rectangle

    `restrain()`
        Restrain the rectangle inside the window
    """

    def __init__(self, movable: bool = True, draggable: bool = True, velocity: list[int, int]=[0, 0], acceleration: list[int, int]=[0, 0], rotation: float=0, density: int=7850, *args, **kwargs):
        shapes.Rectangle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable, velocity, acceleration, rotation)
        self.density = density
        self.radius = 2 # FEURUURURUR
        self.mass = self.width * self.height * self.density
        if movable: self.anchor_position = (self.width/2, self.height/2)


    def get_corners(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        """Returns the coordinates of the angles of the rectangle"""
        r = math.radians(self.rotation+90%360)
        u = (math.cos(r), -math.sin(r))
        v = (-math.sin(r), -math.cos(r))
        h, w = self.height/2, self.width/2
        a = (self.x -h*u[0] +w*v[0], self.y -h*u[1] +w*v[1])
        b = (self.x -h*u[0] -w*v[0], self.y -h*u[1] -w*v[1])
        c = (self.x +h*u[0] -w*v[0], self.y +h*u[1] -w*v[1])
        d = (self.x +h*u[0] +w*v[0], self.y +h*u[1] +w*v[1])
        return a, b ,c ,d


    def get_min_max(self) -> tuple[float, float, float, float]:
        """Returns the minimum x, minimum y, maximum x, maximum y values"""
        a,b,c,d = self.get_corners()
        min_x = min(a[0], b[0], c[0], d[0])
        min_y = min(a[1], b[1], c[1], d[1])

        max_x = max(a[0], b[0], c[0], d[0])
        max_y = max(a[1], b[1], c[1], d[1])

        return min_x, min_y, max_x, max_y


    def get_aabb(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        """Returns the coordinates of the Aligned-Axis Bounding Box"""
        min_x, min_y, max_x, max_y = self.get_min_max()
        return (min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)


    def get_proj_coord(self, phi) -> tuple[float, float]:
        """Takes an angle in degrees and returns the coordinates of the point projection from the center of the rectangle to its edge"""
        a, b = self.width, self.height
        alpha = math.radians((self.rotation+phi)%360)
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
        """Takes coordinates in argument and returns True if the point is inside the rectangle"""
        a, b, c, _ = self.get_corners()
        AB, AM, BC, BM = vectorize(a, b), vectorize(a, [cx, cy]), vectorize(b, c), vectorize(a, [cx, cy]) 
        return (0 <= np.dot(AB, AM) <= np.dot(AB, AB)) and (0 <= np.dot(BC, BM) <= np.dot(BC, BC))


    def collision_check(self, other) -> bool:
        """Check if the rectangles are colliding"""
        assert isinstance(other, Rect), "The objects must be rectangles"
        return len(self.angle_colliding(other)) > 0


    def angle_colliding(self, other) -> tuple:
        """Check if the rectangle is colliding with the other rectangle"""
        for _, angles in enumerate(other.get_corners()):
            # Les coordonnées des angles du second rectangle
            phi = angl([self.x, self.y], angles) + math.radians(180) # L'angle (en radians)
            surf = self.get_proj_coord(math.degrees(phi)%360) # La coordonnée du point projeté sur la surface du premier rectangle en direction du second rectangle PAR RAPPOOOOOOOOOOOORT au centre du premier rectangle
            leng = math.sqrt(surf[0]**2 + surf[1]**2) # Trick jsplus d'ou je sors mais ça work

            #self.sp["u"][_][0].x, self.sp["u"][_][0].y = other1.x + leng *math.cos(phi), other1.y + leng *math.sin(phi) #NO MORE +4???????
            #self.sp["u"][_][1].x, self.sp["u"][_][1].y  = other1.x, other1.y
            #self.sp["u"][_][1].x2, self.sp["u"][_][1].y2  = angles

            proj_dist = fast_fake_size([self.x, self.y], [self.x+surf[0], self.y+surf[1]]) # La distance entre le milieu du premier rectangle et le point projeté sur la surface du premier rectangle
            ecart_dist = fast_fake_size([self.x, self.y], angles) # La distance entre les angles du second rectangle et le milieu du premier rectangle

            if 0 >= (ecart_dist - proj_dist):
                return angles, leng, phi
        return ()


    def anti_overlap(self, other):        
        angles, leng, phi = self.angle_colliding(other)
        overlap_x = angles[0] - (self.x + leng *math.cos(phi))
        overlap_y = angles[1] - (self.y + leng *math.sin(phi))

        print(overlap_x, overlap_y)

        self.x += overlap_x * 2
        self.y += overlap_y * 2

        other.x -= overlap_x * 2
        other.y -= overlap_y * 2

        # FAIRE UN ANTI OVERLAAAAAAP< DIGNE DE CE NOM
        # if other.velocity[0] > 0:
        #     other.velocity[0] -= abs(overlap_x)
        #     self.velocity[0] += abs(overlap_x)
        # elif other.velocity[0] < 0:
        #     other.velocity[0] += abs(overlap_x)
        #     self.velocity[0] -= abs(overlap_x)
        # if other.velocity[1] > 0:
        #     other.velocity[1] += abs(overlap_y)
        #     self.velocity[1] -= abs(overlap_y)
        # elif other.velocity[1] < 0:
        #     other.velocity[1] -= abs(overlap_y)
        #     self.velocity[1] += abs(overlap_y)


    def restrain(self):
        """Restrain the rectangle inside the window"""
        global win_width, win_height
        min_x, min_y, max_x, max_y = self.get_min_max()
        if max_x >= win_width:
            self.color = (122, 222, 22, 255)
            self.velocity[0] = -self.velocity[0]
            self.x = win_width - (max_x-min_x)/2

        if min_x <= 0: 
            self.color = (122, 222, 22, 255)
            self.velocity[0] = -self.velocity[0]
            self.x = (max_x-min_x)/2


        if max_y >= win_height:
            self.color = (122, 222, 22, 255)
            self.velocity[1] = -self.velocity[1]
            self.y = win_height-(max_y-min_y)/2

        if min_y <= 0:
            self.color = (122, 222, 22, 255)
            self.velocity[1] = -self.velocity[1]
            self.y = (max_y-min_y)/2


class Circ(PhysicalObject, shapes.Circle):
    """
    Classe qui englobe l'objet Circle de Pyglet et qui contient toutes les informations nécessaires

    Attributs
    ----------
    `density` : int
        la densité de l'objet (default 7850)

    `mass` : int
        la masse de l'objet calculée graçe à la densité et sa taille

    Methodes
    ----------
    `bounds(cx, cy)` -> bool
        Takes coordinates in argument and returns True if the point is inside the circle

    `restrain()`
        Restrain the circle inside the window
    """
    def __init__(self, movable: bool = True, draggable: bool = True, velocity: list[int, int]=[0, 0], acceleration: list[int, int]=[0, 0], rotation: float=0, density: int=7850, *args, **kwargs):
        shapes.Circle.__init__(self, *args, **kwargs)
        PhysicalObject.__init__(self, draggable, movable, velocity, acceleration, rotation)
        self.density = density
        self.mass = math.pi * self.radius * self.density


    def bounds(self, cx, cy) -> bool:
        """Takes coordinates in argument and returns True if the point is inside the circle"""
        return self.radius >= math.sqrt((cx-self.x)**2+(cy-self.y)**2)


    def collision_check(self, other) -> bool:
        """Check if the circles are colliding"""
        assert isinstance(other, Circ), "The objects must be circles"
        return (self.x-other.x)**2 + (self.y-other.y)**2 <= (self.radius + other.radius)**2 # plus rapide sans la racine carré


    def anti_overlap(self, other):
        """Function that moves the circles so that they never overlap"""
        distance = math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
        overlap = distance - self.radius - other.radius
        overlap *= 2 # A CHANGER

        if distance == 0:distance = 1

        self.x -= overlap * (self.x - other.x) / distance
        self.y -= overlap * (self.y - other.y) / distance

        other.x -= overlap * (other.x - self.x) / distance
        other.y -= overlap * (other.y - self.y) / distance
        

    def restrain(self):
        """Restrain the circle inside the window"""
        if self.x + self.radius >= self.width:
            self.velocity[0] = -self.velocity[0]
            self.x = self.width - self.radius

        if self.x - self.radius <= 0:
            self.velocity[0] = -self.velocity[0]
            self.x = self.radius

        if self.y + self.radius >= self.height:
            self.velocity[1] = -self.velocity[1]
            self.y = self.height - self.radius

        if self.y - self.radius <= 0:
            self.velocity[1] = -self.velocity[1]
            self.y = self.radius


class Events:
    def __init__(self):
        self.drag_object = None # Référence à l'objet que l'on déplace
        self.cue_object = None # Référence à l'objet qui va être tiré

        self.cursorpos = [0, 0]
        self.target = None # Référence à l'objet selectionné pour les informations

    # FIRST HIT
    def on_mouse_press(self, x, y, button, modifiers):
        self.cursorpos = [x, y]
        if button in (mouse.LEFT, mouse.RIGHT):
            for _ in PhysicalObject.get_movables():
                if _.bounds(x, y) and _.draggable:
                    if (button == mouse.LEFT) and self.drag_object is None: # Drag
                        self.target = _
                        self.drag_object = _
                        self.drag_object.velocity = [0, 0]

                    elif (button == mouse.RIGHT) and self.cue_object is None: # Cue
                        self.target = _
                        self.cue_object = _

    # WHILE
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if (buttons & mouse.LEFT) and self.drag_object is not None:
            self.drag_object.x += dx
            self.drag_object.y += dy
            self.drag_object.velocity = [dx*100, dy*100]

        if (buttons & mouse.RIGHT) and self.cue_object is not None:
            self.cursorpos = [x, y]
                
    # AFTER
    def on_mouse_release(self, x, y, button, modifiers):
        if (button & mouse.LEFT) and self.drag_object is not None:
            self.drag_object = None

        elif (button & mouse.RIGHT) and self.cue_object is not None:
            self.cue_object.velocity[0] = 5 * (self.cue_object.x - x)
            self.cue_object.velocity[1] = 5 * (self.cue_object.y - y)
            self.cue_object = None


class Sim:
    """
    Classe qui s'occupe de la simulation

    Attributs
    ----------
    `sp` : dict[str, pyglet.shapes]
        Dictionnaire qui contient les objets de la simulation

    Methodes
    ----------
    `init_render_objects()`
        Initialise les objets de la simulation
    
    `on_draw()`
        Dessine les objets de la simulation

    `touched_reset(dt)`
        Remet les objets touchés à leur couleur d'origine

    `cue_line()`
        Dessine la ligne de visée

    `rotat(dt)`
        Fait tourner les objets de la simulation

    `move(dt)`
        Calcule les nouvelles positions des objets de la simulation

    `update(dt)`
        Met à jour les objets de la simulation, vérifie les collisions, fais les déplacements

    """
    def __init__(self):
        #self.quadtree = QuadTree(0, 0, self.width, self.height) # TODO: setup la quadtree map
        #self.quadtree.check()
        #self.quad_shape=self.quadtree.get_quadtree_divisions()
        self.init_render_objects()


    def init_render_objects(self):
        """Initialise les objets de la simulation"""
        main_batch = pyglet.graphics.Batch()
        ground = Rect(x=0, y=0, width=self.width, height=int(1/30*self.height), color=(93,23,222,89), movable=False, draggable=False)
        counter = pyglet.window.FPSDisplay(window=self)
        label = pyglet.text.Label("", color=(122, 122, 122, 255), font_size=36, x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center')
        cue_line = shapes.Line(0, 0, 0, 0, color = (120, 35, 120, 120), width=3, batch = main_batch)
        j = [shapes.Line(0, 0, 0, 0, color=(252, 82, 22, 255), width=3, batch = main_batch) for i in range(4)]
        l = Rect(x=200, y=200, width=135, height=280, color=(122, 122, 122, 255), rotation=randint(0, 360))#, angle=42)
        d = Rect(x=40, y=400, width=90, height=160, color=(122, 122, 122, 255), rotation=randint(0, 360))
        f = [shapes.Line(l.x, l.y, 0, 0, color = (i*6, i*6, i*6, 255), width=3, batch = main_batch) for i in range(36)]
        u = [[Circ(x=0, y=0, radius=8, color=(10+i*28, 255-i*28, 120, 255), movable=False, draggable=False), shapes.Line(0, 0, 0, 0, color=(10+i*28, 255-i*28, 250, 255), width=3, batch=main_batch)] for i in range(8)]

        #[Circ(x=randint(100, self.width-100), y=randint(100, self.height-100), radius=randint(5,80), color=(randint(0,255), randint(0,255), randint(0,255), 255), velocity=[randint(-1000,1000), randint(-1000,1000)]) for x in range(randint(2, 10))]
        self.sp = {n: v for n, v in vars().items() if n != "self"}


    def on_draw(self):
        """Dessine les objets de la simulation"""
        self.clear()

        #self.quadtree.check()
        #self.quad_shape=self.quadtree.get_quadtree_divisions()
        #for _ in self.quad_shape:
        #    _.draw()

        # Lines from center of the rect to the other rect corners
        a,b,c,d=self.sp["l"].get_aabb()
        self.sp["j"][0].x, self.sp["j"][0].y = a
        self.sp["j"][0].x2, self.sp["j"][0].y2 = b

        self.sp["j"][1].x, self.sp["j"][1].y = a
        self.sp["j"][1].x2, self.sp["j"][1].y2 = c

        self.sp["j"][2].x, self.sp["j"][2].y = b
        self.sp["j"][2].x2, self.sp["j"][2].y2 = d

        self.sp["j"][3].x, self.sp["j"][3].y = c
        self.sp["j"][3].x2, self.sp["j"][3].y2 = d

        def recurse_draw(tab):
            for _ in tab:
                if isinstance(_, list):
                    recurse_draw(_)
                else:
                    _.draw()

        # Casting rays from the center of the rect
        angl = 0
        for _ in self.sp["f"]:
            a,b=self.sp["l"].get_proj_coord(angl)
            leng= math.sqrt(a**2 + b**2)
            _.x = self.sp["l"].x
            _.y = self.sp["l"].y
            _.x2 = self.sp["l"].x + leng *math.cos(math.radians(angl)) #1
            _.y2 = self.sp["l"].y + leng *math.sin(math.radians(angl)) #0
            angl+=10

        for _ in PhysicalObject.get_movables():
            _.draw()

        recurse_draw(self.sp.values())


    def touched_reset(self, dt=None):
        """Remet les objets touchés à leur couleur d'origine"""
        for shape in PhysicalObject.get_movables():
            if shape != self.drag_object:
                if isinstance(shape, Rect):
                    if shape.color != (122, 122, 122, 255):
                        shape.color = (122, 122, 122, 255)
                else:
                    if shape.color != (255,255,100, 255):
                        self.sp["label"].color = (122, 122, 122, 255)


    def rotat(self, dt=None):
        """Fait tourner les objets de la simulation"""
        self.sp["l"].rotation+=0.1


    def cue_line(self):
        """Dessine la ligne de visée"""
        if self.cue_object is not None:
            self.sp["cue_line"].x = self.cue_object.x
            self.sp["cue_line"].y = self.cue_object.y
            self.sp["cue_line"].x2 = self.cursorpos[0]
            self.sp["cue_line"].y2 = self.cursorpos[1]
            self.sp["cue_line"].visible = True
        else:
            self.sp["cue_line"].visible = False


    def move(self, dt):
        """Calcule les nouvelles positions des objets de la simulation"""

        for shape in PhysicalObject.get_movables():
            if shape != self.drag_object:

                # MOVE
                shape.acceleration[0] = -shape.velocity[0] * 0.8
                shape.acceleration[1] = -shape.velocity[1] * 0.8
                shape.velocity[0] += shape.acceleration[0] * dt
                shape.velocity[1] += shape.acceleration[1] * dt

                # ANTI OOB
                shape.restrain()

                # ENERGY LOSS
                shape.x += shape.velocity[0] * dt
                shape.y += shape.velocity[1] * dt

                # FULL STOP
                if abs(shape.velocity[0]**2 + shape.velocity[1]**2) < 0.01:
                    shape.velocity = [0, 0]


    def update(self, dt):
        self.cue_line()
        self.move(dt)
        
        if self.target is not None: # debug
            feur = len([i for i in PhysicalObject.get_movables() if i.draggable and i.movable]) # nombre d'entitées
            self.sp["label"].text = f"nb: {feur} x: {int(self.target.x)} y:{int(self.target.y)} dx:{int(self.target.velocity[0])} dy:{int(self.target.velocity[1])}" # label de debug

        objects = PhysicalObject.get_movables()
        for shape_a in objects:
            for shape_b in objects:# bouze temporaire en attendant l'imple du quadtree
                if (shape_b != shape_a) and shape_a.movable and shape_a.draggable and shape_b.movable and shape_b.draggable:
                    if type(shape_a) == type(shape_b):#nesting de if pour de meilleures perfs (oui oui)
                        if shape_a.collision_check(shape_b):
                            shape_a.anti_overlap(shape_b)
                            self.sp["label"].color = (255,255,100, 255)
                            PhysicalObject.elastic_colision(self, shape_a, shape_b) 


class Wind(Sim, Events, pyglet.window.Window):
    def __init__(self, *args, **kwargs):    
        # Création de la fenêtre
        pyglet.window.Window.__init__(self, *args, **kwargs) # la fenêtre c'est self ... lol.
        #self.mousebuttons = mouse.MouseStateHandler()
        #self.push_handlers(self.mousebuttons)
        Sim.__init__(self)
        Events.__init__(self)

        pyglet.clock.schedule_interval(self.update, 1 / 1200.0)
        #pyglet.clock.schedule_interval(self.rotat, 1 / 120)
        pyglet.clock.schedule_interval(self.touched_reset, 1 / 6)
        pyglet.app.run()



class QuadTree:
    __MAX_LEVELS = 6
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
    
    def __init__(self):
        pass


if __name__ == "__main__":
    global win_width, win_height
    win_width, win_height = 800, 600
    fsim = Wind(win_width, win_height) # 800 , 600

