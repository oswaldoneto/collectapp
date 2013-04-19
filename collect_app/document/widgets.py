
from django import forms
from django.contrib.admin.templatetags.admin_static import static

class DateWidget(forms.DateInput):
    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vDateField', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(DateWidget, self).__init__(attrs=final_attrs, format=format)

