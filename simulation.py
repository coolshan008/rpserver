import pickle
import string
import random
import time
from math import *


trainingFile = open('training.sql', 'w')
testingFile = open('testing.sql', 'w')
APs = list()
Devices = list()
Macs = list()
Depos = list()
Heads = list()
Tails = list()
WallsBet = dict()  # (classID, APid) ==> wallsNum
Distance = dict()  # (classID, APid) ==> distance between
Ssi = dict()  # (classID, APid) ==> Ssi
classNum = 0
wallNum = 0
deviceNum = 0
positionID = 1000  # table key, auto increase
deviceID = 1  # table key, auto increase

WALLFACTOR = 5
UPLOADGAP = 130# seconds
HALFGAP = 90# half of UPLOADGAP
NOICEFACTOR = 2


class Point:
    x = 0
    y = 0
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
    def distance2(self, p2):
        a = self.x - p2.x
        b = self.y - p2.y
        re = sqrt(hypot(a, b))
        #print (str(a) + ' '+ str(b ) + ' '+ str(re))
        if re == 0:
            return 1
        return re


def readPosition():
    #file = open('pos.setting', 'r')
    file = open('pos1.setting', 'r')
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
        Macs.append(string.join(random.sample('1234567890abcdef:',16)).replace(" ",""))



def determinant(v1, v2, v3, v4):
    return v1*v4 - v2*v3

def max(a,b):
    if a > b:
        return a
    return b

def min(a,b):
    if(a<b):
        return a
    return b

def quickOut(P1, P2, Q1, Q2):
    if min(P1.x, P2.x) <= max(Q1.x, Q2.x) and min(Q1.x, Q2.x)<=max(P1.x, P2.x)\
       and min(P1.y, P2.y) <= max(Q1.y, Q2.y) and min(Q1.y, Q2.y) <= \
       max(P1.y, P2.y):
        return True
    return False

def isLineSegmentCross(P1, P2, Q1, Q2):
    if ((Q1.x-P1.x)*(Q1.y-Q2.y)-(Q1.y-P1.y)*( Q1.x-Q2.x)) * ((Q1.x-P2.x)*(Q1.y-Q2.y)-(Q1.y-P2.y)*(Q1.x-Q2.x)) < 0 or ((P1.x-Q1.x)*(P1.y-P2.y)-(P1.y-Q1.y)*(P1.x-P2.x)) * ((P1.x-Q2.x)*(P1.y-P2.y)-(P1.y-Q2.y)*( P1.x-P2.x)) < 0: 
        return True
    else:
        return False

'''
    Judge sector(aa,bb) and sector(cc,dd) is interface
'''
def intersect3(aa, bb, cc, dd):
    '''delta = determinant(bb.x - aa.x, cc.x- dd.x, bb.y - aa.y, cc.y - dd.y)
    if delta <= 1e-6 and delta >= -1e-6:
        return False
    nameda = determinant(cc.x - aa.x, cc.x - dd.x, cc.y - aa.y, cc.y - dd.y) / delta
    if nameda > 1 or nameda < 0:
        return False
    miu = determinant(bb.x - aa.x, cc.x - aa.x, bb.y - aa.y, cc.y - aa.y) / delta
    if miu > 1 or miu < 0:
        return False
    return True'''
    if quickOut(aa, bb, cc, dd):
        if isLineSegmentCross(aa, bb, cc, dd):
            return True
    return False

zeros = 0

def wallBlock():
    global zeros
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
            if WallsBet[(i,j)] == 0:
                zeros += 1
            Distance[(i,j)] = cc.distance2(dd)
            #print (str((i,j)) + ' ' + str(Distance[(i,j)]))

def computeSsi():
    for i in range(0, classNum):
        for j in range(0, deviceNum):
            tup = (i,j)
            #ssi = -30 - 30*log10( Distance[tup]) + 1/sqrt(8*pi)*exp(-pow(Distance[tup], 2)) - WALLFACTOR * WallsBet[tup];
            ssi = -35 - 35*log10( Distance[tup]) + 1/sqrt(8*pi)*exp(-pow(Distance[tup], 2)) - WALLFACTOR * WallsBet[tup];
            #print (str(tup) + ': ' + str(ssi) )
            Ssi[tup] = int(ssi)


def generateTraining(k):
    currentT = time.time()  # use for upload position
    global positionID,deviceID
    # random = random.randint(12,20)
    for t in range(0, k):
        currentT += UPLOADGAP
        for j in range(0, deviceNum):
            # insert to position
            trainingFile.write('INSERT INTO trainer_position VALUES (' + str(positionID) + ',\"' + Macs[j] + '\",' + str(currentT) + ',' + str(Depos[j]) + ',0);\n')
            positionID += 1
            trainingFile.write('INSERT INTO trainer_device VALUES ')
            for i in range(0, classNum):
                #timeVar = random.randint(-HALFGAP, HALFGAP)
                timeVar = random.randint(-UPLOADGAP, 0)
                noice = random.randint(-NOICEFACTOR, NOICEFACTOR)
                ssi = Ssi[(i,j)] + noice
                if ssi < -110:  # threshold can be modified
                    ssi = -150
                upTime = currentT + timeVar
                if i == classNum-1:
                    trainingFile.write('(' + str(deviceID) + ', \"' + Macs[j] + '\",' + str(ssi) + ',' + str(upTime) + ',' + str(i) + ');\n')
                else:
                    trainingFile.write('(' + str(deviceID) + ', \"' + Macs[j] + '\",' + str(ssi) + ',' + str(upTime) + ',' + str(i) + '),')
                deviceID += 1


# is wrong with mac
def generateTesting(k):
    currentT = time.time()  # use for upload position
    global positionID,deviceID
    # random = random.randint(12,20)
    for t in range(0, k):
        currentT += UPLOADGAP
        for j in range(0, deviceNum):
            # insert to position
            testingFile.write('INSERT INTO trainer_position VALUES (' + str(positionID) + ',\"00:00:00:00:00:00\",' + str(currentT) + ',' + str(Depos[j]) + ',0);\n')
            positionID += 1
            testingFile.write('INSERT INTO trainer_device VALUES ')
            for i in range(0, classNum):
                #timeVar = random.randint(-HALFGAP, HALFGAP)
                timeVar = random.randint(-UPLOADGAP, 0)
                noice = random.randint(-NOICEFACTOR, NOICEFACTOR)
                ssi = Ssi[(i,j)] + noice
                if ssi < -100:  # threshold can be modified
                    ssi = -150
                elif WallsBet[(i,j)] >=4:
                    ssi = -150
                upTime = currentT + timeVar
                if i == classNum-1:
                    testingFile.write('(' + str(deviceID) + ', \"00:00:00:00:00:00\",' + str(ssi) + ',' + str(upTime) + ',' + str(i) + ');\n')
                else:
                    testingFile.write('(' + str(deviceID) + ', \"00:00:00:00:00:00\",' + str(ssi) + ',' + str(upTime) + ',' + str(i) + '),')
                deviceID += 1



def main():
    readPosition()
    wallBlock()
    computeSsi()
    generateTraining(5)
    #print WallsBet
    #print zeros
    #generateTesting(1)


if __name__ == "__main__":
    main()
