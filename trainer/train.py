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


def train(request):
    try:
        flash()
        getTuple()
        training_process()
    finally:
        output_file.close()
    return HttpResponse("success")


# This func is use to generate the data set for training
#pdb.set_trace()


def getTuple():
    classrooms = CLASSROOM.objects.all()
    for no in classrooms:
        no_tuples = TUPLE.objects.filter(Correct_no=no.No)
        if no_tuples.__len__() < gl.NUMBER_OF_SAMPLES:
            return HttpResponse(str(no_tuples.__len__()) + " fail")
        for i in range(0, gl.NUMBER_OF_SAMPLES):
            ssi_array = pickle.loads(no_tuples[i].Array)  # get the samples Ssi array
            temp = dict()
            debug("array = " + str(ssi_array))
            for j in range(0, ssi_array.__len__() - 1):
                for k in range(j + 1, ssi_array.__len__()):
                    temp[(j, k)] = ssi_array[j] - ssi_array[k]  # compute the margin feature between j and k
            gl.CORRECT.append(no.No)  # corresponding room
            gl.DATA.append(temp)
            gl.DATA_SIZE += 1
            gl.DISTRIBUTION.append(1.0)
            no_tuples[i].Used = 1
            no_tuples[i].save()
    # debug(gl.DATA_SIZE)
    # #now gl.DATA is the array of data( data is vector of (SSI1,SSI2,...,SSIn)
    for i in range(0, gl.DISTRIBUTION.__len__()):
        gl.DISTRIBUTION[i] /= gl.DATA_SIZE


def training_process():
    model_file_prefix = 'model/room'
    for i in range(0, gl.NUMBER_OF_PIS):
        file_name = model_file_prefix + str(i)
        model_file = open(file_name, 'w')
        ensemble(i, model_file)
        model_file.close()


# This func is the major process of ensemble training
# @no   The no of the classroom
# @writer The file to write
def ensemble(no, writer):
    Ts = tuple()  # store the T(m) selected to combine the F
    Thres = tuple()
    Weights = tuple()
    exist = set()
    corrects = gl.CORRECT
    if gl.DATA_SIZE == 0:
		return
    for i in range(0, gl.NUMBER_OF_WEAK):

        # Fit a classifier T(m) to the training data using weights wi
        # debug(gl.DATA)
        dict_tmp = gl.DATA[0]
        weights = gl.DISTRIBUTION
        record = list()  # record if T(m) classify correctly
        dict_size = dict_tmp.__len__()
        key = (-1, -1)
        err = 1  # This variant is err(m)
        threshold = 0
        # debug('dict_size = ' + str(dict_size))
        for j in range(0, dict_size):
            key_tmp = dict_tmp.keys()[j]
            if exist.__contains__(key_tmp):
                continue
            for k in range(0, gl.DATA_SIZE):  # try all value as threshold greedy
                threshold_tmp = gl.DATA[k][key_tmp]
                record_tmp = list()
                err_tmp = 0.0
                for l in range(0, gl.DATA_SIZE):  # test the weak learn with all training data
                    data = gl.DATA[l]
                    if data[key_tmp] > threshold_tmp and corrects[l] == no:  # Ci == T(m)
                        record_tmp.append(True)
                        continue
                    if data[key_tmp] <= threshold_tmp and corrects[l] != no:  # Ci == T(m)
                        record_tmp.append(True)
                        continue

                    record_tmp.append(False)  # Ci != T(m)
                    err_tmp += weights[l]
                if err_tmp < err:
                    err = err_tmp
                    # debug('record_tmp = ' + str(record_tmp))
                    record = record_tmp
                    key = key_tmp
                    threshold = threshold_tmp
                    # debug(record)

        debug("err = " + str(err))
        Ts = Ts.__add__((key,))
        Thres = Thres.__add__((threshold,))
        exist.add(key)

        # write to the file, each line write a tuple
        # writer.write(pickle.dumps(Ts) + '\n')

        if err == 0:
            err += 0.000001
        # compute alpha(m)
        alpha = log((1 - err) / err)

        Weights = Weights.__add__((alpha,))
        # Set Wi
        # debug("record size = " + str(record.__len__()))
        # assert(record.__len__() == dict_size)
        wi_sum = 0.0
        for j in range(0, gl.DATA_SIZE):
            if not record[j]:
                # weights[j] *= math.exp(alpha)
                weights[j] *= exp(alpha)
            wi_sum += weights[j]

        # Re-normalize wi
        for j in range(0, gl.DATA_SIZE):
            weights[j] /= wi_sum
    # debug(Ts)

    WeiSum = 0.0
    for wei in Weights:
        WeiSum += wei
    Weights_result = tuple()
    for i in range(0, Weights.__len__()):
        Weights_result = Weights_result.__add__((Weights[i] / WeiSum,))

    pickle.dump(Ts, writer)
    pickle.dump(Thres, writer)
    pickle.dump(Weights_result, writer)


def debug(obj):
    output_file.write(str(obj) + '\n')

