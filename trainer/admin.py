from trainer.models import DEVICE, POSITION, TUPLE
from django.contrib import admin


class DEVICEInline(admin.StackedInline):
    model=DEVICE
    extra=3


class POSITIONAdmin(admin.ModelAdmin):
    fields=['Mac', 'Time', 'No']


class DEVICEAdmin(admin.ModelAdmin):
    fields = ['Mac', 'Ssi', 'Time', 'Class_No']


class TUPLEAdmin(admin.ModelAdmin):
    fields = ['Mac', 'Correct_no', 'Time', 'Array']

admin.site.register(POSITION, POSITIONAdmin)
admin.site.register(DEVICE, DEVICEAdmin)
admin.site.register(TUPLE, TUPLEAdmin)