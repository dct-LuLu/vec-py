from vec2py.entities.Entity import Entity
from vec2py.util.DoubleRect import DoubleRect
from vec2py.util.Vector import Vector


# Implementer les trois différentes types de collisions handler

# PM Quadtree (maybe compressed?)
# https://www.cs.umd.edu/~meesh/cmsc420/ContentBook/FormalNotes/PMQuadtree/pm_quadtree_samet.pdf

# Grid Hierarchy
# TAS

class PolygonMapQuadtree:
    def __init__(self):
        #self._root = QuadNode(self._bounds)
        self.routine()
        self._may_collide = []
        # Faire une liste de sets de deux polygones qui peuvent se toucher
        

    def routine(self):
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

    def insert(self, polygon: Entity):
        assert isinstance(polygon, Entity), "Inserting entities is only allowed."
        if self._level <= QuadNode.__MAX_DEPTH:
            AABB = polygon.get_AABB()
            for _ in range(4):
                quad_rect = self._bounds.quadrant(_)
                if AABB.intersects(quad_rect):
                    if self._level == QuadNode.__MAX_DEPTH:# LEAF NODE
                        if self._childs[_] is None: self._childs[_] = [polygon]  
                        elif polygon not in self._childs[_]:
                            self._childs[_].append(polygon)

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

