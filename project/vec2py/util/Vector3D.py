from vec2py.util.Util import Util
from vec2py.util.Vector2D import Vector2D

class Vector3D:
    _TINY_POSITIVE = 1E-10
    def __init__(self, x, y, z):
        self._x = Util.testNumber(x)
        self._y = Util.testNumber(y)
        self._z = Util.testNumber(z)

    def from_vector2D(vector2D, z = 0):
        return Vector3D(vector2D.getX(), vector2D.getY(), z)

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

    def getZ(self) -> float:
        """
        Returns the y-coordinate of this vector
        """
        return self._z

    def __str__(self) -> str:
        return str(f"Vector{{x: {self._x}, y: {self._y}, z: {self._z}}}")
    
    def __repr__(self) -> str:
        return str(self)

    def cross_product_2D(a: Vector2D, b: Vector2D):
        return Vector3D.from_vector2D(a).cross_product(Vector3D.from_vector2D(b))

    def cross_product(self, other: "Vector3D"):
        return Vector3D(self.getY() * other.getZ() - self.getZ() * other.getY(),
                        self.getZ() * other.getX() - self.getX() * other.getZ(),
                        self.getX() * other.getY() - self.getY() * other.getX())

    def self_dot_product(self):
        return self.dot_product(self)

    def dot_product(self, other: "Vector3D"):
        return self.getX() * other.getX() + self.getY() * other.getY() + self.getZ() * other.getZ()
