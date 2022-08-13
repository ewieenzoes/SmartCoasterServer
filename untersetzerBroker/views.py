from datetime import time
from time import sleep

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from untersetzerBroker.models import Untersetzer, Table, Beverage, lastBeverages, BeverageTemplate


def index(request):
    return HttpResponse("Hello, world. This is Project C by Robert Fischbach & Enzo Frenker-Hackfort.")


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


def timeout(request, identifier, tableId):
    if identifier != '':
        glass = Untersetzer.objects.get(identifier=identifier, table__identifier=tableId)
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
    newDrinks = lastBeverages.objects.all()  # Get new Drinks
    for coaster in allCoasterData:  # Iterate over Coaster and check for critical
        beverageTemplate = BeverageTemplate.objects.filter(name=coaster.description)
        if coaster.glass_level <= beverageTemplate.weight:
            criticalCoaster.append(coaster)
    return render(request, 'main.html',
                  {'coasterTemplateData': allCoasterData, 'criticalCoaster': criticalCoaster, 'newDrinks': newDrinks})


def newdrink(request, identifier, tableId):
    if identifier != '':
        glass = Untersetzer.objects.get(identifier=identifier, table__identifier=tableId)
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
    glass = Untersetzer.objects.get(identifier=coasterId, table__identifier=identifier)
    bill = 0.0
    for bevs in glass.beverage.all():
        bill += bevs.price
    return HttpResponse(round(bill, 2))


def tablePayTable(request, identifier):
    glass = Untersetzer.objects.filter(table__identifier=identifier)
    bill = 0.0
    for coaster in glass:
        for bevs in coaster.beverage.all():
            bill += bevs.price
    return HttpResponse(round(bill, 2))


def tableDeleteCoaster(request, identifier, coasterId):
    coaster = Untersetzer.objects.get(identifier=coasterId, table__identifier=identifier)
    for bevs in coaster.beverage.all():
        bevs.delete()
    return HttpResponse("Getränke gelöscht!")


def tableNewBeverage(request, identifier, coasterId, beverageName, beverageEdition):
    beverageTemplate = BeverageTemplate.objects.filter(name=beverageName, edition=beverageEdition)
    coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
    b = Beverage.objects.create(name=beverageTemplate.name,
                                edition=beverageTemplate.edition,
                                price=beverageTemplate.price,
                                coaster=coaster)
    l = lastBeverages.objects.create(beverages=b)
    c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
        description=beverageTemplate.name + beverageTemplate.edition)
    return HttpResponse("Added")


def tableNewBeverageMulti(request, identifier, coasterId):
    beverages = request.POST.getlist('beverages[]')
    for beverageName in enumerate(beverages):
        price = 0.0
        beverageEdition = ""
        beverageTemplate = BeverageTemplate.objects.filter(name=beverageName[1])
        coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
        b = Beverage.objects.create(name=beverageTemplate.name,
                                    edition=beverageTemplate.edition,
                                    price=beverageTemplate.price,
                                    coaster=coaster)
        l = lastBeverages.objects.create(beverages=b)
        c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
            description=beverageTemplate.name + beverageTemplate.edition)
    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp


def newDrinksDeleteLatest(request, identifier):
    deleted = lastBeverages.objects.filter(id=identifier).delete()
    return HttpResponse("Getränke gelöscht!")

def rundeAusgeben(request, identifier, coasterId, receivingCoasterIds, beverageName, beverageEdition):
    beverageTemplate = BeverageTemplate.objects.filter(name=beverageName, edition=beverageEdition)
    # get Coaster
    payingCoaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
    receivingCoasters = request.POST.getlist('receivingCoasterIds[]')
    # book amount of drinks and money to "ausgeber
    for rcId in enumerate(receivingCoasters):
        b = Beverage.objects.create(name=beverageTemplate.name,
                                    edition=beverageTemplate.edition,
                                    price=beverageTemplate.price,
                                    coaster=payingCoaster
                                    )
        l = lastBeverages.objects.create(beverages=b)
    c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
        description=beverageTemplate.name + beverageTemplate.edition)
    # book "free" drinks to the rest
    for rcId in receivingCoasterIds:
        b = Beverage.objects.create(name=beverageTemplate.name,
                                    edition="FREE",
                                    price=0,
                                    coaster=rcId)
        l = lastBeverages.objects.create(beverages=b)
        c = Untersetzer.objects.filter(identifier=rcId.id, table__identifier=identifier).update(
        description=beverageTemplate.name + beverageTemplate.edition)
    return HttpResponse("Runde gebucht")

def groupOrder(request, identifier, coasterIds, beverageName, beverageEdition):
    beverageTemplate = BeverageTemplate.objects.filter(name=beverageName, edition=beverageEdition)
    # get Coaster
    receivingCoasters = request.POST.getlist('receivingCoasterIds[]')
    # book amount of drinks and money to "ausgeber
    for rcId in coasterIds:
        b = Beverage.objects.create(name=beverageTemplate.name,
                                    edition=beverageTemplate.edition,
                                    price=beverageTemplate.price,
                                    coaster=rcId)
        l = lastBeverages.objects.create(beverages=b)
        c = Untersetzer.objects.filter(identifier=rcId.id, table__identifier=identifier).update(
            description=beverageTemplate.name + beverageTemplate.edition)
    return HttpResponse("Gruppenbestellung gebucht")
