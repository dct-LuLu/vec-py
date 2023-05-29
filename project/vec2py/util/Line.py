from vec2py.util.Vector2D import Vector2D
from vec2py.util.Util import Util
from pyglet import shapes


class Line(shapes.Line):
    def __init__(self, p1: Vector2D, p2: Vector2D, color=0):
        shapes.Line.__init__(self, p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y(), color=color)

    def get_p1(self) -> Vector2D:
        """
        Returns the first endpoint of this line
        """
        return Vector2D(self.x, self.y)

    def get_p2(self) -> Vector2D:
        """
        Returns the second endpoint of this line
        """
        return Vector2D(self.x2, self.y2)

    def get_length(self) -> float:
        """
        Returns the length of this line
        """
        return self.get_p1().distance(self.get_p2())
    
    @staticmethod
    def make(x1: float, y1: float, x2: float, y2: float) -> "Line":
        """
        Returns a line connecting the given points
        """
        return Line(Vector2D(x1, y1), Vector2D(x2, y2))

    def __str__(self):
        return str("Line{p1: " + str(self.get_p1()) + ", p2: " + str(self.get_p2()) + "}") if Util.DEBUG else str()

    def __repr__(self):
        return str("Line{p1: " + str(self.get_p1()) + ", p2: " + str(self.get_p2()) + "}") if Util.DEBUG else str()
