from django.conf.urls import patterns
from django.views.decorators.csrf import csrf_exempt
from storage.api import StorageReserveKeyView, StorageMetadataRefreshView,\
    StorageAccessURLView

urlpatterns = patterns('',
    (r'^api/storage/reserve-key$', csrf_exempt(StorageReserveKeyView.as_view())),
    (r'^api/storage/metadata/refresh/key/(?P<key>\w+)$', csrf_exempt(StorageMetadataRefreshView.as_view())),
    (r'^api/storage/key/(?P<key>\w+)$', csrf_exempt(StorageAccessURLView.as_view())),
        
)
    