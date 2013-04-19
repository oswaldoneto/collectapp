from django.conf.urls import patterns
from status import views

urlpatterns = patterns('',
    (r'^status$',views.collect_config),
)
    