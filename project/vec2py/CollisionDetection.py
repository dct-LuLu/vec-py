from vec2py.entities.Entity import Entity
from vec2py.util import DoubleRect, Vector, Util
from pyglet import shapes


# Implementer les trois différentes types de collisions handler

# PM Quadtree (maybe compressed?)
# https://www.cs.umd.edu/~meesh/cmsc420/ContentBook/FormalNotes/PMQuadtree/pm_quadtree_samet.pdf

# Grid Hierarchy
# TASDisplay

class PolygonMapQuadtree:
    _MAX_DEPTH = 6 #5461
    _MAX_NODES = int((4**(_MAX_DEPTH + 1) - 1) / 3)
    _may_collide = set()
    _fun = set()
    _PRE_CACHED_BOUNDS = {}
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        PolygonMapQuadtree._PRE_CACHED_BOUNDS["ROOT"] = DoubleRect.make(Vector(0, 0), Vector(self.window_width, self.window_height))
        self.__precache(PolygonMapQuadtree._MAX_NODES)
        assert 22 == self.get_number(self.get_sequence(22))
        self.routine()


    def __precache(self, stage:int, upper:int="ROOT"):
        stage = int((stage-1)//4)
        if stage >= 1:
            bounds = PolygonMapQuadtree._PRE_CACHED_BOUNDS[upper]
            for _ in range(4):
                if upper == "ROOT":
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
        self._root = QuadNode(PolygonMapQuadtree._MAX_NODES)
        for polygon in Entity.get_movables():
            self._root.insert(polygon)

    def get_debug_lines(self, a = None):
        r = []
        a = self._root if a is None else a
        r.append(a.get_bounds().get_horizontal_line())
        r.append(a.get_bounds().get_vertical_line())
        g = []
        for _ in range(4):
            if a._childs[_] is not None and a._childs[_]._stage > 1: #agagag?
                g += self.get_debug_lines(a._childs[_])
        return r + g


class QuadNode:
    def __init__(self, stage:int, num:int="ROOT"):
        self._childs = [None] * 4 # [ Bottom left // Bottom right // Top right // Top left ]
        self._stage = int((stage-1)//4)
        self._num = num

    def get_bounds(self):
        return PolygonMapQuadtree._PRE_CACHED_BOUNDS[self._num]
        
    def get_rect(self, color = (85, 99, 25, 128)):
        bounds = self.get_bounds()
        return shapes.Rectangle(bounds.getLeft(), bounds.getBottom(), bounds.getWidth(), bounds.getHeight(), color=color)
    
    def get_child_num(self, i):
        if self._num == "ROOT":
            match i:
                case 0: return 0
                case 1: return self._stage
                case 2: return self._stage *2   
                case 3: return self._stage *3
        else:
            match i:
                case 0: return (self._num + 1)
                case 1: return (self._num + 1) + self._stage
                case 2: return (self._num + 1) + 2*self._stage
                case 3: return (self._num + 1) + 3*self._stage

    
    def get_child_bounds(self, i):
        assert 0 <= i <= 3, "i must be between 0 and 3"
        return PolygonMapQuadtree._PRE_CACHED_BOUNDS[self.get_child_num(i)]

    def insert(self, polygon: Entity):
        assert isinstance(polygon, Entity), "Inserting entities is only allowed."
        if self._stage >= 1:
            AABB = polygon.get_AABB()
            for _ in range(4):
                quadrants_bounds = self.get_child_bounds(_)
                if AABB.intersects(quadrants_bounds):
                    if self._stage == 1:# LEAF NODE
                        if self._childs[_] is None: 
                            self._childs[_] = {polygon}
                            if Util.DEBUG:
                                PolygonMapQuadtree._fun.add(self.get_rect())
                        elif polygon not in self._childs[_]:
                            self._childs[_].add(polygon)
                            PolygonMapQuadtree._may_collide.add(frozenset([*self._childs[_]]))
                            if Util.DEBUG:
                                PolygonMapQuadtree._fun.add(self.get_rect((217, 45, 78, 128)))

                    else:# BRANCH NODE
                        if self._childs[_] is None: self._childs[_] = QuadNode(self._stage, self.get_child_num(_))
                        self._childs[_].insert(polygon)


        # get polygon AABB and store it
        # recursively check if each part of the node intersects with the polygon AABB
        # if it's a branch node, recursively continue
        # else insert the polygon reference in the node


class CollisionDetection(PolygonMapQuadtree):
    def __init__(self, width, height, type = "quadtree"):
        self.window_width = width
        self.window_height = height
        if type == "quadtree":
            PolygonMapQuadtree.__init__(self, width, height)


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
