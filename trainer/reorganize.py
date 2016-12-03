from models import POSITION
from models import DEVICE
from models import TUPLE
import gl
from django.http import HttpResponse

import pickle
# import string
import pdb


# pdb.set_trace()
def reorganize(request):  # reorganize the data to be computed conveniently and store them in table tuple
	NUMBER_OF_PIS = gl.NUMBER_OF_PIS  # HERE DEFINE THE NUMBER OF PIS, can read from database later
	positions = POSITION.objects.filter(Used=0)
	for position in positions:
		time = position.Time
		mac = position.Mac
		correct_no = position.No  # details in trainer/models.py
		# array = [-150] * NUMBER_OF_PIS
		array = list()
                # ###########!!!!! the No of classroom start from 0
		for i in range(0, NUMBER_OF_PIS):
			devices = DEVICE.objects.filter(Mac=mac).filter(Class_No=i).filter(Time__gt=time - 180).filter(Time__lt=time + 180)
			# search for current data(Mac,Class_No,time in 180seconds)
			if len(devices) != 0:
				# pdb.set_trace()
				'''maxSsi = -150
				for device in devices:
					if device.Ssi > maxSsi:
						maxSsi = device.Ssi
				array[i - 1] = maxSsi  # the most powerful signal is the correct one'''
				#array[i] = devices[0].Ssi  # tempary select the first data
				array.append(devices[0].Ssi)
			else:
				array.append(-150)
		"""
		Here, we construct an array storing Ssi of the current device gather by each pi(default 0)
		The Array should be unserialized using pickle.loads(Array)
		"""
		orgData = TUPLE(Mac=mac, Correct_no=correct_no, Array=pickle.dumps(array), Time=time)
		orgData.save()
		# position.Used = 1
		# position.save()  # may be wrong
	return HttpResponse("Success")


def checkTuple():
	Array = [0, 1, 2, 3, 4, 5]
	string1 = pickle.dumps(Array)
	Array1 = pickle.loads(string1)
	for i in range(0, 6):
		print("%d ", Array1[i])


if __name__ == '__main__':
	checkTuple()

