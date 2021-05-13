from django.http import HttpResponse
from django.shortcuts import redirect , redirect


class unauthenticateduser:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        context = {}
        if request.user.is_authenticated:
            return redirect('home')

        return response


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			try:
				if request.user.groups.exists():
					group = request.user.groups.all()[0].name
			except:
				return HttpResponse('Only Vendors are allowed to upload product')
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator



