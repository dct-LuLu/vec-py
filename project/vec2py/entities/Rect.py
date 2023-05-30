from vec2py.entities.Entity import Entity
from vec2py.util import DoubleRect, Vector2D, Util, Line
from math import pi, cos, sin, radians

from pyglet import shapes


class Rect(Entity, shapes.Rectangle):
    def __init__(self, x, y, width, height, rotation=0, color=(255, 255, 255, 255), is_static=False, maneuverable=True,
                 density=0.388, x_velocity=0, y_velocity=0, angular_velocity=0):
        shapes.Rectangle.__init__(self, x, y, width, height, color)
        self.rotation = rotation
        self.anchor_position = (width / 2, height / 2)
        self.needUpdate = True
        self.air_resistance_coefficient = 1.05

        Entity.__init__(self, is_static, maneuverable, density, x_velocity, y_velocity, angular_velocity)

        self.moment_of_inertia = 1 / 12 * self.get_mass() * (self.width ** 2 + self.height ** 2)

    def get_area(self):
        return self.width / 100 * self.height / 100

    def get_mass(self):
        return self.area * self.density

    def draw(self):
        # self.rotation = (self.rotation + 1) % 360
        super().draw()
        self.needUpdate = True

    def get_corners(self) -> tuple[Vector2D, Vector2D, Vector2D, Vector2D]:
        r = radians(self.rotation)

        width = self.width / 2
        height = self.height / 2

        cosr = cos(r)
        sinr = -sin(r)

        a = Vector2D(self.x + (-width * cosr - -height * sinr), self.y + (-width * sinr + -height * cosr))
        b = Vector2D(self.x + (-width * cosr - height * sinr), self.y + (-width * sinr + height * cosr))
        c = Vector2D(self.x + (width * cosr - height * sinr), self.y + (width * sinr + height * cosr))
        d = Vector2D(self.x + (width * cosr - -height * sinr), self.y + (width * sinr + -height * cosr))

        return a, b, c, d

    def get_perfored_vector(self, p) -> Vector2D:
        corners = self.get_corners()

        mini = Vector2D.distance_from_segment(corners[0], corners[1], p)
        vector = corners[0] - corners[1]

        for i in range(1, len(corners)):
            j = i + 1 if i != len(corners) - 1 else 0

            a = Vector2D.distance_from_segment(corners[i], corners[j], p)
            if a < mini:
                mini = a
                vector = corners[i] - corners[j]

        return vector

    def get_min_max(self):
        a, b, c, d = self.get_corners()
        min_x = min(a.get_x(), b.get_x(), c.get_x(), d.get_x())
        min_y = min(a.get_y(), b.get_y(), c.get_y(), d.get_y())

        max_x = max(a.get_x(), b.get_x(), c.get_x(), d.get_x())
        max_y = max(a.get_y(), b.get_y(), c.get_y(), d.get_y())

        return Vector2D(min_x, min_y), Vector2D(max_x, max_y)

    def get_AABB(self):
        if self.needUpdate:
            self.aabb = self.get_min_max()
            self.needUpdate = False

        return DoubleRect.make(self.aabb[0], self.aabb[1])

    def contains(self, point: Vector2D):
        a, b, _, d = self.get_corners()

        am = point - a
        ab = b - a
        ad = d - a

        return 0 < Vector2D.dot_product(am, ab) < Vector2D.dot_product(ab, ab) and 0 < Vector2D.dot_product(am, ad) < Vector2D.dot_product(ad, ad)

    def get_axes_SAT(self) -> list[Vector2D]:
        corners = self.get_corners()

        axes = [(corners[1] - corners[0]).get_normal().normalize(),
                (corners[2] - corners[1]).get_normal().normalize()]

        Util.LINES.append(Line((corners[0] + corners[1]) / 2, (corners[0] + corners[1]) / 2 + axes[0] * 15, (255,0,0,255)))
        Util.LINES.append(Line((corners[1] + corners[2]) / 2, (corners[1] + corners[2]) / 2 + axes[1] * 15, (255,0,0,255)))

        return axes

    def project_shape_onto_axis(self, axis: Vector2D) -> Entity.Projection:
        vertices = self.get_corners()

        p_min = Vector2D.dot_product(axis, vertices[0])
        p_max = p_min

        for vertices in vertices[1:]:
            p = Vector2D.dot_product(axis, vertices)

            if p < p_min:
                p_min = p
            elif p > p_max:
                p_max = p

        return Entity.Projection(p_min, p_max)

    def __str__(self):
        return f"Rect(x={self.x}, y={self.y}, width={self.width}, height={self.height}, rotation={self.rotation})"

    def __repr__(self):
        return self.__str__()
