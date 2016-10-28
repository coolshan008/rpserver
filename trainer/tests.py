from models import TUPLE
from models import CLASSROOM
from math import *
import pickle
import pdb
import gl
from django.http import HttpResponse

output_file = open('test/output', 'a')


def flash():
    output_file.write('\n\n')


def test(request):
    try:
        flash()
        precision = randomTest()
    finally:
        output_file.close()
    return HttpResponse(str(precision))


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
    tuples = TUPLE.objects.filter(Used=0)
    total = 0.0
    correct_count = 0
    for tp in tuples:
        correct_no = tp.Correct_no
        delta = dict()
        vote = dict()
        ssi_array = pickle.loads(tp.Array)
        debug(ssi_array)
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
    return correct_count / total


def debug(obj):
    output_file.write(str(obj) + '\n')

