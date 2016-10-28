from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'rpserver.views.home', name='home'),
    # url(r'^rpserver/', include('rpserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^trainer/android/', 'trainer.android.update_position'),
    url(r'^trainer/pi/', 'trainer.pi.update_device'),
    url(r'^trainer/re/', 'trainer.reorganize.reorganize'),
    url(r'^trainer/train/', 'trainer.train.train'),
    url(r'^trainer/test/', 'trainer.tests.test'),
    url(r'^cron/', 'server.update.cron'),  # update the devices in classroom
    url(r'^update/', 'server.update.update_signal'),  # upload devices
    url(r'^inquiry/', 'server.inquiry.one_classroom'),  # inquiry num in classroom
    url(r'^classify/', 'server.classify.classify'),  # run classify
    url(r'^syn/', 'server.inquiry.syn_time'),
    # url(r'^time/', 'server.system.get_time'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(admin.site.urls)),
)
