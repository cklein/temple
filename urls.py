from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list/$', 'temple.views.list_templates'),
    (r'^get/$', 'temple.views.get_template'),
    (r'^set/$', 'temple.views.set_template'),
)
