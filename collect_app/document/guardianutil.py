
from guardian.shortcuts import get_users_with_perms    
from guardian.shortcuts import assign
from guardian.shortcuts import remove_perm
from guardian.shortcuts import get_perms

def clear_permission(user_or_group,doc):
    for perm in get_perms(user_or_group,doc):
        remove_perm(perm,user_or_group,doc)
    

    
        
        
        
        
        
    
    