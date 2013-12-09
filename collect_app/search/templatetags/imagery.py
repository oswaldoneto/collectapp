from django import template
 
register = template.Library()

IMAGE_GALERY = {
    "image/gif":"icon-picture",
    "application/msword":"icon-file-text",
    "text/plain":"icon-file-text-alt",
    "text/html":"icon-code",
    "text/css":"icon-code",
}

@register.filter
def imagery(value):
    return 'icon-file' if value not in IMAGE_GALERY else IMAGE_GALERY[value]




    
    
    
    


