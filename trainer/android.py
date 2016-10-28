from trainer.models import POSITION
from django.http import HttpResponse
# import string
# import pdb


# pdb.set_trace()
def update_position(request):
    dic = request.POST
    position = POSITION(Mac=dic['mac'], Time=dic['time'], No=dic['no'])
    position.save()
    return HttpResponse("Success!")

