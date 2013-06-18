from django import template
from django.contrib.admin.templatetags.admin_list import register
from document.models import Document, DocumentPublicPermission

class PermissionCheckerNode(template.Node):
    def __init__(self, model, context_var):
        self.model = template.Variable(model)
        self.context_var = context_var

    def render(self, context):
        model = self.model.resolve(context)
        if not isinstance(model, Document):
            raise template.TemplateSyntaxError("invalid get_public_perms tag usage")
        context[self.context_var] = [(dpp.permission.codename) for dpp in DocumentPublicPermission.objects.filter(document=model)]
        return ''   

@register.tag
def get_public_perms(parser,token):
    """
    {% get_public_perms model as context_var %}
    """ 
    bits = token.split_contents()
    if len(bits) != 4 or bits[2] != 'as':
        raise template.TemplateSyntaxError("invalid get_public_perms tag usage")
    model = bits[1]
    context_var = bits[3]
    return PermissionCheckerNode(model, context_var)
    
    