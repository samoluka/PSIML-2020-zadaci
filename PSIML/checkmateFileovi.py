from PIL import Image
import numpy as np
import glob
import time


def findStart(image, pixelwhite, width, height):
    for j in range(0, width):
        for i in range(0, height):
            if (image[i, j][0] == pixelwhite[0] and image[i, j][1] == pixelwhite[1] and image[i, j][2] == pixelwhite[2]):
                return [i, j]


def findEnd(image, pixelwhite, width, height):
    for j in range(width - 1, -1, -1):
        for i in range(height - 1, -1, -1):
            if (image[i, j][0] == pixelwhite[0] and image[i, j][1] == pixelwhite[1] and image[i, j][2] == pixelwhite[2]):
                return [i + 1, j + 1]


def indexToCord(i, j, a):
    return [i * a, j * a]


def isEmptyTile(table, i, j):
    a = int(len(table) / 8)
    startX, startY = indexToCord(i, j, a)
    for i in range(startX + 1, startX + a):
        for j in range(startY + 1, startY + a):
            if (table[i, j][0] != table[startX, startY][0] or table[i, j][1] != table[startX, startY][1] or table[i, j][2] != table[startX, startY][2]):
                return "ne"
    return "e"


def isSame(a, b):
    l = len(a)
    for i in range(0, l):
        if (a[i] != b[i]):
            return False
    return True


def getMiddle(x):
    sum = 0
    for i in range(0, len(x) - 1):
        sum += x[i]
    sum /= (len(x) - 1)
    return sum


def ok(a, b):
    return a >= 0 and a < 8 and b >= 0 and b < 8


def moveBishop(tabla, x, y):
    moves = []
    a = True
    b = True
    c = True
    d = True
    for i in range(1, 8):
        if (a):
            if (ok(x + i, y + i)):
                if (tabla[x + i][y + i][0] == "e"):
                    moves.append([x + i, y + i])
                else:
                    a = False
                    if (tabla[x + i][y + i][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x + i, y + i])
        if (b):
            if (ok(x - i, y - i)):
                if (tabla[x - i][y - i][0] == "e"):
                    moves.append([x - i, y - i])
                else:
                    b = False
                    if (tabla[x - i][y - i][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x - i, y - i])
        if (c):
            if (ok(x + i, y - i)):
                if (tabla[x + i][y - i][0] == "e"):
                    moves.append([x + i, y - i])
                else:
                    c = False
                    if (tabla[x + i][y - i][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x + i, y - i])
        if (d):
            if (ok(x - i, y + i)):
                if (tabla[x - i][y + i][0] == "e"):
                    moves.append([x - i, y + i])
                else:
                    d = False
                    if (tabla[x - i][y + i][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x - i, y + i])

    return moves


def moveQueen(tabla, x, y):
    movesA = moveBishop(tabla, x, y)
    movesB = moveRook(tabla, x, y)
    return movesA + movesB


def moveKing(tabla, x, y):
    moves = []
    if (ok(x + 1, y + 1)):
        if (tabla[x + 1][y + 1][0] == "e"):
            moves.append([x + 1, y + 1])
        else:
            if (tabla[x + 1][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y + 1])
    if (ok(x + 1, y)):
        if (tabla[x + 1][y][0] == "e"):
            moves.append([x + 1, y])
        else:
            if (tabla[x + 1][y][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y])
    if (ok(x + 1, y - 1)):
        if (tabla[x + 1][y - 1][0] == "e"):
            moves.append([x + 1, y - 1])
        else:
            if (tabla[x + 1][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y - 1])
    if (ok(x, y + 1)):
        if (tabla[x][y + 1][0] == "e"):
            moves.append([x, y + 1])
        else:
            if (tabla[x][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x, y + 1])
    if (ok(x, y - 1)):
        if (tabla[x][y - 1][0] == "e"):
            moves.append([x, y - 1])
        else:
            if (tabla[x][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x, y - 1])
    if (ok(x - 1, y + 1)):
        if (tabla[x - 1][y + 1][0] == "e"):
            moves.append([x - 1, y + 1])
        else:
            if (tabla[x - 1][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y + 1])
    if (ok(x - 1, y)):
        if (tabla[x - 1][y][0] == "e"):
            moves.append([x - 1, y])
        else:
            if (tabla[x - 1][y][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y])
    if (ok(x - 1, y - 1)):
        if (tabla[x - 1][y - 1][0] == "e"):
            moves.append([x - 1, y - 1])
        else:
            if (tabla[x - 1][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y - 1])
    return moves


