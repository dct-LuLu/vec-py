from vec2py.entities.Entity import Entity
from vec2py.util import DoubleRect, Util, Vector

from pyglet import shapes

class Circ(Entity, shapes.Circle):
    def __init__(self, x, y, radius, segments=None, color=(255, 255, 255, 255), x_velocity=0, y_velocity=0, angular_velocity=0):
        if segments is None: self.fixed_segments = False
        else: self.fixed_segments = True
        
        shapes.Circle.__init__(self, x, y, radius, segments, color)
        # creates, x, y, radius, color vars
        Entity.__init__(self)

        self._squared_radius = radius**2 # évite de faire 50 fois la même opération et de faire des racines carrées

    @property
    def radius(self):
        return self._radius

    #Override la library pour que lorsqu'on augmante la taille du cercle le nombre de segments soit recalculé
    @radius.setter
    def radius(self, value):
        self._radius = value
        self._squared_radius = value**2
        if not self.fixed_segments:
            self._segments = max(14, int(value / 1.25))
            self._num_verts = self._segments * 3
            self._create_vertex_list()
        self._update_vertices()
        #if Util.DEBUG: print(f"radius: {self._radius} segments: {self._segments}")

    def get_pos(self):
        """
        Returns the position of the circle as a Vector
        """
        return Vector(self.x, self.y)

    def get_AABB(self):
        """
        Returns the axis-aligned bounding box of the circle
        """
        return DoubleRect.makeCentered(self.get_pos(), self.radius*2)
    
    def is_inside(self, point: Vector):
        """
        Returns whether the given point is inside the circle
        """
        #((point.getX()-self.x)**2 + (point.getY()-self.y)**2)
        return self._squared_radius >= point.distanceSquared(self.get_pos())

if __name__ == "__main__":
    c = Circ(5, 5, 5)
    print(c.is_inside(Vector(2, 2)))
    print(c.is_inside(Vector(15, 5)))
    c.radius += 5
    print(c.radius)
    print(c.get_pos())
    print(c.get_AABB())
    print(c.is_inside(Vector(12, 7)))
    print(c.is_inside(Vector(20, 5)))