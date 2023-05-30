from math import isnan, isinf, pi, floor


class Util:
    DEBUG = False
    ADVANCED = False

    @staticmethod
    def test_finite(value):
        """
        Throws an error if the argument is not a finite number
        """
        if isinf(value):
            raise ValueError(f"not a finite number {value}")

        return value

    @staticmethod
    def test_number(value):
        """
        Throws an error if the argument is not a number
        """
        if isnan(value):
            raise ValueError(f"not a number {value}")

        return value

    @staticmethod
    def limit_angle(angle):
        """
        Returns the angle in the range [-pi, +pi]
        """
        if angle > pi:
            N = floor((angle + pi) / (2 * pi))
            return angle - 2 * pi * N

        elif angle < -pi:
            N = floor((-angle + pi) / (2 * pi))
            return angle + 2 * pi * N
        
        else:
            return angle

    @staticmethod
    def NFE(num):
        """
        Returns the number formatted as a string with 7 digit exponential notation
        """
        if num is not None:
            return "{:e}".format(num)
        
        else:
            return 'None' if num is None else 'undefined'

    @staticmethod
    def very_different(arg1, arg2, epsilon=1E-14, magnitude=1):
        """
        Returns true if the two arguments are very different
        """
        if isnan(arg1) or isnan(arg2):
            raise OverflowError('argument is NaN')

        if epsilon <= 0:
            raise ValueError(f'epsilon must be positive {epsilon}')

        if magnitude <= 0:
            raise ValueError(f'magnitude must be positive {magnitude}')

        max_arg = max(abs(arg1), abs(arg2))
        maxi = max_arg if max_arg > magnitude else magnitude

        return abs(arg1 - arg2) > epsilon * maxi

    @staticmethod
    def NF5(num):
        """
        Returns the number formatted as a string with 5 digits of precision
        """
        if num is not None:
            return "{:.5f}".format(num)
        
        else:
            return 'None' if num is None else 'undefined'

    @staticmethod
    def nf5(num):
        """
        Returns a number formatted for 5 digits of precision with cleaned up trailing zeros
        """
        if num is not None:
            s = Util.NF5(num)
            return s.rstrip('0').rstrip('.') if '.' in s else s
        
        else:
            return 'None' if num is None else 'undefined'

    @staticmethod
    def unique_sets(s: set) -> set:
        """
        Returns a set of sets of 2 objects from the input set of objects
        """
        r = set()
        for i in s:
            for j in s:
                if i != j:
                    r.add(frozenset([i, j]))
        return r

    @staticmethod
    def near_equal(a, b, epsilon=1E-14):
        """
        Returns true if the two arguments are nearly equal
        """
        if epsilon <= 0:
            raise ValueError(f'epsilon must be positive {epsilon}')

        return abs(a - b) < epsilon * max(abs(a), abs(b))

    @staticmethod
    def clamp(value: float, v_min: float, v_max: float):
        if v_min == v_max:
            return v_min
        if min > max:
            raise Exception("min is greater than the max.")
        if value < min:
            return min
        if value > max:
            return max



    NF = nf5  # alias, base format number



if __name__ == "__main__":
    o = {1, 2, 3, 4, 5}
    print(o)
    print(Util.unique_sets(o))
