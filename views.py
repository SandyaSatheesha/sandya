from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return HttpResponse("Hello World!")


def greet_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return HttpResponse(f"Hello {username}!")
    return render(request, 'greet.html')

