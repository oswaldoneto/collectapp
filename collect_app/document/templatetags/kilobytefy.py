from django import template
 
register = template.Library()

@register.filter
def kilobytefy(value):
    """
    Bytes to Kilobyte for template:
    {{ file.size|sizify }}
    """
    try:
        value = value / 1024.0
    except TypeError:
        value = 0
    ext = 'kb'
    return '%s %s' % (str(round(value, 2)), ext)



