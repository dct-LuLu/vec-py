from vec2py.entities import Entity, Circ, Rect
from vec2py.util import DoubleRect, Vector2D, Util, Line
from pyglet import shapes


# Implementer les trois différentes types de collisions handler

# PM Quadtree (maybe compressed?)
# https://www.cs.umd.edu/~meesh/cmsc420/ContentBook/FormalNotes/PMQuadtree/pm_quadtree_samet.pdf

# Grid Hierarchy
# TASDisplay

class PolygonMapQuadtree:
    _MAX_DEPTH = 6  # 5 461
    _MAX_NODES = int((4 ** (_MAX_DEPTH + 1) - 1) / 3)
    PRE_CACHED_BOUNDS = {}

    if Util.DEBUG:
        debug_squares = set()

    def __init__(self, window_width, window_height):
        self._root = None
        PolygonMapQuadtree.PRE_CACHED_BOUNDS["ROOT"] = DoubleRect.make(Vector2D(0, 0),
                                                                       Vector2D(window_width, window_height))
        self.__precache(PolygonMapQuadtree._MAX_NODES)
        self.routine()

    def __precache(self, stage: int, upper: int = "ROOT"):
        stage = int((stage - 1) // 4)

        if stage >= 1:
            bounds = PolygonMapQuadtree.PRE_CACHED_BOUNDS[upper]

            for _ in range(4):
                if upper == "ROOT":
                    next_upper = _ * stage

                else:
                    next_upper = (upper+1) + _*stage

                PolygonMapQuadtree.PRE_CACHED_BOUNDS[next_upper] = bounds.quadrant(_)
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
    def get_number(num_list):
        number = 0
        for i in range(len(num_list)):
            number += (num_list[i] * (4 ** (PolygonMapQuadtree._MAX_DEPTH - i) - 1) / 3)

        return int(number) + (len(num_list) - 1)

    def routine(self):
        CollisionDetection.may_collide = set()

        if Util.DEBUG:
            PolygonMapQuadtree.debug_squares = set()

        self._root = QuadNode(PolygonMapQuadtree._MAX_NODES)

        for polygon in Entity.get_movables():
            self._root.insert(polygon)

    def get_debug_lines(self, a=None):
        r = []
        a = self._root if a is None else a
        r.append(a.get_bounds().get_horizontal_line())
        r.append(a.get_bounds().get_vertical_line())
        g = []

        for _ in range(4):
            if a.child[_] is not None:
                if a.child[_]._stage > 1:  # agagag?
                    g += self.get_debug_lines(a.child[_])
                
        return r + g


class QuadNode:
    def __init__(self, stage: int, num: int = "ROOT"):
        self.child = [None] * 4  # [ Bottom left // Bottom right // Top right // Top left ]
        self._stage = int((stage - 1) // 4)
        self._num = num

    def get_bounds(self):
        return PolygonMapQuadtree.PRE_CACHED_BOUNDS[self._num]

    def get_rect(self, color=(85, 99, 25, 128)):
        bounds = self.get_bounds()
        return shapes.Rectangle(bounds.get_left(), bounds.get_bottom(), bounds.get_width(), bounds.get_height(),
                                color=color)
    
    def get_child_num(self, i):
        if self._num == "ROOT":
            match i:
                case 0:
                    return 0
                case 1:
                    return self._stage
                case 2:
                    return self._stage * 2
                case 3:
                    return self._stage * 3
        else:
            match i:
                case 0: return (self._num + 1)
                case 1: return (self._num + 1) + self._stage
                case 2: return (self._num + 1) + 2*self._stage
                case 3: return (self._num + 1) + 3*self._stage

    def get_child_bounds(self, i):
        assert 0 <= i <= 3, "i must be between 0 and 3"
        return PolygonMapQuadtree.PRE_CACHED_BOUNDS[self.get_child_num(i)]

    def insert(self, polygon: Entity):
        assert isinstance(polygon, Entity), "Inserting entities is only allowed."

        if self._stage >= 1:
            AABB = polygon.get_AABB()

            for _ in range(4):
                quadrants_bounds = self.get_child_bounds(_)
                if AABB.intersects(quadrants_bounds):

                    if self._stage == 1:  # LEAF NODE
                        if self.child[_] is None:
                            self.child[_] = {polygon}
                            if Util.DEBUG:
                                PolygonMapQuadtree.debug_squares.add(self.get_rect())

                        elif polygon not in self.child[_]:
                            self.child[_].add(polygon)
                            CollisionDetection.may_collide.add(frozenset([*self.child[_]]))
                            if Util.DEBUG:
                                PolygonMapQuadtree.debug_squares.add(self.get_rect((217, 45, 78, 128)))

                    else:  # BRANCH NODE
                        if self.child[_] is None: self.child[_] = QuadNode(self._stage, self.get_child_num(_))
                        self.child[_].insert(polygon)


        # get polygon AABB and store it
        # recursively check if each part of the node intersects with the polygon AABB
        # if it's a branch node, recursively continue
        # else insert the polygon reference in the node


class CollisionSAT:
    def routine(self=None):
        CollisionDetection.may_collide = set()
        for polygons in Util.unique_sets(set(Entity.get_entities())):
            if CollisionSAT.collision_check_SAT(*polygons):
                CollisionDetection.may_collide.add(polygons)

    @staticmethod
    def collision_check_SAT(shape_a: Entity, shape_b: Entity):
        axes = shape_a.get_axes_SAT() + shape_b.get_axes_SAT()

        if type(shape_a) == Circ and type(shape_b) == Rect:
            vertice = find_closest_point_on_polygon(shape_a.get_pos(), shape_b.get_corners())
            axes.append((shape_a.get_pos() - vertice).normalize())
            if Util.DEBUG:
                Util.LINES.append(Line(shape_a.get_pos(), vertice, (255,0,0,255)))

        if type(shape_a) == Rect and type(shape_b) == Circ:
            vertice = find_closest_point_on_polygon(shape_b.get_pos(), shape_a.get_corners())
            axes.append((vertice - shape_b.get_pos()).normalize())
            if Util.DEBUG:
                Util.LINES.append(Line(vertice, shape_b.get_pos(), (255,0,0,255)))

        if type(shape_a) == Circ and type(shape_b) == Circ:
            axes.append((shape_a.get_pos() - shape_b.get_pos()).normalize())
            if Util.DEBUG:
                Util.LINES.append(Line(shape_a.get_pos(), shape_b.get_pos(), (255,0,0,255)))

        normal = Vector2D(0, 0)
        depth = float('inf')

        for axis in axes:
            p1 = shape_a.project_shape_onto_axis(axis)
            p2 = shape_b.project_shape_onto_axis(axis)

            if not p1.overlap(p2):
                return (False,)

            axisDepth = p1.get_axis_depth(p2)

            if axisDepth < depth:
                depth = axisDepth
                normal = axis

        direction = shape_b.get_pos() - shape_a.get_pos()

        if Vector2D.dot_product(direction, normal) < 0:
            normal = normal * -1;

        return True, normal, depth

def find_closest_point_on_polygon(circleCenter: Vector2D, vertices: list[Vector2D]) -> Vector2D:
    result = -1;
    minDistance = float('inf')

    for i in range(len(vertices)):
        v = vertices[i]
        distance = Vector2D.distance_squared(v, circleCenter)

        if distance < minDistance:
            minDistance = distance
            result = i

    return vertices[result]

class CollisionDetection:
    may_collide = set()

    def __init__(self, width, height, setting="SAT"):
        match setting:
            case "quadtree":
                self.system = PolygonMapQuadtree(width, height)
            case "SAT":
                self.system = CollisionSAT()

    def routine(self=None):
        self.system.routine()
