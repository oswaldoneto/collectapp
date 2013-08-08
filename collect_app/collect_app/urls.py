from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
	#Index Page
	(r'^$', TemplateView.as_view(
		template_name="layout/index.html"
	)),
	#Admin App
	(r'^admin/', include(admin.site.urls)),
	# Login App
	url(r'', include('login.urls')),
	# Security App
	url(r'', include('security.urls')),
	# Search App
	url(r'',include('search.urls')),
	# Category App
	url(r'', include('category.urls')),
	# Document App
	url(r'', include('document.urls')),
	# Tag App
	url(r'', include('tag.urls')),
	# Status App
	url(r'', include('status.urls')),
	# Error App
	url(r'', include('error.urls')),
	# Storage App
	url(r'', include('storage.urls')),
)

if settings.DEBUG:	
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_DOC_ROOT}),
		(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	)	
	

	


