import json

def parseUserPermissions(user_permissions):
    permissions = []
    for perms in user_permissions:
        permission = []
        permission.append(('user_id',perms.id))
        permission.append(('username',perms.username))
        permission.append(('permission',user_permissions[perms]))
        permissions.append(dict(permission))
    return json.dumps(permissions)

def parseGroupPermissions(group_permissions):
    permissions = []
    for perms in group_permissions:
        permission = []
        permission.append(('group_id',perms.id))
        permission.append(('name',perms.name))
        permission.append(('permission',group_permissions[perms]))
        permissions.append(dict(permission))
    return json.dumps(permissions)

def parseUserPermission(user,permission):
    parse = []
    parse.append(('user_id',user.id))
    parse.append(('username',user.username))
    parse.append(('permission',permission))
    return json.dumps(dict(parse))

def parseGroupPermission(group,permission):
    parse = []
    parse.append(('group_id',group.id))
    parse.append(('name',group.name))
    parse.append(('permission',permission))
    return json.dumps(dict(parse))

    
    
 
    
    