from server.models import CLASSROOM
from django.http import HttpResponse
import datetime
# import pdb

# pdb.set_trace()


def one_classroom(request):
    dic = request.GET
    classroom = CLASSROOM.objects.filter(No=dic['no'])
    if not classroom:
        return HttpResponse('No such classroom')
    p = classroom.Num_of_device
    return HttpResponse("%d devices in this classroom" % p)


def syn_time(request):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pos = current_time.find(' ')
    date_command = "date --set " + current_time[0:pos] + "\n"
    time_command = "date --set " + current_time[pos+1:] + "\n"
    hard_command = "hwclock -w\n"
    return HttpResponse(date_command + time_command + hard_command)
