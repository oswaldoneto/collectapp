from document.models import DocumentPublicPermission
def get_public_perms(doc):
    """
    Returns permissions for given document object, as list of strings.
    """
    return  [(dpp.permission.codename) for dpp in DocumentPublicPermission.objects.filter(document=doc)]
