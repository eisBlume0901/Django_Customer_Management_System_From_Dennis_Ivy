from django.http import *
from django.shortcuts import redirect, reverse

# Decorators are used to add functionality to an existing function before that function is executed
# useful for eliminating code redundancy
def unauthorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        else:
            return view_func(request, *args, **kwargs) # call the original function (for example, register and login functions) 
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func): # This acts like a wrapper function which takes in the view function (such as createOrder, updateOrder, deleteOrder)
        def wrapper_func(request, *args, **kwargs): # This is the actual wrapper function that will be executed before the view function
            group = None # Initialize the group variable
            if request.user.groups.exists(): 
                # Get the first group of the user
                group = request.user.groups.all()[0].name # The reason we have to retrieve the first group is because a user can have multiple groups 
            
            if group in allowed_roles: # If the group of the user is in the allowed_roles list then the can proceed to the view template
                return view_func(request, *args, **kwargs) 
            else:
                return HttpResponse('You are not authorized to view this page')
            # print('Working:', allowed_roles) for debugging
        return wrapper_func
    return decorator

