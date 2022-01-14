from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from untersetzerBroker.models import Untersetzer


def index(request):
    return HttpResponse("Hello, world. This is the Füllstand-Endpoint")

def level(request, identifier, glass_level):
    if identifier != '':
        glass = Untersetzer.objects.get(identifier=identifier)
        glass.glass_level = glass_level
        glass.save()
        return HttpResponse("Updated")
    else:
        return HttpResponse("¯\_(ツ)_/¯")

def overviewTest (request):
    allCoasterData = Untersetzer.objects.all()
    return render(request, 'test.html', {'coasterTemplateData': allCoasterData})