def moveKnight(tabla, x, y):
    moves = []
    if (ok(x + 2, y + 1)):
        if (tabla[x + 2][y + 1][0] == "e"):
            moves.append([x + 2, y + 1])
        else:
            if (tabla[x + 2][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 2, y + 1])
    if (ok(x - 2, y + 1)):
        if (tabla[x - 2][y + 1][0] == "e"):
            moves.append([x - 2, y + 1])
        else:
            if (tabla[x - 2][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 2, y + 1])
    if (ok(x + 2, y - 1)):
        if (tabla[x + 2][y - 1][0] == "e"):
            moves.append([x + 2, y - 1])
        else:
            if (tabla[x + 2][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 2, y - 1])
    if (ok(x - 2, y - 1)):
        if (tabla[x - 2][y - 1][0] == "e"):
            moves.append([x - 2, y - 1])
        else:
            if (tabla[x - 2][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 2, y - 1])

    if (ok(x + 1, y + 2)):
        if (tabla[x + 1][y + 2][0] == "e"):
            moves.append([x + 1, y + 2])
        else:
            if (tabla[x + 1][y + 2][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y + 2])
    if (ok(x + 1, y - 2)):
        if (tabla[x + 1][y - 2][0] == "e"):
            moves.append([x + 1, y - 2])
        else:
            if (tabla[x + 1][y - 2][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y - 2])
    if (ok(x - 1, y + 2)):
        if (tabla[x - 1][y + 2][0] == "e"):
            moves.append([x - 1, y + 2])
        else:
            if (tabla[x - 1][y + 2][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y + 2])
    if (ok(x - 1, y - 2)):
        if (tabla[x - 1][y - 2][0] == "e"):
            moves.append([x - 1, y - 2])
        else:
            if (tabla[x - 1][y - 2][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y - 2])
    return moves


def movePond(tabla, x, y):
    moves = []
    if (not tabla[x][y][0].islower()):
        if (ok(x - 1, y + 1)):
            if (tabla[x - 1][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y + 1])
        if (ok(x - 1, y)):
            if (tabla[x - 1][y][0] == "e"):
                moves.append([x - 1, y])
        if (ok(x - 1, y - 1)):
            if (tabla[x - 1][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x - 1, y - 1])
        # if (x == 6):
        #     if (ok(x - 2, y)):
        #         if (tabla[x - 2][y][0] == "e"):
        #             moves.append([x - 2, y])
    else:
        if (ok(x + 1, y + 1)):
            if (tabla[x + 1][y + 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y + 1])
        if (ok(x + 1, y)):
            if (tabla[x + 1][y][0] == "e"):
                moves.append([x + 1, y])
        if (ok(x + 1, y - 1)):
            if (tabla[x + 1][y - 1][0].islower() != tabla[x][y][0].islower()):
                moves.append([x + 1, y - 1])
        # if (x == 1):
        #     if (ok(x + 2, y)):
        #         if (tabla[x + 2][y][0] == "e"):
        #             moves.append([x + 2, y])
    return moves


def moveRook(tabla, x, y):
    moves = []
    a = True
    b = True
    c = True
    d = True
    for i in range(1, 8):
        if (a):
            if (ok(x, y + i)):
                if (tabla[x][y + i][0] == "e"):
                    moves.append([x, y + i])
                else:
                    a = False
                    if (tabla[x][y + i][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x, y + i])
        if (b):
            if (ok(x, y - i)):
                if (tabla[x][y - i][0] == "e"):
                    moves.append([x, y - i])
                else:
                    b = False
                    if (tabla[x][y - i][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x, y - i])
        if (c):
            if (ok(x + i, y)):
                if (tabla[x + i][y][0] == "e"):
                    moves.append([x + i, y])
                else:
                    c = False
                    if (tabla[x + i][y][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x + i, y])
        if (d):
            if (ok(x - i, y)):
                if (tabla[x - i][y][0] == "e"):
                    moves.append([x - i, y])
                else:
                    d = False
                    if (tabla[x - i][y][0].islower() != tabla[x][y][0].islower()):
                        moves.append([x - i, y])

    return moves


