from trainer.models import DEVICE, CLASSROOM
from django.http import HttpResponse


def update_device(request):
    dic = request.POST
    '''room_list = CLASSROOM.objects.filter(No=dic['no'])
    if not room_list:
        room = CLASSROOM(No=dic['no'])
        room.save()
    else:
        assert(len(room_list) == 1)
        room = room_list[0]
    '''
    device = DEVICE(Mac=dic['mac'], Ssi=dic['ssi'], Time=dic['time'], Class_No=dic['no'])
    device.save()
    return HttpResponse("Success")
