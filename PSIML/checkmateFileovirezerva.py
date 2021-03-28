from sys import path

from PIL import Image
import numpy as np
import glob


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


def calBlacksTable(arr, k, l, a):
    startX, startY = indexToCord(k, l, a)
    res = []
    tmp1 = []
    for i in range(startX, startX + a):
        count = 0
        for j in range(startY, startY + a):
            if (isSame(arr[i][j], arr[startX][startY])):
                continue
            if ((int(arr[i][j][0]) + int(arr[i][j][1]) + int(arr[i][j][2])) / 3 < 128):
                count += 1
        tmp1.append(count)
    res.append(tmp1)
    tmp2 = []
    for j in range(startY, startY + a):
        count = 0
        for i in range(startX, startX + a):
            if (isSame(arr[i][j], arr[startX][startY])):
                continue
            if ((int(arr[i][j][0]) + int(arr[i][j][1]) + int(arr[i][j][2])) / 3 < 128):
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


gresaka = 0
for p in range(0, 26):

    pathBig = "dataCheckmate\public\set\/{}/{}.png".format(p, p)
    pathWhite = "dataCheckmate\public\set/{}/tiles\white.png".format(p)
    pathFigure = "dataCheckmate\public\set\/{}\pieces".format(p)
    pathBlack = "dataCheckmate\public\set/{}/tiles\/black.png".format(p)
    pathout = "dataCheckmate\public\outputs/{}.txt".format(p)

    out = open(pathout)
    big = Image.open(pathBig)
    white = Image.open(pathWhite)
    image = np.array(big)
    whiteimage = np.array(white)
    pixelwhite = whiteimage[0, 0]
    pixelBlack = np.array(Image.open(pathBlack))[0, 0]
    # print(pixelBlack)
    width, height = big.size
    # print(pixelwhite)
    [a, b] = findStart(image, pixelwhite, width, height)
    [c, d] = findEnd(image, pixelwhite, width, height)

    dict = {
        0: "bBishop",
        1: "bKing",
        2: "bKnight",
        3: "bPawn",
        4: "bQueen",
        5: "bRook",
        6: "wBishop",
        7: "wKing",
        8: "wKnight",
        9: "wPawn",
        10: "wQueen",
        11: "wRook"
    }
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
    # newImage.show()
    width, height = newImage.size
    newarr = np.array(newImage)

    # for x in range(0, width):
    #     for j in range(0, height):
    #         if isSame(newarr[x, j], pixelBlack):
    #             newarr[x, j] = [240, 217, 183]

    # newImage = Image.fromarray(newarr, "RGB")
    # newImage.show()
    # newImgae = newImage.convert("LA")
    # newImage.show()
    # newarr = np.array(newImage)
    FigureFiles = glob.glob(pathFigure + "/**/*.png", recursive=True)

    figures = []
    ind = 0;

    for figure in FigureFiles:
        # img = Image.open(figure)
        size = (int(width / 8), int(height / 8))
        image = Image.open(figure).resize(size).convert("RGBA")
        img = Image.new("RGBA", image.size, "WHITE")  # Create a white rgba background
        img.paste(image, (0, 0), image)
        # size = img.size
        # size = (int(width / 8), int(height / 8))
        # img = img.resize(size)
        figureArray = np.array(img)
        # if (len(figureArray[0][0]) == 4):
        #     for x in range(0, size[0]):
        #         for j in range(0, size[0]):
        #             if (figureArray[x, j][3] == 0):
        #                 figureArray[x, j] = [255, 255, 255, 255]
        #             figureArray[x, j][0] = (int(figureArray[x, j][0]) + int(figureArray[x, j][1]) + int(figureArray[x, j][2])) / 3
        #     img = Image.fromarray(figureArray, "RGBA")
        # if (len(figureArray[0][0]) == 2):
        #     for x in range(0, size[0]):
        #         for j in range(0, size[0]):
        #             if (figureArray[x, j][1] == 0):
        #                 figureArray[x, j] = 255
        #     img = Image.fromarray(figureArray, "LA")
        # size = (int(width / 8), int(height / 8))
        # img = img.resize(size)
        # img.show()
        # figureArray = np.array(img)
        # img.show()
        figures.append([figure, calBlacks(figureArray, 0, 0, 30)])
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
                min = 100000
                code = -1
                for f in figures:
                    fscore = calBlacks(newarr, i, j, 30)
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
                # print(ffscore)
            red.append(cur)
        color = "w" * (color == "b") + "b" * (color == "w")
        # print(red)
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
print(gresaka)
