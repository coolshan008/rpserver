import pickle
import math

APs = list()
Devices = list()
Depos = list()
Heads = list()
Tails = list()
WallsBet = dict()  # (classID, APid) ==> wallsNum
classNum = 0
wallNum = 0
deviceNum = 0

class Point:
    x = 0
    y = 0
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy


def readPosition():
    file = open('pos.setting', 'r')
    global classNum, wallNum, deviceNum
    classNum = int(file.readline().strip())
    for i in range(0,classNum):
        line = file.readline()
        splits = line.strip().split(' ')
        pos = (int(splits[0]), int(splits[1]))
        APs.append(pos)
    wallNum = int(file.readline().strip())
    for i in range(0, wallNum):
        line = file.readline()
        splits = line.strip().split(' ')
        pos = (int(splits[0]), int(splits[1]))
        Heads.append(pos)
        pos = (int(splits[2]), int(splits[3]))
        Tails.append(pos)
    deviceNum = int(file.readline().strip())
    for i in range(0, deviceNum):
        line = file.readline()
        splits = line.strip().split(' ')
        pos = (int(splits[0]), int(splits[1]))
        Devices.append(pos)
        Depos.append(int(splits[2]))



def determinant(v1, v2, v3, v4):
    return v1*v4 - v2*v3

'''
    Judge sector(aa,bb) and sector(cc,dd) is interface
'''
def intersect3(aa, bb, cc, dd):
    delta = determinant(bb.x - aa.x, cc.x- dd.x, bb.y - aa.y, cc.y - dd.y)
    if delta <= 1e-6 and delta >= -1e-6:
        return False
    nameda = determinant(cc.x - aa.x, cc.x - dd.x, cc.y - aa.y, cc.y - dd.y) / delta
    if nameda > 1 or nameda < 0:
        return False
    miu = determinant(bb.x - aa.x, cc.x - aa.x, bb.y - aa.y, cc.y - aa.y) / delta
    if miu > 1 or miu < 0:
        return False
    return True


def wallBlock():
    for i in range(0, classNum):
        cc = Point(APs[i][0], APs[i][1])
        for j in range(0, deviceNum):
            dd = Point(Devices[j][0], Devices[j][1])
            WallsBet[(i,j)] = 0
            for w in range(0, wallNum):
                aa = Point(Heads[w][0], Heads[w][1])
                bb = Point(Tails[w][0], Tails[w][1])
                if intersect3(aa, bb, cc, dd):
                    tmp = WallsBet[(i, j)]
                    tmp += 1
                    WallsBet[(i,j)] = tmp


def main():
    readPosition()
    wallBlock()
    print WallsBet


if __name__ == "__main__":
    main()
