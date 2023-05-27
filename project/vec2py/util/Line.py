from vec2py.util.Vector2D import Vector2D
from vec2py.util.Util import Util
from pyglet import shapes

class Line(shapes.Line):
    def __init__(self, p1: Vector2D, p2: Vector2D, color=0):
        shapes.Line.__init__(self, p1.getX(), p1.getY(), p2.getX(), p2.getY())
    
    def getP1(self) -> Vector2D:
        """
        Returns the first endpoint of this line
        """
        return Vector2D(self.x, self.y)
    
    def getP2(self) -> Vector2D:
        """
        Returns the second endpoint of this line
        """
        return Vector2D(self.x2, self.y2)
    
    def getLength(self) -> float:
        """
        Returns the length of this line
        """
        return self.getP1().distance(self.getP2())
    
    @staticmethod
    def make(x1: float, y1: float, x2: float, y2: float) -> "Line":
        """
        Returns a line connecting the given points
        """
        return Line(Vector2D(x1, y1), Vector2D(x2, y2))
    
    def __str__(self):
        return str("Line{p1: "+str(self.getP1())+", p2: "+str(self.getP2())+"}") if Util.DEBUG else str()
    
    def __repr__(self):
        return str("Line{p1: "+str(self.getP1())+", p2: "+str(self.getP2())+"}") if Util.DEBUG else str()