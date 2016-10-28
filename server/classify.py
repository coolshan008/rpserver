from models import SIGNAL
from models import TUPLE
from models import DEVICE
from models import CLASSROOM
import gl
from django.http import HttpResponse

import pickle
# import string
import pdb

# delete all the data may influent the signals haven't been used

# pdb.set_trace()
def reorganize():  # reorganize the data to be computed conveniently and store them in table tuple
    # called every 5 mins
    NUMBER_OF_PIS = gl.NUMBER_OF_PIS  # HERE DEFINE THE NUMBER OF PIS, can read from database later
    signals = SIGNAL.objects.all()
    macs = set()
    devices = dict()
    for signal in signals:
        macs.add(signal.Mac)
        devices[(
            signal.Mac,
            signal.Class_No)] = signal.Ssi  # we don't need to keep the time because the old data have been drop
    for mac in macs:
        array = list()
        for i in range(0, NUMBER_OF_PIS):
            if devices.__contains__((mac, i)):
                # array[i] = devices[0].Ssi  # tempary select the first data
                array.append(devices[(mac, i)])
            else:
                array.append(-150)
        """
        Here, we construct an array storing Ssi of the current device gather by each pi(default 0)
        The Array should be unserialized using pickle.loads(Array)
        """
        orgData = TUPLE(Mac=mac, Array=pickle.dumps(array))
        orgData.save()
        # position.Used = 1
        # position.save()  # may be wrong
    signals.delete()
    # return HttpResponse("Success")


def classify(request):
    reorganize()
    Ts = dict()
    Thres = dict()
    Weights = dict()
    for i in range(0, gl.NUMBER_OF_PIS):
        modelf = open('model/room' + str(i))
        Ts[i] = pickle.load(modelf)
        Thres[i] = pickle.load(modelf)
        Weights[i] = pickle.load(modelf)
        modelf.close()
    tuples = TUPLE.objects.all()
    for tp in tuples:
        delta = dict()
        vote = dict()
        ssi_array = pickle.loads(tp.Array)
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
        classroom = CLASSROOM.objects.get(No=position)
        dev = DEVICE.objects.filter(Mac=tp.Mac)
        if dev.__len__() == 0:
            dev = DEVICE(Mac=tp.Mac, Place=classroom, Time_to_live=gl.time_to_live)
            classroom.Num_of_device += 1
            dev.save()
            classroom.save()
        else:
            dev = dev[0]
            if classroom.No != dev.Place.No:
                old_place = dev.Place
                old_place.Num_of_device -= 1
                old_place.save()
                classroom.Num_of_device += 1
                classroom.save()
                dev.Place = classroom
            dev.Time_to_live = gl.time_to_live
            dev.save()
    tuples.delete()
    return HttpResponse("Success")
