from vec2py.entities.Entity import Entity
from vec2py.util.DoubleRect import DoubleRect
from vec2py.util.Vector import Vector
from vec2py.util.Util import Util
from pyglet import shapes


# Implementer les trois différentes types de collisions handler

# PM Quadtree (maybe compressed?)
# https://www.cs.umd.edu/~meesh/cmsc420/ContentBook/FormalNotes/PMQuadtree/pm_quadtree_samet.pdf

# Grid Hierarchy
# TAS

class PolygonMapQuadtree:
    _MAX_DEPTH = 6 #5461
    _may_collide = set()
    _fun = set()
    _PRE_CACHED_BOUNDS = {}
    def __init__(self):
        #self._root = QuadNode(self._bounds)
        self.__precache(PolygonMapQuadtree._get_nb_nodes())
        assert 22 == self.get_number(self.get_sequence(22))
        #print(PolygonMapQuadtree._PRE_CACHED_BOUNDS.keys())
        print(len(PolygonMapQuadtree._PRE_CACHED_BOUNDS.keys()))
        self.routine()
        # Faire une liste de sets de deux polygones qui peuvent se toucher

    @staticmethod
    def _get_nb_nodes(depth = _MAX_DEPTH):
        return int((4**(depth + 1) - 1) / 3)


    def __precache(self, stage:int, upper:int=None):
        stage = int((stage-1)//4)
        if stage >= 1:
            if upper is None:
                bounds = self._bounds
            else:
                bounds = PolygonMapQuadtree._PRE_CACHED_BOUNDS[upper]
            for _ in range(4):
                if upper is None:
                    next_upper = _*stage
                else:
                    next_upper = (upper+1) + _*stage
                PolygonMapQuadtree._PRE_CACHED_BOUNDS[next_upper] = bounds.quadrant(_)
                self.__precache(stage, next_upper)

    @staticmethod
    def get_sequence(n):
        tab = []
        for i in range(PolygonMapQuadtree._MAX_DEPTH - 1):
            calcul = int((4**(PolygonMapQuadtree._MAX_DEPTH - i) - 1) / 3)

            tab.append(n // calcul)

            if n % calcul == 0:
                break

            n = n % calcul - 1
        else:
            tab.append(n)
        return tab

    @staticmethod
    def get_number(list):
        number = 0
        for i in range(len(list)):
            number += (list[i] * (4**(PolygonMapQuadtree._MAX_DEPTH - i) - 1) / 3)
        return int(number) + (len(list) - 1)
        

    def routine(self):
        PolygonMapQuadtree._may_collide = set()
        PolygonMapQuadtree._fun = set()
        self._root = QuadNode()
        for polygon in Entity.get_movables():
            self._root.insert(polygon)

    def get_debug_lines(self, a = None):
        r = []
        a = self._root if a is None else a
        r.append(a._bounds.get_horizontal_line())
        r.append(a._bounds.get_vertical_line())
        g = []
        for _ in range(4):
            if a._childs[_] is not None and a._childs[_]._level < 6:
                g += self.get_debug_lines(a._childs[_])
        return r + g


class QuadNode:
    def __init__(self, num:int=None, level:int = None):
        self._num = num
        self._childs = [None] * 4 # [ Bottom left // Bottom right // Top right // Top left ]
        self._level = int((level-1)//4) if level is not None else PolygonMapQuadtree._get_nb_nodes()

    def get_bounds(self):
        if self._num is None:
            return self._window_bounds
        else:
            return PolygonMapQuadtree._PRE_CACHED_BOUNDS[self._num]

        
    def get_rect(self, color = (85, 99, 25, 128)):
        return shapes.Rectangle(self.get_bounds().getLeft(), self.get_bounds().getBottom(), self.get_bounds().getWidth(), self.get_bounds().getHeight(), color=color)
    
    def get_child_num(self, i):
        if self._level >= 1:
            if self._num is None:
                match i:
                    case 0: return 0
                    case 1: return self._level
                    case 2: return self._level*2
                    case 3: return self._level*3
            else:
                match i:
                    case 0: return (self._num+1)
                    case 1: return (self._num+1) + self._level
                    case 2: return (self._num+1) + self._level*2
                    case 3: return (self._num+1) + self._level*3
    
    def get_child_bounds(self, i):
        if self._level >= 1:
            print(self.get_child_num(i), self._level, self._num, i)
            return PolygonMapQuadtree._PRE_CACHED_BOUNDS[self.get_child_num(i)]

    def insert(self, polygon: Entity):
        assert isinstance(polygon, Entity), "Inserting entities is only allowed."
        if self._level >= 1:
            AABB = polygon.get_AABB()
            for _ in range(4):
                quadrants_bounds = self.get_child_bounds(_)
                if AABB.intersects(quadrants_bounds):
                    if self._level == 1:# LEAF NODE
                        if self._childs[_] is None: 
                            self._childs[_] = {polygon}
                            if Util.DEBUG:
                                PolygonMapQuadtree._fun.add(self.get_rect())
                        elif polygon not in self._childs[_]:
                            self._childs[_].add(polygon)
                            PolygonMapQuadtree._may_collide.add(frozenset([*self._childs[_]]))
                            PolygonMapQuadtree._fun.add(self.get_rect((217, 45, 78, 128)))

                    else:# BRANCH NODE
                        if self._childs[_] is None: self._childs[_] = QuadNode(self.get_child_num(_), self._level)
                        self._childs[_].insert(polygon)


        # get polygon AABB and store it
        # recursively check if each part of the node intersects with the polygon AABB
        # if it's a branch node, recursively continue
        # else insert the polygon reference in the node


class CollisionDetection(PolygonMapQuadtree):
    def __init__(self, width, height, type = "quadtree"):
        self._bounds = DoubleRect.make(Vector(0, 0), Vector(width, height))
        if type == "quadtree":
            PolygonMapQuadtree.__init__(self)


class CollisionSAT:
    @staticmethod
    def collisionSATWithAntiOverlap(shape_a: Entity, shape_b: Entity):
        overlap = 10**6
        smallest = None
        axes_a = shape_a.get_axesSAT()
        axes_b = shape_b.get_axesSAT()

        for axis in axes_a:
            p1 = CollisionSAT.projectShapeOntoAxis(shape_a, axis)
            p2 = CollisionSAT.projectShapeOntoAxis(shape_b, axis)

            if not p1.overlap(p2):
                return None
            else:
                o = p1.getOverlap(p2);

                if (o < overlap):
                    overlap = o
                    smallest = axis

        for axis in axes_b:
            p1 = CollisionSAT.projectShapeOntoAxis(shape_a, axis)
            p2 = CollisionSAT.projectShapeOntoAxis(shape_b, axis)

            if not p1.overlap(p2):
                return None
            else:
                o = p1.getOverlap(p2);

                if (o < overlap):
                    overlap = o
                    smallest = axis

        overlap = smallest.multiply(overlap)

        dir = Vector(shape_b.x - shape_a.x, shape_b.y - shape_a.y)

        if (overlap.dotProduct(dir) > 0):
            overlap = overlap.multiply(-1)

        return overlap

    @staticmethod
    def collisionSAT(shape_a: Entity, shape_b: Entity):
        axes_a = shape_a.get_axesSAT()
        axes_b = shape_b.get_axesSAT()

        for axis in axes_a:
            p1 = CollisionSAT.projectShapeOntoAxis(shape_a, axis)
            p2 = CollisionSAT.projectShapeOntoAxis(shape_b, axis)

            if not p1.overlap(p2):
                return False

        for axis in axes_b:
            p1 = CollisionSAT.projectShapeOntoAxis(shape_a, axis)
            p2 = CollisionSAT.projectShapeOntoAxis(shape_b, axis)

            if not p1.overlap(p2):
                return False

        return True

    @staticmethod
    def projectShapeOntoAxis(shape: Entity, axis: Vector):
        vertices = shape.get_corners()

        min = axis.dotProduct(vertices[0])
        max = min

        for vertice in vertices[1:]:
            p = axis.dotProduct(vertice)

            if p < min:
                min = p
            elif p > max:
                max = p

        return Projection(min, max)

class Projection:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def overlap(self, other):
        return self.min < other.max and other.min < self.max

    def getOverlap(self, other):
        return min(self.max, other.max) - max(self.min, other.min)
