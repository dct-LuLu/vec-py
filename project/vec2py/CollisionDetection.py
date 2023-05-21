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
    def __init__(self):
        #self._root = QuadNode(self._bounds)
        self.routine()
        # Faire une liste de sets de deux polygones qui peuvent se toucher
        self._PRE_CACHED_BOUNDS = {}
        self.precache(self._bounds)
        print(self._PRE_CACHED_BOUNDS)

    def get_nb_nodes(self, depth = _MAX_DEPTH):
        return int(((4**(depth + 1) - 1) / 3)-1)


    def precache(self, bounds: DoubleRect):
        nb = self.get_nb_nodes()//4
        for _ in range(4):
            self._PRE_CACHED_BOUNDS[_*nb] = bounds.quadrant(_)
        print(self._PRE_CACHED_BOUNDS)
        
        #for _ in range(self.get_nb_nodes()): self._PRE_CACHED_BOUNDS[_] = self._PRE_CACHED_BOUNDS[_].quadrant(_)

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
        

    def routine(self):
        PolygonMapQuadtree._may_collide = set()
        PolygonMapQuadtree._fun = set()
        self._root = QuadNode(self._bounds)
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
    __MAX_DEPTH = 6
    def __init__(self, bounds: DoubleRect, level = 0):
        self._bounds = bounds
        self._childs = [None] * 4 # [ Bottom left // Bottom right // Top right // Top left ]
        self._level = level + 1
        
    def get_rect(self, color = (85, 99, 25, 128)):
        return shapes.Rectangle(self._bounds.getLeft(), self._bounds.getBottom(), self._bounds.getWidth(), self._bounds.getHeight(), color=color)

    def insert(self, polygon: Entity):
        assert isinstance(polygon, Entity), "Inserting entities is only allowed."
        if self._level <= QuadNode.__MAX_DEPTH:
            AABB = polygon.get_AABB()
            for _ in range(4):
                quad_rect = self._bounds.quadrant(_)
                if AABB.intersects(quad_rect):
                    if self._level == QuadNode.__MAX_DEPTH:# LEAF NODE
                        if self._childs[_] is None: 
                            self._childs[_] = {polygon}
                            if Util.DEBUG:
                                PolygonMapQuadtree._fun.add(self.get_rect())
                        elif polygon not in self._childs[_]:
                            self._childs[_].add(polygon)
                            PolygonMapQuadtree._may_collide.add(frozenset([*self._childs[_]]))
                            PolygonMapQuadtree._fun.add(self.get_rect((217, 45, 78, 128)))

                    else:# BRANCH NODE
                        if self._childs[_] is None: self._childs[_] = QuadNode(quad_rect, self._level)
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
