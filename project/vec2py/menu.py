def precache(self, bounds):
        nb = self.get_nb_nodes() // 4
        for _ in range(4):
            self.PRE_CACHED_BOUNDS[_ * nb] = bounds.quadrant(_)
        print(self.PRE_CACHED_BOUNDS)

{
    0:{
        1:{2:{}, 3:{}, 4:{}, 5:{}},
        6:{7:{}, 8:{}, 9:{}, 10:{}},
        11:{12:{}, 13:{}, 14:{}, 15:{}},
        16:{17:{}, 18:{}, 19:{}, 20:{}}},
    21:{
        22:{23:{}, 24:{}, 25:{}, 26:{}},
        27:{28:{}, 29:{}, 30:{}, 31:{}},
        32:{33:{}, 34:{}, 35:{}, 36:{}},
        37:{38:{}, 39:{}, 40:{}, 41:{}}},
    42:{
        43:{44:{}, 45:{}, 46:{}, 47:{}},
        48:{49:{}, 50:{}, 51:{}, 52:{}},
        53:{54:{}, 55:{}, 56:{}, 57:{}},
        58:{59:{}, 60:{}, 61:{}, 62:{}}},
    63:{
        64:{65:{}, 66:{}, 67:{}, 68:{}},
        69:{70:{}, 71:{}, 72:{}, 73:{}},
        74:{75:{}, 76:{}, 77:{}, 78:{}},
        79:{80:{}, 81:{}, 82:{}, 83:{}}}
}

class feur:
    def __init__(self, name):
          self.name = name
    def quadrant(self, quadrant, up):
        match quadrant:
            case 0:
                return feur(up)
            case 1:
                return feur(up)
            case 2:
                return feur(up)
            case 3:
                return feur(up)
                  
    def __repr__(self):
        return f"{self.name}"


P = 3
N = (((4**(P+1))-1) / 3) # 85
_PRE_CACHED_BOUNDS = {}

def prec(l, upper=None):
    l = int((l-1)//4)
    if l >= 1:
        if upper is None:
             bounds = feur("ROOT")
        else:
            bounds = _PRE_CACHED_BOUNDS[upper]

        for _ in range(4):
            if upper is None:
                next_upper = _*l
            else:
                next_upper = (upper+1) + _*l
            _PRE_CACHED_BOUNDS[next_upper] = bounds.quadrant(_, next_upper)
            print(next_upper, l)
            prec(l, next_upper)



#21.0
#5.0
#1.0

    #0  0
    #21 1
    #42 2
    #63 3


#_PRE_CACHED_BOUNDS[(_*(P/4))+1] = _PRE_CACHED_BOUNDS[_*(P/4) + _*(((P/4)-1)/4)].quadrant(_)
if __name__ == '__main__':
    prec(N)
    print(_PRE_CACHED_BOUNDS)
#1 0 0
#
