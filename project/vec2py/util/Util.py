from math import isnan, isinf, pi, floor

class Util:
    DEBUG = True
    ADVANCED = False

    def __init__(self):
        raise ''

    def testFinite(value):
        """
        Throws an error if the argument is not a finite number
        """
        if isinf(value):
            raise ValueError(f"not a finite number {value}")
        
        return value

    def testNumber(value):
        """
        Throws an error if the argument is not a number
        """
        if isnan(value):
            raise ValueError(f"not a number {value}")
        
        return value

    def limitAngle(angle):
        """
        Returns the angle in the range [-pi, +pi]
        """
        if angle > pi:
            N = floor((angle + pi)/(2*pi))
            return angle - 2*pi*N
        
        elif angle < -pi:
            N = floor((-angle + pi)/(2*pi))
            return angle + 2*pi*N
        
        else:
            return angle

    def NFE(num):
        """
        Returns the number formatted as a string with 7 digit exponential notation
        """
        if num is not None:
            return "{:e}".format(num)
        
        else:
            return 'None' if num is None else 'undefined'

    def veryDifferent(arg1, arg2, epsilon = 1E-14, magnitude = 1):
        """
        Returns true if the two arguments are very different
        """
        if isnan(arg1) or isnan(arg2):
            raise 'argument is NaN'
        
        if epsilon <= 0:
            raise f'epsilon must be positive {epsilon}'
        
        if magnitude <= 0:
            raise f'magnitude must be positive {magnitude}'
        
        maxArg = max(abs(arg1), abs(arg2))
        max = maxArg if maxArg > magnitude else magnitude

        return abs(arg1 - arg2) > epsilon*max

    def NF5(num):
        """
        Returns the number formatted as a string with 5 digits of precision
        """
        if num is not None:
            return "{:.5f}".format(num)
        
        else:
            return 'None' if num is None else 'undefined'


    def nf5(num):
        """
        Returns a number formatted for 5 digits of precision with cleaned up trailing zeros
        """
        if num is not None:
            s = Util.NF5(num)
            return s.rstrip('0').rstrip('.') if '.' in s else s
        
        else:
            return 'None' if num is None else 'undefined'

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

    NF = nf5 # alias, base format number

if __name__ == "__main__":
    o = {1, 2, 3, 4, 5}
    print(o)
    print(Util.unique_sets(o))