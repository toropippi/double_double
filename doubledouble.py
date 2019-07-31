#double-double演算を行う関数
import numpy as np

class dd:#≒構造体として使用
    def __init__(self,x,y):
        self.hi = np.float64(x)
        self.lo = np.float64(y)

# dd a
def twosum(a):
    x = a.hi + a.lo
    tmp= x - a.hi
    y = (a.hi - (x - tmp)) + (a.lo - tmp)
    return dd(x, y)

# double a
def dsplit(a):
    tmp = a * 134217729.0#2^27+1
    x = tmp - (tmp - a)
    y = a - x
    return dd(x, y)

# dd a
def twoproduct(a):
    x = a.hi * a.lo
    ca = dsplit(a.hi)
    cb = dsplit(a.lo)
    y = (((ca.hi * cb.hi - x) + ca.lo * cb.hi) + ca.hi * cb.lo) + ca.lo * cb.lo
    return dd(x, y)

#dd x,dd y
def dd_add(x,y):
    cz = twosum(dd(x.hi, y.hi))
    cz.lo = cz.lo + x.lo + y.lo
    return twosum(cz)

#dd x,dd y
def dd_sub(x,y):
    cz = twosum(dd(x.hi, -y.hi))
    cz.lo = cz.lo + x.lo - y.lo
    return twosum(cz)

# dd x,dd y
def dd_mul(x,y):
    cz = twoproduct(dd(x.hi, y.hi))
    cz.lo = cz.lo + x.hi * y.lo + x.lo * y.hi + x.lo * y.lo
    return twosum(cz)

# dd x
def dd_pow2(x):
    xx = x.hi * x.hi
    ca = dsplit(x.hi)
    s1 = ca.lo * ca.hi
    y = ((ca.hi * ca.hi - xx) + s1 + s1) + ca.lo * ca.lo
    s1 = x.hi * x.lo
    y = y + (s1 + s1)
    return twosum(dd(xx,y))

# dd x ,double y
def dn_mul(x,y):
    cz = twoproduct(dd(x.hi, y))
    cz.lo = cz.lo + x.lo * y
    return twosum(cz)

# dd x ,dd y
def dd_div(x,y):
    z1 = x.hi / y.hi
    cz = twoproduct(dd(-z1, y.hi))
    z2 = ((((cz.hi + x.hi) - z1 * y.lo) + x.lo) + cz.lo) / y.hi
    return twosum(dd(z1, z2))

# dd x
def dd_sqrt(x):
    if (x.hi == 0.0) & (x.lo == 0.0):
        return dd(0, 0)
    else:
        z1 = np.sqrt(x.hi)
        cz = twoproduct(dd(-z1, z1))
        z2 = ((cz.hi + x.hi) + x.lo + cz.lo) / (2.0 * z1)
        return twosum(dd(z1, z2))



if __name__ == '__main__':
    dda=dd(1,0)
    for i in range(53):
        dda = dd_mul(dda, dd(2,0))#dd型で2の53乗を作る
    print(dda.hi, dda.lo)
    print()

    #dd型の9007199254740992に1を足していくループ。double型なら仮数部桁落ちでこれ以上増えないはず
    for i in range(10):
        dda = dd_add(dda, dd(1,0))
        print(dda.hi,dda.lo)