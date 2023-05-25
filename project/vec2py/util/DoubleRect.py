from vec2py.util.Vector import Vector
from vec2py.util.Util import Util
from vec2py.util.Line import Line

class DoubleRect:
    def __init__(self, left, bottom, right, top):
        self._left = left
        self._bottom = bottom
        self._right = right
        self._top = top
        if self._left > self._right:
            raise ValueError(f"DoubleRect : left > right {self._left} > {self._right}")
        if self._bottom > self._top:
            raise ValueError(f"DoubleRect : bottom > top {self._bottom} > {self._top}")

    def __str__(self):
        return str("DoubleRect{left: " + Util.NF(self._left) + ", right: " + Util.NF(self._right) + ", top: " + Util.NF(self._top) + ", bottom: " + Util.NF(self._bottom) + "}") if Util.DEBUG else str()
    
    def __repr__(self):
        return str("DoubleRect{left: " + Util.NF(self._left) + ", right: " + Util.NF(self._right) + ", top: " + Util.NF(self._top) + ", bottom: " + Util.NF(self._bottom) + "}") if Util.DEBUG else str()


    def getBottom(self) -> float:
        """
        Returns the bottom y-coordinate of this rectangle
        """
        return self._bottom

    def getLeft(self) -> float:
        """
        Returns the left x-coordinate of this rectangle
        """
        return self._left

    def getRight(self) -> float:
        """
        Returns the right x-coordinate of this rectangle
        """
        return self._right

    def getTop(self) -> float:
        """
        Returns the top y-coordinate of this rectangle
        """
        return self._top


    def getHeight(self) -> float:
        """
        Returns the height of this rectangle
        """
        return self._top - self._bottom

    def getWidth(self) -> float:
        """
        Returns the width of this rectangle
        """
        return self._right - self._left


    def getCenterX(self) -> float:
        """
        Returns the x-coordinate of the center of this rectangle
        """
        return (self._left + self._right)/2

    def getCenterY(self) -> float:
        """
        Returns the y-coordinate of the center of this rectangle
        """
        return (self._bottom + self._top)/2

    def getCenter(self) -> Vector:
        """
        Returns the center of this rectangle
        """
        return Vector(self.getCenterX(), self.getCenterY())


    def getCoordinates(self) -> tuple[Vector, Vector, Vector, Vector]:
        """
        Returns the four corners of this rectangle
        """
        return (Vector(self._left, self._bottom), Vector(self._right, self._bottom), Vector(self._right, self._top), Vector(self._left, self._top))


    @staticmethod
    def make(point1: Vector, point2: Vector) -> "DoubleRect":
        """
        Returns a new rectangle with the given corners
        """
        LEFT = min(point1.getX(), point2.getX())
        RIGHT = max(point1.getX(), point2.getX())
        TOP = max(point1.getY(), point2.getY())
        BOTTOM = min(point1.getY(), point2.getY())
        return DoubleRect(LEFT, BOTTOM, RIGHT, TOP)

    @staticmethod
    def makeCentered(center: Vector, width, height=None) -> "DoubleRect":
        """
        Returns a new rectangle with the given center and size
        """
        height = height or width
        HALF_WIDTH = width/2
        HALF_HEIGHT = height/2
        return DoubleRect(center.getX() - HALF_WIDTH, center.getY() - HALF_HEIGHT, center.getX() + HALF_WIDTH, center.getY() + HALF_HEIGHT)


    def containsPoint(self, point: Vector) -> bool:
        """
        Returns whether the given point is inside the rectangle
        """
        return self._left <= point.getX() <= self._right and self._bottom <= point.getY() <= self._top

    def containsRect(self, rect: "DoubleRect") -> bool:
        """
        Returns whether this rectangle contains the given other rectangle
        """
        return not(self._left >= rect.getLeft() or self._bottom <= rect.getBottom() or self._right <= rect.getRight() or self._top >= rect.getTop())

    def touches(self, rect: "DoubleRect") -> bool:
        return ((self._left == rect.getRight()) or (self._right == rect.getLeft())) and ((self._bottom == rect.getTop()) or (self._top == rect.getBottom()))

    def quadrant(self, n: int) -> "DoubleRect":
        """
        Returns the given quadrant of this rectangle
        0 = bottom left
        1 = bottom right
        2 = top right
        3 = top left
        """
        center_x, center_y = self.getCenterX(), self.getCenterY()
        match n:
            case 0:
                return DoubleRect(self._left, self._bottom, center_x, center_y) # bottom left 
            case 1:
                return DoubleRect(center_x, self._bottom, self._right, center_y) # bottom right
            case 2:
                return DoubleRect(center_x, center_y, self._right, self._top) # Top right
            case 3:
                return DoubleRect(self._left, center_y, center_x, self._top) # Top left
            case _:
                raise ValueError(f"DoubleRect : Invalid quadrant {n}")

    def __eq__(self, __o: "DoubleRect") -> bool:
        """
        Returns true if the given object is a rectangle with the same coordinates as this rectangle
        """
        if __o is None:
            return False
        return self._left == __o.getLeft() and self._bottom == __o.getBottom() and self._right == __o.getRight() and self._top == __o.getTop() and isinstance(__o, DoubleRect)

    def expand(self, marginX, marginY) -> "DoubleRect":
        """
        Returns a new rectangle grown in all directions by the given margins
        """
        return DoubleRect(self._left - marginX, self._bottom - marginY, self._right + marginX, self._top + marginY)

    def intersection(self, rect: "DoubleRect") -> "DoubleRect":
        """
        Returns the intersection of this rectangle with the given other rectangle
        """
        LEFT = max(self._left, rect.getLeft())
        RIGHT = min(self._right, rect.getRight())
        TOP = min(self._top, rect.getTop())
        BOTTOM = max(self._bottom, rect.getBottom())
        if LEFT > RIGHT or BOTTOM > TOP:
            return DoubleRect(0, 0, 0, 0)
        return DoubleRect(LEFT, BOTTOM, RIGHT, TOP)

    def intersects(self, rect: "DoubleRect") -> bool:
        return not((self._left > rect.getRight()) or (self._right < rect.getLeft()) or (self._top < rect.getBottom()) or (self._bottom > rect.getTop()))

    def isEmpty(self, opt_tolerance=1E-16):
        """
        Returns whether this rectangle is empty, meaning that it has a zero width or height
        """
        return self.getWidth() < opt_tolerance or self.getHeight() < opt_tolerance

    def nearEqual(self, rect, opt_tolerance=1E-16):
        """
        Returns whether this rectangle is nearly equal to the given other rectangle
        """
        if Util.veryDifferent(self._left, rect.getLeft(), opt_tolerance):
            return False
        if Util.veryDifferent(self._right, rect.getRight(), opt_tolerance):
            return False
        if Util.veryDifferent(self._top, rect.getTop(), opt_tolerance):
            return False
        if Util.veryDifferent(self._bottom, rect.getBottom(), opt_tolerance):
            return False
        return True

    def scale(self, factorX, factorY = None):
        """
        Scales the rectangle by the given factors
        """
        if factorY is None:
            factorY = factorX
        HALF_FACTOR_X = factorX/2
        HALF_FACTOR_Y = factorY/2
        X0 = self.getCenterX()
        Y0 = self.getCenterY()
        W = self.getWidth()
        H = self.getHeight()
        return DoubleRect(X0 - HALF_FACTOR_X*W, Y0 - HALF_FACTOR_Y*H, X0 + HALF_FACTOR_X*W, Y0 + HALF_FACTOR_Y*H)

    def translate(self, coords: Vector) -> "DoubleRect":
        """
        Translates the rectangle by the given amount
        """
        return DoubleRect(self._left + coords.getX(), self._bottom + coords.getY(), self._right + coords.getX(), self._top + coords.getY())

    def union(self, rect: "DoubleRect") -> "DoubleRect":
        """
        Returns the union of this rectangle with the given other rectangle
        """
        return DoubleRect(
            min(self._left, rect.getLeft()),
            max(self._right, rect.getRight()),
            max(self._top, rect.getTop()),
            min(self._bottom, rect.getBottom())
            )

    def unionPoint(self, point: Vector) -> "DoubleRect":
        """
        Returns the union of this rectangle with the given point
        """
        return DoubleRect(
            min(self._left, point.getX()),
            max(self._right, point.getX()),
            max(self._top, point.getY()),
            min(self._bottom, point.getY())
            )
    
    def get_horizontal_line(self) -> Line:
        return Line.make(self._left, self.getCenterY(), self._right, self.getCenterY())
    
    def get_vertical_line(self) -> Line:
        return Line.make(self.getCenterX(), self._bottom, self.getCenterX(), self._top)
    