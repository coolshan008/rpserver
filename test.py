from math import *
import pickle
import random
import pdb
import gl

tuples = list()
NOINUM = 10
NOICEFACTOR = 3


class MyTuple:
    Correct_no = -1
    ssi_array = list()
    def __init__(self, no, ssis):
        self.Correct_no = no
        self.ssi_array = ssis


def readTuples():
    open_file = open('device.txt', 'r')
    current_no = -1
    current_ssi = dict()
    for line in open_file:
        if line.isspace():
            ssiL = list()
            for i in range(0, gl.NUMBER_OF_PIS):
                if current_ssi.has_key(i):
                    ssiL.append(current_ssi[i])
                else:
                    ssiL.append(-150)
            tuples.append(MyTuple(current_no, ssiL))
            current_ssi.clear()
            continue
        if line.strip().endswith(':'):
            current_no = int(line.split(':')[0])
            continue
        line = line.strip()
        splits = line.split('\t')
        current_ssi[int(splits[-1])] = int(splits[2])
    output_file = open('tuple.sql', 'w')
    mac = '\"11:11:11:11:11:11\"'
    tuId = random.randint(0,0x7fffffff)
    output_file.write('INSERT INTO trainer_tuple VALUES ')
    length = tuples.__len__()
    for i in range(0, length):
        cur_no = tuples[i].Correct_no
        for j in range(0, NOINUM):
            tmp = list()
            for k in range(0, gl.NUMBER_OF_PIS):
                tmp.append(tuples[i].ssi_array[k]+random.randint(-NOICEFACTOR, NOICEFACTOR))
            tuples.append(MyTuple(cur_no, tmp))
    random.shuffle(tuples)
    for i in range(0, tuples.__len__()):
        print tuples[i].ssi_array
        output_file.write('(' + str(tuId) + ',' + mac + ',\"' + pickle.dumps(tuples[i].ssi_array) + '\",' + str(tuples[i].Correct_no) + ',0,1000)')
        tuId += 1
        if i != tuples.__len__()-1:
            output_file.write(',')
        else:
            output_file.write(';\n')


def randomTest():
    Ts = dict()
    Thres = dict()
    Weights = dict()
    for i in range(0, gl.NUMBER_OF_PIS):
        modelf = open('model/room' + str(i))
        Ts[i] = pickle.load(modelf)
        Thres[i] = pickle.load(modelf)
        Weights[i] = pickle.load(modelf)
        modelf.close()
    global tuples
    #tuples = TUPLE.objects.filter(Used=0)
    total = 0.0
    correct_count = 0
    for tp in tuples:
        correct_no = tp.Correct_no
        delta = dict()
        vote = dict()
        ssi_array = tp.ssi_array
        for i in range(0, gl.NUMBER_OF_PIS):
            vote[i] = 0.0
            for j in range(0, Ts[i].__len__()):
                delta[Ts[i][j]] = ssi_array[Ts[i][j][0]] - ssi_array[Ts[i][j][1]]
                if delta[Ts[i][j]] > Thres[i][j]:
                    vote[i] += Weights[i][j]
        max = -1
        position = -1
        for key in vote.keys():
            if vote[key] > max:
                max = vote[key]
                position = key
                continue
            '''if vote[key] == max:
                assert(False)'''
        if position == correct_no:
            correct_count += 1
        total += 1
    print correct_count / total



if __name__ == '__main__':
    readTuples()
    #randomTest()
