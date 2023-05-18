from vec2py.util.Util import Util
from math import atan2, sqrt, isnan, cos, sin

class Vector:
    _TINY_POSITIVE = 1E-10
    def __init__(self, x, y):
        self._x = Util.testNumber(x)
        self._y = Util.testNumber(y)

    def __str__(self) -> str:
        return str("Vector{x: "+Util.NF(self._x)+", y: "+Util.NF(self._y)+"}") if Util.DEBUG else str()
    
    def __repr__(self) -> str:
        return str("Vector{x: "+Util.NF(self._x)+", y: "+Util.NF(self._y)+"}") if Util.DEBUG else str()

    def getX(self) -> float:
        """
        Returns the x-coordinate of this vector
        """
        return self._x

    def getY(self) -> float:
        """
        Returns the y-coordinate of this vector
        """
        return self._y

    def angleTo(self, other: "Vector") -> float:
        """
        Returns the angle between this vector and the other vector, in radians; positive means counterclockwise
        """
        AT = atan2(self._y, self._x)
        BT = atan2(other.getY(), other.getX())
        return Util.limitAngle(BT - AT)
        
    def distanceSquared(self, point: "Vector") -> float:
        """
        Returns the square of the distance between this vector and the other vector
        """
        DX = self._x - point.getX()
        DY = self._y - point.getY()
        return DX*DX + DY*DY

    def distance(self, point: "Vector") -> float:
        """
        Returns the distance between this vector and the other vector
        """
        return sqrt(self.distanceSquaredTo(point))

    def divide(self, factor: float) -> "Vector":
        """
        Returns the vector divided by the given factor
        """
        if factor == 1:
            return self
        elif factor < self._TINY_POSITIVE:
            raise ValueError(f"cannot divide by near zero {Util.NFE(factor)}")
        else:
            return Vector(self._x/factor, self._y/factor)

    def dotProduct(self, other: "Vector") -> float:
        """
        Returns the dot product of this vector and the other given vector
        """
        R = self._x*other.getX() + self._y*other.getY()
        if isnan(R):
            if Util.DEBUG:
                raise ValueError(f"dot product is not a number {self} {other}")
            else:
                raise ValueError("")
        return R

    def __eq__(self, __o: object) -> bool:
        """
        Returns true if the given object is a vector with the same coordinates as this vector
        """
        if __o is None:
            return False
        return self._x == __o.getX() and self._y == __o.getY()

    def getAngle(self) -> float:
        return atan2(self._y, self._x)

    def multiply(self, factor: float) -> "Vector":
        """
        Returns the vector multiplied by the given factor
        """
        if factor == 1:
            return self
        else:
            return Vector(self._x*factor, self._y*factor)

    def nearEqual(self, other: "Vector", tolerance: float) -> bool:
        """
        Returns true if the other vector is within the given tolerance of this vector
        """
        if Util.veryDifferent(self._x, other.getX(), tolerance):
            return False
        if Util.veryDifferent(self._y, other.getY(), tolerance):
            return False
        return True

    def rotate(self, angle, sineAngle=None):
        """
        Returns the vector rotated counter-clockwise about the origin by the given angle in radians
        """
        if sineAngle is not None:
            cosAngle = angle
        else:
            cosAngle = cos(angle)
            sineAngle = sin(angle)
        if abs(cosAngle*cosAngle + sineAngle*sineAngle - 1) > 1E-12:
            raise ValueError(f"not cosine, sine: {cosAngle} {sineAngle}")
        return Vector(self._x*cosAngle - self._y*sineAngle, self._x*sineAngle + self._y*cosAngle)
    
    def __sub__(self, other: "Vector") -> "Vector":
        """
        Returns the vector minus the other vector
        """
        return Vector(self._x - other.getX(), self._y - other.getY())

    def __add__(self, other: "Vector") -> "Vector":
        """
        Returns the vector plus the other vector
        """
        return Vector(self._x + other.getX(), self._y + other.getY())
    
    def sum(self) -> float:
        """
        Returns the sum of the coordinates of this vector
        """
        return self._x + self._y

EAST = Vector(1, 0)
NORTH = Vector(0, 1)
WEST = Vector(-1, 0)
SOUTH = Vector(0, -1)
ORIGIN = Vector(0, 0)