def calBlacks(arr, i, j, a):
    startX, startY = indexToCord(i, j, a)
    res = []
    tmp1 = []
    for i in range(startX, startX + a):
        count = 0
        for j in range(startY, startY + a):
            if (isSame(arr[i][j], arr[startX, startY])):
                continue
            if (getMiddle(arr[i][j]) < 128):
                count += 1
        tmp1.append(count)
    res.append(tmp1)
    tmp2 = []
    for j in range(startY, startY + a):
        count = 0
        for i in range(startX, startX + a):
            if (isSame(arr[i][j], arr[startX, startY])):
                continue
            if (getMiddle(arr[i][j]) < 128):
                count += 1
        tmp2.append(count)
    res.append(tmp2)
    return res


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getMovesBlack(tabla):
    moves = []
    i = 0
    j = 0
    for x in tabla:
        j = 0
        for f in x:
            if (f[0] == "e"):
                j += 1
                continue
            if (f[0].islower()):
                if (f[0] == "b"):
                    moves += moveBishop(tabla, i, j)
                if (f[0] == "k"):
                    moves += moveKing(tabla, i, j)
                if (f[0] == "n"):
                    moves += moveKnight(tabla, i, j)
                if (f[0] == "q"):
                    moves += moveQueen(tabla, i, j)
                if (f[0] == "p"):
                    moves += movePond(tabla, i, j)
                if (f[0] == "r"):
                    moves += moveRook(tabla, i, j)
            j += 1
        i += 1
    return moves


def checkWhite(tabla):
    moves = getMovesBlack(tabla)
    for move in moves:
        if (len(move) == 0):
            continue
        if (tabla[move[0]][move[1]][0].isupper() and tabla[move[0]][move[1]][0] == "K"):
            return False
    return True


def getMovesWhite(tabla):
    moves = []
    i = 0
    j = 0
    for x in tabla:
        j = 0
        for f in x:
            if (f[0] == "e"):
                j += 1
                continue
            if (f[0].isupper()):
                if (f[0] == "B"):
                    moves += moveBishop(tabla, i, j)
                if (f[0] == "K"):
                    moves += moveKing(tabla, i, j)
                if (f[0] == "N"):
                    moves += moveKnight(tabla, i, j)
                if (f[0] == "Q"):
                    moves += moveQueen(tabla, i, j)
                if (f[0] == "P"):
                    moves += movePond(tabla, i, j)
                if (f[0] == "R"):
                    moves += moveRook(tabla, i, j)
            j += 1
        i += 1
    return moves


def checkBlack(tabla):
    moves = getMovesWhite(tabla)
    for move in moves:
        if (len(move) == 0):
            continue
        if (tabla[move[0]][move[1]][0].islower() and tabla[move[0]][move[1]][0] == "k"):
            return False
    return True


def checkMatBlack(tabla):
    moves = []
    i = 0
    j = 0
    for x in tabla:
        j = 0
        for f in x:
            if (f[0] == "e"):
                j += 1
                continue
            if (f[0].islower()):
                moves = []
                if (f[0] == "b"):
                    moves += moveBishop(tabla, i, j)
                if (f[0] == "k"):
                    moves += moveKing(tabla, i, j)
                if (f[0] == "n"):
                    moves += moveKnight(tabla, i, j)
                if (f[0] == "q"):
                    moves += moveQueen(tabla, i, j)
                if (f[0] == "p"):
                    moves += movePond(tabla, i, j)
                if (f[0] == "r"):
                    moves += moveRook(tabla, i, j)

                for move in moves:
                    kopija = tabla[move[0]][move[1]][0]
                    tabla[move[0]][move[1]][0] = tabla[i][j][0]
                    tabla[i][j][0] = "e"
                    if (checkBlack(tabla)):
                        return "0"
                    tabla[i][j][0] = tabla[move[0]][move[1]][0]
                    tabla[move[0]][move[1]][0] = kopija
            j += 1
        i += 1
    return "1"


def checkMatWhite(tabla):
    moves = []
    i = 0
    j = 0
    for x in tabla:
        j = 0
        for f in x:
            if (f[0] == "e"):
                j += 1
                continue
            if (f[0].isupper()):
                moves = []
                if (f[0] == "B"):
                    moves += moveBishop(tabla, i, j)
                if (f[0] == "K"):
                    moves += moveKing(tabla, i, j)
                if (f[0] == "N"):
                    moves += moveKnight(tabla, i, j)
                if (f[0] == "Q"):
                    moves += moveQueen(tabla, i, j)
                if (f[0] == "P"):
                    moves += movePond(tabla, i, j)
                if (f[0] == "R"):
                    moves += moveRook(tabla, i, j)

                for move in moves:
                    kopija = tabla[move[0]][move[1]][0]
                    tabla[move[0]][move[1]][0] = tabla[i][j][0]
                    tabla[i][j][0] = "e"
                    if (checkWhite(tabla)):
                        return "0"
                    tabla[i][j][0] = tabla[move[0]][move[1]][0]
                    tabla[move[0]][move[1]][0] = kopija
            j += 1
        i += 1
    return "1"


