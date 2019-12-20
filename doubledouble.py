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

# dd x : pow(x,2)
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

# dd x,int y:xのpow(2,y)乗、yはべき指数であることに注意。y=0ならx,y=1ならxの2乗,y=-1ならyの平方根が出力
def dd_powxpow2y(x,y):
    xx = dd(x.hi,x.lo)
    if y>=0:
        for i in range(y):
            xx=dd_pow2(xx)
    else:
        for i in range(-y):
            xx=dd_sqrt(xx)
    return xx

#dd x,dd y
def dd_pow(x,y):
    yy = dd(y.hi,y.lo)
    ans = dd(1.0, 0.0)
    hisign = True
    losign = True
    if y.hi<0.0:
        yy.hi = -yy.hi
        hisign = False
    if y.lo<0.0:
        yy.lo = -yy.lo
        losign = False
    if yy.hi==0.0:#0乗
        return ans
    #ここでyyの仮数部のbitを取得したい
    #まずyyを1含む～2含まずの範囲にscaleする、ここは仮数部をいじらない操作となる
    scalee=0
    if yy.hi>=1.0:
        scalee=1024
        for i in range(1024):
            if yy.hi>=2.0:
                yy.hi=yy.hi*0.5
                yy.lo=yy.lo*0.5
            else:
                scalee = i
                break
        #これでscaleが求まった
    else:#y.hi<1.0のとき
        scalee=-1024
        for i in range(1024):
            if yy.hi<1.0:
                yy.hi=yy.hi*2.0
                yy.lo=yy.lo*2.0
            else:
                scalee = -i
                break
        #これでscaleが求まった
    if scalee==-1024:
        return ans
    #この時点でyyは必ず1～2の範囲内にある(inf例外あり)
    #ここから、何のくらいの桁がbitがたっているかを検出、リストに保存。ここでscale値正と負を分ける
    pbitlisthi = []  # 中身は正のscalee値 hi
    mbitlisthi = []  # 中身は負のscalee値 hi
    pbitlistlo = []  # 中身は正のscalee値 lo
    mbitlistlo = []  # 中身は負のscalee値 lo

    for i in range(53):
        if yy.hi>=1.0:
            if scalee>=0:
                pbitlisthi.append(scalee)
            else:
                mbitlisthi.append(scalee)
            yy.hi-=1.0
        yy.hi *= 2.0
        yy.lo *= 2.0
        scalee-=1
    #次にloのことを考える
    for i in range(2048):#擬似四倍精度特有の異常高精度を考慮し54ではなく2048
        if yy.lo>=1.0:
            if scalee>=0:
                pbitlistlo.append(scalee)
            else:
                mbitlistlo.append(scalee)
            yy.lo-=1.0
        elif yy.lo==0.0:
            break
        yy.lo *= 2.0
        scalee-=1
    #ここで全部のビットとその符号が求まった。負の場合は逆数にしないといけない
    #まずは小数点より上の指数を
    pbitlistlo=pbitlistlo[::-1]
    pbitlisthi=pbitlisthi[::-1]
    #まずloから
    mysc=0
    lo_ans=dd(1.0, 0.0)
    xp = dd(x.hi, x.lo)
    for sc in pbitlistlo:
        for i in range(sc-mysc):
            xp=dd_pow2(xp)
        lo_ans=dd_mul(lo_ans,xp)
        mysc=sc
    #次にhi
    hi_ans=dd(1.0, 0.0)
    for sc in pbitlisthi:
        for i in range(sc-mysc):
            xp=dd_pow2(xp)
        hi_ans=dd_mul(hi_ans,xp)
        mysc=sc

    #次に小数点以下の指数を
    #まずhi
    xp = dd(x.hi, x.lo)
    mysc=0
    for sc in mbitlisthi:
        for i in range(mysc-sc):
            xp=dd_sqrt(xp)
        hi_ans=dd_mul(hi_ans,xp)
        mysc=sc
    #次にlo
    for sc in mbitlistlo:
        for i in range(mysc-sc):
            xp=dd_sqrt(xp)
        lo_ans=dd_mul(lo_ans,xp)
        mysc=sc

    #最後に指数の符号を考慮しans
    if losign:
        if hisign:#++
            ans = dd_mul(hi_ans, lo_ans)
        else:#-+
            ans = dd_div(lo_ans, hi_ans)
    else:#+-
        if hisign:
            ans = dd_div(hi_ans, lo_ans)
        else:#--
            ans = dd_div(ans, dd_mul(hi_ans,lo_ans))
    return ans





if __name__ == '__main__':

    dda=dd(2,0)
    dda=dd_pow(dda,dd(53,0))
    #for i in range(53):
    #    dda = dd_mul(dda, dd(2,0))#dd型で2の53乗を作る
    print("2の53乗のdd型の中身")
    print(dda.hi, dda.lo)


    #dd型の9007199254740992に1を足していくループ。double型なら情報落ちでこれ以上増えないはず
    print()
    print("1ずつ足していく")
    for i in range(10):
        dda = dd_add(dda, dd(1,0))
        print(dda.hi,dda.lo)
