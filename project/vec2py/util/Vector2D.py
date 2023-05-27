from vec2py.util.Util import Util
from math import atan2, sqrt, isnan, cos, sin


class Vector2D:
    _TINY_POSITIVE = 1E-10

    def __init__(self, x, y):
        self._x = Util.test_number(x)
        self._y = Util.test_number(y)

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
        return self._x == __o.get_x() and self._y == __o.get_y()

    def __mul__(self, other) -> "Vector2D":
        """
        Returns the vector multiplied by the given factor
        """
        if isinstance(other, Vector2D):
            return Vector2D(self._x * other.get_x(), self._y * other.get_y())

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
            return Vector2D(self._x + other.get_x(), self._y + other.get_y())
        
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
            return Vector2D(self._x - other.get_x(), self._y - other.get_y())
        
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
            return Vector2D(self._x / other.get_x(), self._y / other.get_y())
        
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
            return Vector2D(self._x // other.get_x(), self._y // other.get_y())
        
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
            return Vector2D(self._x ** other.get_x(), self._y ** other.get_y())
        
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

    def get_x(self) -> float:
        """
        Returns the x-coordinate of this vector
        """
        return self._x

    def get_y(self) -> float:
        """
        Returns the y-coordinate of this vector
        """
        return self._y

    # CROSS PRODUCT LOGIC
    # [x, y, 0] # vector
    # [0, 0, w] # angle
    # cx = y * w - 0 * 0 = y * w
    # cy = 0 * 0 - x * w = -x * w
    # cz = x * 0 - y * 0 = 0
    # -> [yw, -xw, 0]
    # returns a vector

    # [x, y, 0] # vector
    # [t, v, 0] # vector
    # cx = y * 0 - 0 * v = 0
    # cy = 0 * t - x * 0 = 0
    # cz = x * v - y * t = xv - yt
    # -> [0, 0, xv - yt]
    # returns a value

    @staticmethod
    def cross_product_vec_angle(a: "Vector2D", w: float) -> "Vector2D":
        """
        Returns the cross product of this vector and the other vector
        """
        return Vector2D(w * a.get_y(), -w * a.get_x())

    @staticmethod
    def cross_product_2D(a: "Vector2D", b: "Vector2D") -> float:
        """
        Returns the cross product of this vector and the other vector
        """
        return a.get_x() * b.get_y() - a.get_y() * b.get_x()

    def get_normal(self):
        """
        Returns a new vector that is the normal to this vector
        """
        return Vector2D(-self._y, self._x)

    def get_perpendicular_unit_vector(self):
        return self.normalize().get_normal()

    def normalize(self):
        """
        Normalizes this vector to have length 1
        """
        norm = sqrt(self._x ** 2 + self._y ** 2)
        return Vector2D(self._x / norm, self._y / norm)

    @staticmethod
    def angle_to(a: "Vector2D", b: "Vector2D") -> float:
        """
        Returns the angle between this vector and the other vector, in radians; positive means counterclockwise
        """
        AT = atan2(a.get_y(), a.get_x())
        BT = atan2(b.get_y(), b.get_x())
        return Util.limit_angle(BT - AT)

    @staticmethod
    def distance_squared(a: "Vector2D", b: "Vector2D") -> float:
        """
        Returns the square of the distance between this vector and the other vector
        """
        DX = a.get_x() - b.get_x()
        DY = a.get_y() - b.get_y()
        return DX * DX + DY * DY

    @staticmethod
    def distance(a: "Vector2D", b: "Vector2D") -> float:
        """
        Returns the distance between this vector and the other vector
        """
        return sqrt(Vector2D.distance_squared(a, b))

    @staticmethod
    def is_point_on_segment(segment_start: "Vector2D", segment_end: "Vector2D", point: "Vector2D") -> bool:
        """
        Returns true if the point is on the segment
        """
        return Util.near_equal(Vector2D.distance(segment_start, point) + Vector2D.distance(point, segment_end),
                               Vector2D.distance(segment_start, segment_end))

    @staticmethod
    def dot_product(a: "Vector2D", b: "Vector2D") -> float:
        """
        Returns the dot product of this vector and the other given vector
        """
        R = a.get_x() * b.get_x() + a.get_y() * b.get_y()
        if isnan(R):
            if Util.DEBUG:
                raise ValueError(f"dot product is not a number {a} {b}")
            else:
                raise ValueError("")
        return R

    def get_angle(self) -> float:
        return atan2(self._y, self._x)

    @staticmethod
    def near_equal(a: "Vector2D", b: "Vector2D", tolerance: float) -> bool:
        """
        Returns true if the other vector is within the given tolerance of this vector
        """
        if Util.very_different(a.get_x(), b.get_x(), tolerance):
            return False
        if Util.very_different(a.get_y(), b.get_y(), tolerance):
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