from datetime import time
from time import sleep

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from untersetzerBroker.models import Untersetzer, Table, Beverage, lastBeverages, BeverageTemplate, paymentRequest, \
    serviceCall, FoodTemplate, Food, QuickAccessTemplateFood, QuickAccessTemplate, tempCoasterGroup


def index(request):
    return HttpResponse("Hello, world. This is a master thesis by Robert Fischbach & Enzo Frenker-Hackfort.")


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
    payment = paymentRequest.objects.all()
    service = serviceCall.objects.all()
    for coaster in allCoasterData:  # Iterate over Coaster and check for critical
        beverageTemplate = BeverageTemplate.objects.filter(name=coaster.description)
        for bt in beverageTemplate:
            if coaster.glass_level <= bt.weight:
                criticalCoaster.append(coaster)
    return render(request, 'main.html',
                  {'coasterTemplateData': allCoasterData,
                   'criticalCoaster': criticalCoaster,
                   'newDrinks': newDrinks,
                   'payment': payment,
                   'service': service,
                   })


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
    allBeverageData = BeverageTemplate.objects.all()  # Get drink templates
    allFoodData = FoodTemplate.objects.all()  # Get Food templates
    quickDrinkData = QuickAccessTemplate.objects.all()  # Get Food templates
    quickFoodData = QuickAccessTemplateFood.objects.all()  # Get Food templates
    tempGroups = tempCoasterGroup.objects.filter(table=identifier)  # Get Temp-Coasters
    tempGroupsList = []
    for tempGroup in tempGroups:
        #print(tempGroup.coasters.all())
        tempGroupsList.append(tempGroup.coasters.all())
        #print(tempGroupsList)
    tableCoaster = []
    for coaster in table.coasters.all():
        tableCoaster.append(coaster)
    return render(request, 'table.html', {'tableTemplateData': tableCoaster, 'tableId': table.identifier,
                                          'beverageTemplateData': allBeverageData, 'foodTemplateData': allFoodData,
                                          'quickFood': quickFoodData, 'quickDrink': quickDrinkData,
                                          'tempGroups': tempGroupsList})

def getSubGroups(request, identifier):
    table = Table.objects.get(identifier=identifier)
    tableCoaster = []
    for coaster in table.coasters.all():
        tableCoaster.append(coaster)
    return render(request, 'subGroups.html', {'tableTemplateData': tableCoaster, 'tableId': table.identifier,})


def getTableGroupOrder(request, identifier):
    table = Table.objects.get(identifier=identifier)
    allBeverageData = BeverageTemplate.objects.all()  # Get drink templates
    allFoodData = FoodTemplate.objects.all()  # Get Food templates
    quickDrinkData = QuickAccessTemplate.objects.all()  # Get Food templates
    quickFoodData = QuickAccessTemplateFood.objects.all()  # Get Food templates
    tableCoaster = []
    for coaster in table.coasters.all():
        tableCoaster.append(coaster)
    return render(request, 'groupOrder.html', {'tableTemplateData': tableCoaster, 'tableId': table.identifier,
                                               'beverageTemplateData': allBeverageData, 'foodTemplateData': allFoodData,
                                               'quickFood': quickFoodData, 'quickDrink': quickDrinkData})


def getTableBuyARound(request, identifier):
    table = Table.objects.get(identifier=identifier)
    allBeverageData = BeverageTemplate.objects.all()  # Get drink templates
    allFoodData = FoodTemplate.objects.all()  # Get Food templates
    quickDrinkData = QuickAccessTemplate.objects.all()  # Get Food templates
    quickFoodData = QuickAccessTemplateFood.objects.all()  # Get Food templates
    tableCoaster = []
    for coaster in table.coasters.all():
        tableCoaster.append(coaster)
    return render(request, 'buyaround.html', {'tableTemplateData': tableCoaster, 'tableId': table.identifier,
                                              'beverageTemplateData': allBeverageData, 'foodTemplateData': allFoodData,
                                              'quickFood': quickFoodData, 'quickDrink': quickDrinkData})


def tablePayCoaster(request, identifier, coasterId):
    # table = Table.objects.get(identifier=identifier)
    glass = Untersetzer.objects.get(identifier=coasterId, table__identifier=identifier)
    bill = 0.0
    for bevs in glass.beverage.all():
        bill += bevs.price
    for food in glass.food.all():
        bill += food.price
    return HttpResponse(round(bill, 2))


def tablePayTable(request, identifier):
    glass = Untersetzer.objects.filter(table__identifier=identifier)
    bill = 0.0
    for coaster in glass:
        for bevs in coaster.beverage.all():
            bill += bevs.price
        for food in coaster.food.all():
            bill += food.price
    return HttpResponse(round(bill, 2))


def tableDeleteCoaster(request, identifier, coasterId):
    coaster = Untersetzer.objects.get(identifier=coasterId, table__identifier=identifier)
    for bevs in coaster.beverage.all():
        bevs.delete()
    for food in coaster.food.all():
        food.delete()
    return HttpResponse("Getränke und Speisen gelöscht!")


