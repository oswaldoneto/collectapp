
from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group        
        
class ExtendedUserChangeForm(UserChangeForm):
    """
    Permissions is handled in a different way,
    that means outside user form. 
    """
    class Meta:
        model = User
        exclude = ('user_permissions')
        
class  ExtendedPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        user = kwargs['initial']['user']
        super(ExtendedPasswordChangeForm, self).__init__(user,*args, **kwargs)
    
        
            
    
    
        