#permission for checking assignees 
from rest_framework.permissions import BasePermission
from . import models

class IsAssigneePermission(BasePermission):

    message = "You are not in assigned to this todo"

    def has_object_permission(self, request, view, obj):
        try : 
            todo = models.Todo.objects.get(id=view.kwargs['pk'])
            user = todo.assignee.filter(id = request.user.id)
            if len(user) < 1 : 
                return False
            return True
        except Exception as error:
            # print(error)
            return False 
        
class IsOwnerPermission(BasePermission) : 

    message = "Action not allowed as you are not the owner"

    def has_permission(self, request, view):
        try : 
            
            group = models.Group.objects.get(id=view.kwargs['group_id'])
            if  request.user.id != group.owner.id :
                    return False
            return True        
        except Exception as error:
                # print(error)
                return False 