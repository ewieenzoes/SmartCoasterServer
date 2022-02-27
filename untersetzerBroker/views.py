from datetime import time
from time import sleep

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from untersetzerBroker.models import Untersetzer, Table, Beverage, lastBeverages


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
    for coaster in allCoasterData:  # Iterate over Coaster and check for critical #To-Do: Move to DB
        if coaster.description == 'Riesling' and coaster.glass_level <= 150:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Aperol0.25' and coaster.glass_level <= 212:
            criticalCoaster.append(coaster)
        elif coaster.description == 'MineralWasser0.75' and coaster.glass_level <= 270:
            criticalCoaster.append(coaster)
        elif coaster.description == 'MineralWasser0.25' and coaster.glass_level <= 270:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Cola0.2' and coaster.glass_level <= 250:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Bluna0.2' and coaster.glass_level <= 250:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Apfelschorle0.25' and coaster.glass_level <= 250:
            criticalCoaster.append(coaster)
        elif coaster.description == 'FrühZitrone0.33' and coaster.glass_level <= 270:
            criticalCoaster.append(coaster)
        elif coaster.description == 'RadlerFL' and coaster.glass_level <= 270:
            criticalCoaster.append(coaster)
        elif coaster.description == 'PilsFL' and coaster.glass_level <= 270:
            criticalCoaster.append(coaster)
        elif coaster.description == 'VitaMalz0.5' and coaster.glass_level <= 270:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Benediktiner0.5' and coaster.glass_level <= 545:
            criticalCoaster.append(coaster)
        elif coaster.description == 'BenediktinerWeiss0.5' and coaster.glass_level <= 505:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Weizen0.5' and coaster.glass_level <= 545:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Koelsch0.3' and coaster.glass_level <= 245:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Keller0.3' and coaster.glass_level <= 385:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Radler0.3' and coaster.glass_level <= 350:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Colabier0.3' and coaster.glass_level <= 350:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Schuss0.3' and coaster.glass_level <= 350:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Kaffee' and coaster.glass_level <= 490:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Milchkaffee' and coaster.glass_level <= 550:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Cappuccino' and coaster.glass_level <= 550:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Cappuccino0.35' and coaster.glass_level <= 550:
            criticalCoaster.append(coaster)
        elif coaster.description == 'CappuccinoSpezial' and coaster.glass_level <= 550:
            criticalCoaster.append(coaster)
        elif coaster.description == 'LatteMacchiato' and coaster.glass_level <= 520:
            criticalCoaster.append(coaster)
        elif coaster.description == 'Kakao' and coaster.glass_level <= 550:
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
    if request.method == 'POST':
        for beverageName in request.POST.getlist['multiselect']:
            if beverageName == 'Cola':
                price = 3.99
            elif beverageName == 'Pils 0,3':
                price = 4.50
            coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
            b = Beverage.objects.create(name=beverageName, edition=beverageEdition, price=price, coaster=coaster)
            l = lastBeverages.objects.create(beverages=b)
            c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
                description=beverageName + beverageEdition)
        return HttpResponse("Added (Req: Post)")
    else: #To-Do: Move to DB
        if beverageName == 'Keller':
            price = 2.80
        elif beverageName == 'Cola':
            price = 2.50
        elif beverageName == 'Weizen':
            price = 4.40
        elif beverageName == 'WasserFL':
            price = 6.90
        elif beverageName == 'Cappuchino':
            price = 2.50
        coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
        b = Beverage.objects.create(name=beverageName, edition=beverageEdition, price=price, coaster=coaster)
        l = lastBeverages.objects.create(beverages=b)
        c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
            description=beverageName + beverageEdition)
        return HttpResponse("Added")


def tableNewBeverageMulti(request, identifier, coasterId):
    beverages = request.POST.getlist('beverages[]')
    for beverageName in enumerate(beverages):
        price = 0.0
        beverageEdition = "" #To-Do: Move to DB
        if beverageName[1] == 'Riesling':
            price = 21.90
            print(beverageName[1])
            beverageEdition = "FL"
        elif beverageName[1] == 'Aperol0.25':
            price = 5.60
            beverageEdition = "0,25"
        elif beverageName[1] == 'MineralWasser0.75':
            price = 6.90
            beverageEdition = "0,75"
        elif beverageName[1] == 'MineralWasser0.25':
            price = 2.30
            beverageEdition = "0,25"
        elif beverageName[1] == 'Cola0.2':
            price = 2.50
            beverageEdition = "0,20"
        elif beverageName[1] == 'Bluna0.2':
            price = 2.50
            beverageEdition = "0,20"
        elif beverageName[1] == 'Apfelschorle0.25':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'FrühZitrone0.33':
            price = 2.80
            beverageEdition = "0,33"
        elif beverageName[1] == 'RadlerFL':
            price = 2.80
            beverageEdition = "0,33"
        elif beverageName[1] == 'PilsFL':
            price = 2.80
            beverageEdition = "0,33"
        elif beverageName[1] == 'VitaMalz0.5':
            price = 4.40
            beverageEdition = "0,5"
        elif beverageName[1] == 'Benediktiner0.5':
            price = 4.40
            beverageEdition = "0,5"
        elif beverageName[1] == 'BenediktinerWeiss0.5':
            price = 4.40
            beverageEdition = "0,5"
        elif beverageName[1] == 'Weizen0.5':
            price = 4.40
            beverageEdition = "0,5"
        elif beverageName[1] == 'Koelsch0.3':
            price = 2.80
            beverageEdition = "0,3"
        elif beverageName[1] == 'Keller0.3':
            price = 2.80
            beverageEdition = "0,3"
        elif beverageName[1] == 'Radler0.3':
            price = 2.80
            beverageEdition = "0,3"
        elif beverageName[1] == 'Colabier0.3':
            price = 2.80
            beverageEdition = "0,3"
        elif beverageName[1] == 'Schuss0.3':
            price = 2.80
            beverageEdition = "0,3"
        elif beverageName[1] == 'Kaffee':
            price = 2.20
            beverageEdition = "0,25"
        elif beverageName[1] == 'Milchkaffee':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'Cappuccino':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'CappuccinoSpezial':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'LatteMacchiato':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'Espresso':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'EspressoMacchiato':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'Kakao':
            price = 2.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'JackWaeller':
            price = 3.00
            beverageEdition = "0,25"
        elif beverageName[1] == 'Ramazotti':
            price = 3.00
            beverageEdition = "0,25"
        elif beverageName[1] == 'Obstler':
            price = 3.00
            beverageEdition = "0,25"
        elif beverageName[1] == 'Grappa':
            price = 3.00
            beverageEdition = "0,25"
        elif beverageName[1] == 'AlteMarille':
            price = 3.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'AlteWilliams':
            price = 3.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'AlteHimbeere':
            price = 3.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'AlteKirsche':
            price = 3.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'AlteQuetsch':
            price = 3.50
            beverageEdition = "0,25"
        elif beverageName[1] == 'Haselnuss':
            price = 3.50
            beverageEdition = "0,25"
        coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
        b = Beverage.objects.create(name=beverageName[1], edition=beverageEdition, price=price, coaster=coaster)
        l = lastBeverages.objects.create(beverages=b)
        c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
            description=beverageName[1])
    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp


def newDrinksDeleteLatest(request, identifier):
    deleted = lastBeverages.objects.filter(id=identifier).delete()
    return HttpResponse("Getränke gelöscht!")
