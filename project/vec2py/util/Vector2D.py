from vec2py.util.Util import Util
from math import atan2, sqrt, isnan, cos, sin

class Vector2D:
    _TINY_POSITIVE = 1E-10
    def __init__(self, x, y):
        self._x = Util.testNumber(x)
        self._y = Util.testNumber(y)

    def __str__(self) -> str:
        return str("Vector{x: "+Util.NF(self._x)+", y: "+Util.NF(self._y)+"}") if Util.DEBUG else str()
    
    def __repr__(self) -> str:
        return str("Vector{x: "+Util.NF(self._x)+", y: "+Util.NF(self._y)+"}") if Util.DEBUG else str()

    def __eq__(self, __o: "Vector2D") -> bool:
        """
        Returns true if the given object is a vector with the same coordinates as this vector
        """
        if __o is None:
            return False
        return self._x == __o.getX() and self._y == __o.getY()


    def __mul__(self, other) -> "Vector2D":
        """
        Returns the vector multiplied by the given factor
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x*other.getX(), self._y*other.getY())

        elif isinstance(other, float) or isinstance(other, int):
            if other == 1:
                return self
            else:
                return Vector2D(self._x*other, self._y*other)

        else:
            raise NotImplementedError(f"cannot multiply vector by {other}")  
        
    def __rmul__(self, other) -> "Vector2D":
        """
        Returns the vector multiplied by the given factor
        """
        return self.__mul__(other)
    

    def __add__(self, other) -> "Vector2D":
        """
        Return the vector plus the given factor
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x + other.getX(), self._y + other.getY())
        
        elif isinstance(other, float) or isinstance(other, int):
            if other == 0:
                return self
            else:
                return Vector2D(self._x + other, self._y + other)
            
        else:
            raise NotImplementedError(f"cannot add vector to {other}")
        
    def __radd__(self, other) -> "Vector2D":
        """
        Return the vector plus the given factor
        """
        return self.__add__(other)        


    def __sub__(self, other) -> "Vector2D":
        """
        Return the vector minus the given factor
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x - other.getX(), self._y - other.getY())
        
        elif isinstance(other, float) or isinstance(other, int):
            if other == 0:
                return self
            else:
                return Vector2D(self._x - other, self._y - other)
            
        else:
            raise NotImplementedError(f"cannot subtract {other} from vector")

    def __rsub__(self, other) -> "Vector2D":
        """
        Return the vector minus the given factor
        """
        return self.__sub__(other)        


    def __truediv__(self, other) -> "Vector2D":
        """
        Return the vector divided by the given factor
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x / other.getX(), self._y / other.getY())
        
        elif isinstance(other, float) or isinstance(other, int):
            if other == 1:
                return self
            elif other < self._TINY_POSITIVE:
                raise ValueError(f"cannot divide by near zero {Util.NFE(other)}")
            else:
                return Vector2D(self._x / other, self._y / other)
            
        else:
            raise NotImplementedError(f"cannot divide vector by {other}")

    def __rtruediv__(self, other) -> "Vector2D":
        """
        Return the vector divided by the given factor
        """
        return self.__truediv__(other)
    

    def __floordiv__(self, other) -> "Vector2D":
        """
        Return the vector divided by the given factor
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x // other.getX(), self._y // other.getY())
        
        elif isinstance(other, float) or isinstance(other, int):
            if other == 1:
                return self
            elif other < self._TINY_POSITIVE:
                raise ValueError(f"cannot divide by near zero {Util.NFE(other)}")
            else:
                return Vector2D(self._x // other, self._y // other)
            
        else:
            raise NotImplementedError(f"cannot divide vector by {other}")
        
    def __rfloordiv__(self, other) -> "Vector2D":
        """
        Return the vector divided by the given factor
        """
        return self.__floordiv__(other)


    def __pow__(self, other) -> "Vector2D":
        """
        Return the vector raised to the given power
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x ** other.getX(), self._y ** other.getY())
        
        elif isinstance(other, float) or isinstance(other, int):
            if other == 1:
                return self
            else:
                return Vector2D(self._x ** other, self._y ** other)
            
        else:
            raise NotImplementedError(f"cannot raise vector to {other}")
        
    def __rpow__(self, other) -> "Vector2D":
        """
        Return the vector raised to the given power
        """
        return self.__pow__(other)


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

    def cross_product_sp(self, w:int):
        return Vector2D(-w*self.getY(), w*self.getX())

    def getNormal(self):
        """
        Returns a new vector that is the normal to this vector
        """
        return Vector2D(-self._y, self._x)

    def get_perpendicular_unit_vector(self):
        return self.normalize().getNormal()

    def normalize(self):
        """
        Normalizes this vector to have length 1
        """
        norm = sqrt(self._x**2 + self._y**2)
        return Vector2D(self._x / norm, self._y / norm)

    def angleTo(self, other: "Vector2D") -> float:
        """
        Returns the angle between this vector and the other vector, in radians; positive means counterclockwise
        """
        AT = atan2(self._y, self._x)
        BT = atan2(other.getY(), other.getX())
        return Util.limitAngle(BT - AT)
        
    def distanceSquared(self, point: "Vector2D") -> float:
        """
        Returns the square of the distance between this vector and the other vector
        """
        DX = self._x - point.getX()
        DY = self._y - point.getY()
        return DX*DX + DY*DY

    def distance(self, point: "Vector2D") -> float:
        """
        Returns the distance between this vector and the other vector
        """
        return sqrt(self.distanceSquared(point))

    def dotProduct(self, other: "Vector2D") -> float:
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

    def getAngle(self) -> float:
        return atan2(self._y, self._x)

    def nearEqual(self, other: "Vector2D", tolerance: float) -> bool:
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
        return Vector2D(self._x*cosAngle - self._y*sineAngle, self._x*sineAngle + self._y*cosAngle)

    def sum(self) -> float:
        """
        Returns the sum of the coordinates of this vector
        """
        return self._x + self._y
    

EAST = Vector2D(1, 0)
NORTH = Vector2D(0, 1)
WEST = Vector2D(-1, 0)
SOUTH = Vector2D(0, -1)
ORIGIN = Vector2D(0, 0)
