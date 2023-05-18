from vec2py.util.Vector import Vector
from vec2py.util.Util import Util
from pyglet import shapes

class Line(shapes.Line):
    def __init__(self, p1: Vector, p2: Vector, color=0):
        shapes.Line.__init__(self, p1.getX(), p1.getY(), p2.getX(), p2.getY())
    
    def __str__(self):
        return str("Line{p1: "+str(self._p1)+", p2: "+str(self._p2)+"}") if Util.DEBUG else str()

    def getP1(self) -> Vector:
        """
        Returns the first endpoint of this line
        """
        return Vector(self.x, self.y)
    
    def getP2(self) -> Vector:
        """
        Returns the second endpoint of this line
        """
        return Vector(self.x2, self.y2)
    
    def getLength(self) -> float:
        """
        Returns the length of this line
        """
        return self._p1.distance(self._p2)
    
    @classmethod
    def make(self, x1: float, y1: float, x2: float, y2: float) -> "Line":
        """
        Returns a line connecting the given points
        """
        return Line(Vector(x1, y1), Vector(x2, y2))
    
    def __str__(self):
        return str("Line{p1: "+str(self._p1)+", p2: "+str(self._p2)+"}") if Util.DEBUG else str()
    
    def __repr__(self):
        return str("Line{p1: "+str(self._p1)+", p2: "+str(self._p2)+"}") if Util.DEBUG else str()