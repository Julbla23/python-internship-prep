from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, world.")

def bank(request):
    return HttpResponse("Twoje saldo wynosi 1 000$.")

def hello(request, name):
    template = "hello/hello_name.html"
    ctx = {"name": name}
    return render(request, template, ctx)
