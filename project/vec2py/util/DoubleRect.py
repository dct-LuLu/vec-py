from vec2py.util.Vector2D import Vector2D
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

    def get_bottom(self) -> float:
        """
        Returns the bottom y-coordinate of this rectangle
        """
        return self._bottom

    def get_left(self) -> float:
        """
        Returns the left x-coordinate of this rectangle
        """
        return self._left

    def get_right(self) -> float:
        """
        Returns the right x-coordinate of this rectangle
        """
        return self._right

    def get_top(self) -> float:
        """
        Returns the top y-coordinate of this rectangle
        """
        return self._top

    def get_height(self) -> float:
        """
        Returns the height of this rectangle
        """
        return self._top - self._bottom

    def get_width(self) -> float:
        """
        Returns the width of this rectangle
        """
        return self._right - self._left

    def get_center_x(self) -> float:
        """
        Returns the x-coordinate of the center of this rectangle
        """
        return (self._left + self._right) / 2

    def get_center_y(self) -> float:
        """
        Returns the y-coordinate of the center of this rectangle
        """
        return (self._bottom + self._top) / 2

    def get_center(self) -> Vector2D:
        """
        Returns the center of this rectangle
        """
        return Vector2D(self.get_center_x(), self.get_center_y())

    def get_corners(self) -> tuple[Vector2D, Vector2D, Vector2D, Vector2D]:
        """
        Returns the four corners of this rectangle
        """
        return Vector2D(self._left, self._bottom), Vector2D(self._right, self._bottom), Vector2D(self._right,
                                                                                                 self._top), Vector2D(
            self._left, self._top)

    @staticmethod
    def make(point1: Vector2D, point2: Vector2D) -> "DoubleRect":
        """
        Returns a new rectangle with the given corners
        """
        left = min(point1.get_x(), point2.get_x())
        right = max(point1.get_x(), point2.get_x())
        top = max(point1.get_y(), point2.get_y())
        bottom = min(point1.get_y(), point2.get_y())
        return DoubleRect(left, bottom, right, top)

    @staticmethod
    def make_from_center(center: Vector2D, width, height=None) -> "DoubleRect":
        """
        Returns a new rectangle with the given center and size
        """
        height = height or width
        half_width = width / 2
        half_height = height / 2
        return DoubleRect(center.get_x() - half_width, center.get_y() - half_height, center.get_x() + half_width,
                          center.get_y() + half_height)

    def contains_point(self, point: Vector2D) -> bool:
        """
        Returns whether the given point is inside the rectangle
        """
        return self._left <= point.get_x() <= self._right and self._bottom <= point.get_y() <= self._top

    def contains_rect(self, rect: "DoubleRect") -> bool:
        """
        Returns whether this rectangle contains the given other rectangle
        """
        return not (
                    self._left >= rect.get_left() or self._bottom <= rect.get_bottom() or self._right <= rect.get_right() or self._top >= rect.get_top())

    def touches(self, rect: "DoubleRect") -> bool:
        return ((self._left == rect.get_right()) or (self._right == rect.get_left())) and (
                    (self._bottom == rect.get_top()) or (self._top == rect.get_bottom()))

    def quadrant(self, n: int) -> "DoubleRect":
        """
        Returns the given quadrant of this rectangle
        0 = bottom left
        1 = bottom right
        2 = top right
        3 = top left
        """
        center_x, center_y = self.get_center_x(), self.get_center_y()
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
        return self._left == __o.get_left() and self._bottom == __o.get_bottom() and self._right == __o.get_right() and self._top == __o.get_top() and isinstance(
            __o, DoubleRect)

    def expand(self, margin_x, margin_y) -> "DoubleRect":
        """
        Returns a new rectangle grown in all directions by the given margins
        """
        return DoubleRect(self._left - margin_x, self._bottom - margin_y, self._right + margin_x, self._top + margin_y)

    def intersection(self, rect: "DoubleRect") -> "DoubleRect":
        """
        Returns the intersection of this rectangle with the given other rectangle
        """
        left = max(self._left, rect.get_left())
        right = min(self._right, rect.get_right())
        top = min(self._top, rect.get_top())
        bottom = max(self._bottom, rect.get_bottom())
        if left > right or bottom > top:
            return DoubleRect(0, 0, 0, 0)
        return DoubleRect(left, bottom, right, top)

    def intersects(self, rect: "DoubleRect") -> bool:
        return not ((self._left > rect.get_right()) or (self._right < rect.get_left()) or (
                    self._top < rect.get_bottom()) or (self._bottom > rect.get_top()))

    def is_empty(self, opt_tolerance=1E-16):
        """
        Returns whether this rectangle is empty, meaning that it has a zero width or height
        """
        return self.get_width() < opt_tolerance or self.get_height() < opt_tolerance

    def near_equal(self, rect, opt_tolerance=1E-16):
        """
        Returns whether this rectangle is nearly equal to the given other rectangle
        """
        if Util.very_different(self._left, rect.get_left(), opt_tolerance):
            return False
        if Util.very_different(self._right, rect.get_right(), opt_tolerance):
            return False
        if Util.very_different(self._top, rect.get_top(), opt_tolerance):
            return False
        if Util.very_different(self._bottom, rect.get_bottom(), opt_tolerance):
            return False
        return True

    def scale(self, factor_x, factor_y=None):
        """
        Scales the rectangle by the given factors
        """
        if factor_y is None:
            factor_y = factor_x
        half_factor_x, half_factor_y = factor_x / 2, factor_y / 2
        center_x, center_y = self.get_center_x(), self.get_center_y()
        width, height = self.get_width(), self.get_height()
        return DoubleRect(center_x - half_factor_x * width, center_y - half_factor_y * height,
                          center_x + half_factor_x * width, center_y + half_factor_y * height)

    def translate(self, coords: Vector2D) -> "DoubleRect":
        """
        Translates the rectangle by the given amount
        """
        return DoubleRect(self._left + coords.get_x(), self._bottom + coords.get_y(), self._right + coords.get_x(),
                          self._top + coords.get_y())

    def union(self, rect: "DoubleRect") -> "DoubleRect":
        """
        Returns the union of this rectangle with the given other rectangle
        """
        return DoubleRect(
            min(self._left, rect.get_left()),
            max(self._right, rect.get_right()),
            max(self._top, rect.get_top()),
            min(self._bottom, rect.get_bottom())
        )

    def union_point(self, point: Vector2D) -> "DoubleRect":
        """
        Returns the union of this rectangle with the given point
        """
        return DoubleRect(
            min(self._left, point.get_x()),
            max(self._right, point.get_x()),
            max(self._top, point.get_y()),
            min(self._bottom, point.get_y())
        )
    
    def get_horizontal_line(self) -> Line:
        return Line.make(self._left, self.get_center_y(), self._right, self.get_center_y())
    
    def get_vertical_line(self) -> Line:
        return Line.make(self.get_center_x(), self._bottom, self.get_center_x(), self._top)
