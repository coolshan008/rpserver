from server.models import CLASSROOM, DEVICE
from django.contrib import admin


class DEVICEInline(admin.StackedInline):
    model = DEVICE
    extra = 3


class CLASSROOMAdmin(admin.ModelAdmin):
    fields = ['No', 'Num_of_device']
    inlines = [DEVICEInline]


class DEVICEAdmin(admin.ModelAdmin):
    fields = ['Mac', 'Place', 'Time_to_live']

admin.site.register(CLASSROOM, CLASSROOMAdmin)
admin.site.register(DEVICE, DEVICEAdmin)
