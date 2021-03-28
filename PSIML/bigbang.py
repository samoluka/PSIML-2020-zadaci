import math
import numpy as np


class particle:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.numOfCollisions = 0


def callwalls(par, time, s):
    res = 0
    npx = math.fabs(par.px + time * par.vx)
    npy = math.fabs(par.py + time * par.vy)
    if (npx > s):
        res += 1
        res += math.floor((npx - s) / (2 * s))
    if (npy > s):
        res += 1
        res += math.floor((npy - s) / (2 * s))
    return res


def bigbang():
    n, s, t, p = input().split(" ")
    n = int(n)
    s = int(s)
    t = int(t)
    p = float(p)
    l = []
    times = []
    k = 0
    for i in range(0, int(n)):
        px, py, vx, vy = input().split(" ")
        px = float(px)
        py = float(py)
        vx = float(vx)
        vy = float(vy)
        l.append(particle(px, py, vx, vy))
        times.append(math.fabs(px / vx))
        times.append(math.fabs(py / vy))
    time = np.median(times)
    time = np.round(time)
    walls = 0
    numOfParticles = 0
    for par in l:
        par.numOfCollisions = callwalls(par, t, s)
        walls += par.numOfCollisions
        numOfParticles += p ** par.numOfCollisions

    # numOfParticles = round(numOfParticles,5)
    return [int(time), walls, numOfParticles]


if __name__ == "__main__":
    res = bigbang()
    print(res[0], res[1], res[2])
