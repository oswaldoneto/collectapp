
from guardian.shortcuts import get_users_with_perms    
from guardian.shortcuts import assign
from guardian.shortcuts import remove_perm
from guardian.shortcuts import get_perms

import rule 

# public --- 

def modify_permission(user_or_group,doc,permission):
    user_or_group_perms = get_perms(user_or_group,doc)
    assign_permission(user_or_group,doc,user_or_group_perms,permission)
    remove_permission(user_or_group,doc,user_or_group_perms,permission)

def clear_permission(user_or_group,doc):
    for perm in get_perms(user_or_group,doc):
        remove_perm(perm,user_or_group,doc)
    
def get_user_permission(doc):
    user_perms = get_users_with_perms(doc,attach_perms=True)
    return user_perms                        


# private --- 

def assign_permission(user,doc,user_perms,req_perm):
    for perm in rule.RULE_PERMISSION_DEPENDENCY:
        if perm not in user_perms:
            assign(perm,user,doc)    
        if req_perm == perm:
            break;
        
def remove_permission(user,doc,user_perms, req_perm):
    for perm in tuple(reversed(rule.RULE_PERMISSION_DEPENDENCY)):  
        if req_perm == perm:
            break;
        if perm in user_perms:
            remove_perm(perm,user,doc)


    
    
    
    
    
        
        
        
        
        
    
    