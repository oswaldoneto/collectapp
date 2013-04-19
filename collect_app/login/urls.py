from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    
    (r'^login/$','django.contrib.auth.views.login',{'template_name':'app/login/login.xhtml'}),
    (r'^logout/$','django.contrib.auth.views.logout_then_login',{'login_url':'/login/'}),

)
