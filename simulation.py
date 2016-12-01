import pickle
import random
import time
from math import *


trainingFile = open('training.sql', 'w')
APs = list()
Devices = list()
Depos = list()
Heads = list()
Tails = list()
WallsBet = dict()  # (classID, APid) ==> wallsNum
Distance = dict()  # (classID, APid) ==> distance between
Ssi = dict()  # (classID, APid) ==> Ssi
classNum = 0
wallNum = 0
deviceNum = 0
positionID = 1  # table key, auto increase
deviceID = 1  # table key, auto increase

WALLFACTOR = 10
UPLOADGAP = 240  # seconds
HALFGAP = 120  # half of UPLOADGAP
NOICEFACTOR = 4


class Point:
    x = 0
    y = 0
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
    def distance2(self, p2):
        a = self.x - p2.x
        b = self.y = p2.y
        return sqrt(hypot(a, b))


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
            # update WallsBetween
            for w in range(0, wallNum):
                aa = Point(Heads[w][0], Heads[w][1])
                bb = Point(Tails[w][0], Tails[w][1])
                if intersect3(aa, bb, cc, dd):
                    tmp = WallsBet[(i, j)]
                    tmp += 1
                    WallsBet[(i,j)] = tmp
            # compute distance
            Distance[(i,j)] = cc.distance2(dd)

def computeSsi():
    for i in range(0, classNum):
        for j in range(0, deviceNum):
            tup = (i,j)
            ssi = -30 - 30*log10( Distance[tup]) + 1/sqrt(8*pi)*exp(-pow(Distance[tup], 2)) - WALLFACTOR * WallsBet[tup];
            Ssi[tup] = int(ssi)


def generateTraining(k):
    currentT = time.time()  # use for upload position
    global positionID,deviceID
    # random = random.randint(12,20)
    for t in range(0, k):
        currentT += UPLOADGAP
        for j in range(0, deviceNum):
            # insert to position
            trainingFile.write('INSERT INTO trainer_position VALUES (' + str(positionID) + ',\"00:00:00:00:00:00\",' + str(currentT) + ',' + str(Depos[j]) + ',0);\n')
            positionID += 1
            trainingFile.write('INSERT INTO trainer_device VALUES ')
            for i in range(0, classNum):
                timeVar = random.randint(-HALFGAP, HALFGAP)
                noice = random.randint(-NOICEFACTOR, NOICEFACTOR)
                ssi = Ssi[(i,j)] + noice
                if ssi < -150:
                    ssi = -150
                upTime = currentT + timeVar
                if i == classNum-1:
                    trainingFile.write('(' + str(deviceID) + ', \"00:00:00:00:00:00\",' + str(ssi) + ',' + str(upTime) + ',' + str(i+1) + ');\n')
                else:
                    trainingFile.write('(' + str(deviceID) + ', \"00:00:00:00:00:00\",' + str(ssi) + ',' + str(upTime) + ',' + str(i+1) + '),')
                deviceID += 1


def main():
    readPosition()
    wallBlock()
    computeSsi()
    generateTraining(10)
    #print WallsBet
    #print Distance
    #print Ssi


if __name__ == "__main__":
    main()