def tableNewBeverage(request, identifier, coasterId, beverageName, beverageEdition):
    beverageTemplate = BeverageTemplate.objects.filter(name=beverageName, edition=beverageEdition)
    coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
    b = Beverage.objects.create(name=beverageTemplate[0].name,
                                edition=beverageTemplate[0].edition,
                                price=beverageTemplate[0].price,
                                coaster=coaster)
    l = lastBeverages.objects.create(beverages=b)
    c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
        description=beverageTemplate[0].name + beverageTemplate[0].edition)
    return HttpResponse("Added")


def tableNewFood(request, identifier, coasterId, foodName, ):
    foodTemplate = FoodTemplate.objects.filter(name=foodName)
    coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
    b = Food.objects.create(name=foodTemplate[0].name,
                            price=foodTemplate[0].price,
                            coaster=coaster)
    return HttpResponse("Added")


def tableNewBeverageMulti(request, identifier, coasterId):
    beverages = request.POST.getlist('beverages[]')
    for beverageName in beverages:
        price = 0.0
        beverageEdition = ""
        beverage = BeverageTemplate.objects.filter(name=beverageName)
        for b in beverage:
            print(b.name)
            coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
            booking = Beverage.objects.create(name=b.name,
                                              edition=b.edition,
                                              price=b.price,
                                              coaster=coaster)
            l = lastBeverages.objects.create(beverages=booking)
            c = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).update(
                description=b.name + b.edition)
    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp


def tableNewFoodMulti(request, identifier, coasterId):
    foods = request.POST.getlist('foods[]')
    for foodName in foods:
        price = 0.0
        beverageEdition = ""
        food = FoodTemplate.objects.filter(name=foodName)
        for f in food:
            print(f.name)
            coaster = Untersetzer.objects.filter(identifier=coasterId, table__identifier=identifier).get()
            booking = Food.objects.create(name=f.name,
                                          price=f.price,
                                          coaster=coaster)
    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp


def newDrinksDeleteLatest(request, identifier):
    deleted = lastBeverages.objects.filter(id=identifier).delete()
    return HttpResponse("Getränke gelöscht!")

def subGroupDelete(request, identifier):
    deleted = tempCoasterGroup.objects.filter(coasters__id=identifier).delete()
    return HttpResponse("Subgroup gelöscht!")


def rundeAusgeben(request, identifier):
    beverages = request.POST.getlist('beverages[]')
    receivingCoasters = request.POST.getlist('coasters[]')
    payingCoasters = request.POST.getlist('payingCoasters[]')
    print(payingCoasters[0])

    for beverageName in beverages:
        beverageTemplate = BeverageTemplate.objects.filter(name=beverageName)
        for rcId in receivingCoasters:
            b = Beverage.objects.create(name=beverageTemplate[0].name,
                                        edition='Das Getränk wurde ausgegeben!',
                                        price=0,
                                        coaster=Untersetzer.objects.filter(identifier=rcId)[0])
            a = Beverage.objects.create(name=beverageTemplate[0].name,
                                        edition=beverageTemplate[0].edition,
                                        price=beverageTemplate[0].price,
                                        coaster=Untersetzer.objects.filter(identifier=payingCoasters[0])[0])
            l = lastBeverages.objects.create(beverages=b)
            c = Untersetzer.objects.filter(identifier=rcId, table__identifier=identifier).update(
                description=beverageTemplate[0].name + beverageTemplate[0].edition)
    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp


def groupOrder(request, identifier):
    beverages = request.POST.getlist('beverages[]')
    receivingCoasters = request.POST.getlist('coasters[]')

    for beverageName in beverages:
        beverageTemplate = BeverageTemplate.objects.filter(name=beverageName)
        for rcId in receivingCoasters:
            b = Beverage.objects.create(name=beverageTemplate[0].name,
                                        edition=beverageTemplate[0].edition,
                                        price=beverageTemplate[0].price,
                                        coaster=Untersetzer.objects.filter(identifier=rcId)[0])
            l = lastBeverages.objects.create(beverages=b)
            c = Untersetzer.objects.filter(identifier=rcId, table__identifier=identifier).update(
                description=beverageTemplate[0].name + beverageTemplate[0].edition)
    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp

def createSubGroup(request, identifier):
    sbCoasters = request.POST.getlist('coasters[]')
    b = tempCoasterGroup.objects.create(table_id=identifier)
    for coaster in sbCoasters:
        b.coasters.add(coaster)

    resp = HttpResponse("Added")
    resp['HX-Redirect'] = '/table/' + identifier
    return resp

def tablePayTempGroup(request, identifier):
    # table = Table.objects.get(identifier=identifier)
    group = tempCoasterGroup.objects.get(coasters__id=identifier)
    coasters = group.coasters.all()
    bill = 0.0
    for coaster in coasters:
        for bevs in coaster.beverage.all():
            bill += bevs.price
        for food in coaster.food.all():
            bill += food.price
    return HttpResponse(round(bill, 2))

def tablePayAndDeleteTempGroup(request, identifier):
    # table = Table.objects.get(identifier=identifier)
    group = tempCoasterGroup.objects.get(coasters__id=identifier)
    coasters = group.coasters.all()
    bill = 0.0
    for coaster in coasters:
        for bevs in coaster.beverage.all():
            bevs.delete()
        for food in coaster.food.all():
            food.delete()
    group.delete()

    resp = HttpResponse("Deleted")
    resp['HX-Refresh'] = True
    return resp