if __name__ == "__main__":
    gresaka = 0
    for p in range(0,54):
        print(p)
        tic = time.perf_counter()
        pathBig = "dataCheckmate\private\set\/{}/{}.png".format(p, p)
        pathWhite = "dataCheckmate\private\set/{}/tiles\white.png".format(p)
        pathFigure = "dataCheckmate\private\set\/{}\pieces".format(p)
        pathBlack = "dataCheckmate\private\set/{}/tiles\/black.png".format(p)
        pathout = "dataCheckmate\private\outputs/{}.txt".format(p)

        out = open(pathout)
        big = Image.open(pathBig)
        white = Image.open(pathWhite)
        image = np.array(big)
        whiteimage = np.array(white)
        pixelwhite = whiteimage[0, 0]
        width, height = big.size

        [a, b] = findStart(image, pixelwhite, width, height)
        [c, d] = findEnd(image, pixelwhite, width, height)

        dict2 = {
            0: "b",
            1: "k",
            2: "n",
            3: "p",
            4: "q",
            5: "r",
            6: "B",
            7: "K",
            8: "N",
            9: "P",
            10: "Q",
            11: "R"
        }

        rs = "{},{}".format(a, b)
        good = out.readline()[:-1]
        if (rs != good):
            print(f"{bcolors.WARNING}GRESKAA{bcolors.ENDC}")
            gresaka += 1
        print(rs, good)

        newImage = big.crop((b, a, d, c))
        width, height = newImage.size
        length = int(width / 8)
        newarr = np.array(newImage)

        FigureFiles = glob.glob(pathFigure + "/**/*.png", recursive=True)

        figures = []
        ind = 0;

        for figure in FigureFiles:
            size = (length, length)
            image = Image.open(figure).resize(size).convert("RGBA")
            img = Image.new("RGBA", image.size, "WHITE")  # Create a white rgba background
            img.paste(image, (0, 0), image)
            figureArray = np.array(img)
            figures.append([figure, calBlacks(figureArray, 0, 0, length)])
            ind += 1

        tabla = []
        color = "w"
        for i in range(0, 8):
            red = []
            for j in range(0, 8):
                cur = [isEmptyTile(newarr, i, j), color]
                color = "w" * (color == "b") + "b" * (color == "w")
                if (cur[0] == "ne"):
                    findex = 0
                    min = 1000000000
                    code = -1
                    for f in figures:
                        fscore = calBlacks(newarr, i, j, length)
                        s = 0
                        for xx, yy in zip(fscore[0], f[1][0]):
                            s += abs(xx - yy)
                        for xx, yy in zip(fscore[1], f[1][1]):
                            s += abs(xx - yy)
                        if (s < min):
                            min = s
                            code = findex
                        findex += 1
                    cur[0] = dict2[code]
                red.append(cur)
            color = "w" * (color == "b") + "b" * (color == "w")
            tabla.append(red)

        rs = ""
        for x in tabla:
            s = ""
            i = 0
            for p in x:
                if (p[0] != "e"):
                    if (i != 0):
                        s += "{}".format(i)
                    s += p[0]
                    i = 0
                else:
                    i += 1
            if (i != 0):
                s += "{}".format(i)
            rs += s + "/"
        rs = rs[:-1]
        good = out.readline()[:-1]
        if (rs != good):
            print(f"{bcolors.WARNING}GRESKA{bcolors.ENDC}")
            gresaka += 1
        print(rs, good)
        B = checkWhite(tabla)
        W = checkBlack(tabla)
        # print(B)
        # print(W)
        res = "-"
        if (not B or not W):
            res = "W" * (W == False) + "B" * (B == False)
        if (res == "-"):
            cm = "0"
        else:
            if (W == False):
                cm = checkMatBlack(tabla)
            else:
                cm = checkMatWhite(tabla)
        # print(checkMatBlack(tabla))
        # print(checkMatWhite(tabla))
        good = out.readline()[:-1]
        if (res != good):
            print(f"{bcolors.WARNING}GRESKA{bcolors.ENDC}")
            gresaka += 1
        print(res, good)
        good = out.readline()[:-1]
        if (cm != good):
            print(f"{bcolors.WARNING}GRESKA{bcolors.ENDC}")
            gresaka += 1
        print(cm, good)
        toc = time.perf_counter()
        print(f"Reseno za {toc - tic:0.4f} seconds")
    print(gresaka)
