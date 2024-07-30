from django.http import HttpResponse
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