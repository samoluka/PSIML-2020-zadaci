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
    t = time
    npx = math.fabs(par.px + t * par.vx)
    npy = math.fabs(par.py + t * par.vy)

    if (npx > s):
        res += 1
        res += math.floor((npx - s) / (2 * s))
    if (npy > s):
        res += 1
        res += math.floor((npy - s) / (2 * s))
    # while (t > 0):
    #     dtx = math.fabs((np.sign(par.vx) * s - par.px) / par.vx)
    #     dty = math.fabs((np.sign(par.vy) * s - par.py) / par.vy)
    #     dt = min(dtx, dty)
    #     npx = par.px + par.vx * dt
    #     npy = par.py + par.vy * dt
    #     t = t - dt
    #     if (t <= 0):
    #         break
    #     par.px = npx
    #     par.py = npy
    #     if (math.fabs(npx) >= s):
    #         res += 1
    #         par.vx = -par.vx
    #         if (npx > 0):
    #             par.px = s
    #         else:
    #             par.px = -s
    #     if (math.fabs(npy) >= s):
    #         res += 1
    #         par.vy = -par.vy
    #         if (npy > 0):
    #             par.py = s
    #         else:
    #             par.py = -s
    return res


def bigbang(path, ind):
    with open(path) as f:
        n, s, t, p = [float(x) for x in next(f).split()]
        l = []
        times = []
        k = 0
        for i in range(0, int(n)):
            px, py, vx, vy = [float(x) for x in next(f).split()]
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
        with open("results/res{:02d}.txt".format(ind), "w+") as f:
            f.write("{} {} {}".format(int(time), walls, numOfParticles))
            f.close()
        return [int(time), walls, numOfParticles]


if __name__ == "__main__":
    for i in range(0, 10):
        res = bigbang("data/private/inputs/{:d}.txt".format(i), i)
        with open("data/private/outputs/{:d}.txt".format(i)) as out:
            a, b, c = [float(x) for x in next(out).split()]
            print("{} {} {} {}\n".format(i, res[0] - a, res[1] - b, res[2] - c))
