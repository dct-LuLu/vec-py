from vec2py.entities.Entity import Entity
from vec2py.util.Vector import Vector
from vec2py.util.DoubleRect import DoubleRect
from math import pi, cos, sin, radians

from pyglet import shapes

class Rect(Entity, shapes.Rectangle):
    def __init__(self, x, y, width, height, color=(255, 255, 255, 255)):
        shapes.Rectangle.__init__(self, x, y, width, height, color)
        Entity.__init__(self)
        self.anchor_position = (width / 2, height / 2)
        self.needUpdate = True

    def draw(self):
        self.rotation = (self.rotation + 1) % 360
        super().draw()
        self.needUpdate = True

    def get_corners(self):
        r = radians(self.rotation)

        width = self.width / 2
        height = self.height / 2

        cosr = cos(r)
        sinr = sin(r)

        a = Vector(self.x + (-width * cosr - -height * sinr), self.y + (-width * sinr + -height * cosr))
        b = Vector(self.x + (-width * cosr -  height * sinr), self.y + (-width * sinr +  height * cosr))
        c = Vector(self.x + ( width * cosr -  height * sinr), self.y + ( width * sinr +  height * cosr))
        d = Vector(self.x + ( width * cosr - -height * sinr), self.y + ( width * sinr + -height * cosr))

        return a, b, c, d

    def get_min_max(self):
        a, b, c, d = self.get_corners()
        min_x = min(a.getX(), b.getX(), c.getX(), d.getX())
        min_y = min(a.getY(), b.getY(), c.getY(), d.getY())

        max_x = max(a.getX(), b.getX(), c.getX(), d.getX())
        max_y = max(a.getY(), b.getY(), c.getY(), d.getY())

        return Vector(min_x, min_y), Vector(max_x, max_y)

    def get_AABB(self):
        if self.needUpdate:
            self.aabb = self.get_min_max()
            self.needUpdate = False

        return DoubleRect.make(self.aabb[0], self.aabb[1])

    def get_pos(self):
        return Vector(self.x, self.y)

    def is_inside(self, point: Vector):
        return self.x - self.width / 2 < point.getX() and self.x + self.width / 2 > point.getX() \
            and self.y - self.height / 2 < point.getY() and self.y + self.height / 2 > point.getY()
