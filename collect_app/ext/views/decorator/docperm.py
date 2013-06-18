from functools import wraps
from django.utils.decorators import available_attrs
from ext.views.decorator.exceptions import DocPermDecoratorError
from django.shortcuts import get_object_or_404
from document.models import Document, DocumentPublicPermission
from django.http import HttpResponseForbidden

def document_permission_or_403(permissions,lookup):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled for a particular document.

    :param permissions: Tuple of permissions to be checked 
    :param lookup: Lookup field key 

    Examples::

        @method_decorator(document_permission_or_403(('document.change_document',),'document'))
        def my_view(request):
            return HttpResponse('Hello')

        @method_decorator(document_permission_or_403(('document.read_document','document.change_document',),'document'))
        def dispatch(self, *args, **kwargs):
            return super(YourClassBasedView, self).dispatch(*args, **kwargs)
    """    
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            has_perm = False
            if lookup in kwargs:
                doc = get_object_or_404(Document,pk=kwargs[lookup])
                public_permissions = [(dpp.permission.codename) for dpp in DocumentPublicPermission.objects.filter(document=doc)]
                for perm in permissions:
                    if perm in public_permissions:
                        has_perm = True
                        break
                    if request.user.has_perm(perm, doc):
                        has_perm = True
                        break
                if not has_perm:
                    return HttpResponseForbidden()
            return func(request, *args, **kwargs)
        return inner
    return decorator