from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf.urls import url


'''
Error Pages
'''


def handle500(request):
    return render(request, '500.html', status=500)


def handle403(request):
    return render(request, '403.html', status=403)


def handle404(request):
    return render(request, '404.html', status=404)



'''
From this point on everything focuses on static content/redirects. 
Create a function and add a redirect/static page. 
Then add the path to PAGESERVER. It will function the same as any 
top level url
'''


#def example(request):
#    return redirect('https://google.com')


PAGESERVER = [
    # url(r'^example/$', example),

]