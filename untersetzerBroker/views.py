from datetime import time
from time import sleep

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from untersetzerBroker.models import Untersetzer, Table, Beverage


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


def overviewTest(request):
    allCoasterData = Untersetzer.objects.all()
    return render(request, 'test.html', {'coasterTemplateData': allCoasterData})


def timeout(request, identifier):
    if identifier != '':
        glass = Untersetzer.objects.get(identifier=identifier)
        glass.timeout = True
        glass.save()
        sleep(180)  # Timeout 3 Minuten
        glass.timeout = False
        glass.save()
        return HttpResponse("Updated")
    else:
        return HttpResponse("¯\_(ツ)_/¯")


def overview(request):
    allCoasterData = Untersetzer.objects.all()  # All Data (Old Approach)
    criticalCoaster = []  # Init List for critical Coasters
    for coaster in allCoasterData:  # Iterate over Coaster and check for critical
        if coaster.description == 'Cola0.3' and coaster.glass_level <= 320:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Weizen0.5' and coaster.glass_level <= 650:
            criticalCoaster.append(coaster)
    return render(request, 'main.html', {'coasterTemplateData': allCoasterData, 'criticalCoaster': criticalCoaster})


def newdrink(request, identifier):
    if identifier != '':
        glass = Untersetzer.objects.get(identifier=identifier)
        glass.glass_level = 1000
        glass.save()
        return HttpResponse("Updated")
    else:
        return HttpResponse("¯\_(ツ)_/¯")


def allTables(request):
    tables = Table.objects.all()
    return render(request, 'allTables.html', {'tables': tables})


def getTable(request, identifier):
    table = Table.objects.get(identifier=identifier)
    tableCoaster = []
    for coaster in range(0, table.coasters):
        tableCoaster.append(coaster)
    return render(request, 'table.html', {'tableTemplateData': tableCoaster, 'tableId': table.identifier})


def tablePayCoaster(request, identifier, coasterId):
    # table = Table.objects.get(identifier=identifier)
    glass = Untersetzer.objects.get(identifier=coasterId)
    bill = 0.0
    for bevs in glass.beverage.all():
        bill += bevs.price
    return HttpResponse(round(bill, 2))


def tableDeleteCoaster(request, identifier, coasterId):
    coaster = Beverage.objects.filter(coaster_id=coasterId).delete()
    return HttpResponse("Getränke gelöscht!")


def tableNewBeverage(request, identifier, coasterId, beverageName, beverageEdition):
    if beverageName == 'Cola':
        price = 3.99
    elif beverageName == 'Pils' and beverageEdition == '0.4':
        price = 4.50
    elif beverageName == 'Weizen':
        price = 4.50
    elif beverageName == 'Wasser':
        price = 4.50
    elif beverageName == 'Cappuchino':
        price = 4.50
    b = Beverage.objects.create(name=beverageName, edition=beverageEdition, price=price, coaster_id=coasterId)
    c = Untersetzer.objects.filter(identifier=coasterId).update(description=beverageName + beverageEdition)
    return HttpResponse("Added")
