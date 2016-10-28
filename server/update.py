from server.models import CLASSROOM, DEVICE, SIGNAL
from django.http import HttpResponse
import string
# import pdb

# pdb.set_trace()


def update_signal(request):
    dic = request.POST
    # room_no = CLASSROOM.objects.filter(No=dic['no'])[0]  # we assert the classroom is in the table
    device = SIGNAL(Mac=dic['mac'], Ssi=dic['ssi'], Time=dic['time'], Class_No=dic['no'])
    device.save()
    return HttpResponse("Success")


def cron(request):
    devices = DEVICE.objects.all()
    for device in devices:
        if device.Time_to_live == 0:
            device.Place.Num_of_device -= 1
            device.Place.save()
            device.delete()
        else:
            device.Time_to_live -= 1
            device.save()
    return HttpResponse("success")
