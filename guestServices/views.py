from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from untersetzerBroker.models import Untersetzer, serviceCall, paymentRequest, paymentSuccess


def dashboardView(request, coasterId):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    total_price = 0
    itemList = []
    for bevs in coaster.beverage.all():
        itemList.append(bevs)
    for food in coaster.food.all():
        itemList.append(food)
    for total_food in coaster.food.all():
        total_price += total_food.price
    for total_bev in coaster.beverage.all():
        total_price += total_bev.price
    return render(request, 'guestServices.html', {'dashboardTemplateData': itemList, 'coasterId': coasterId, 'total_price': total_price})

def callService(request, coasterId):
    #coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    # Send Notification
    s = serviceCall.objects.get_or_create(coaster_id=coasterId)
    return HttpResponse("Service benachrichtigt")

def PaymentSuccess(request, coasterId):
    p = paymentSuccess.objects.get_or_create(coaster_id=coasterId)

def requestPayment(request, coasterId, modality):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    # Send Notification
    p = paymentRequest.objects.get_or_create(coaster_id=coasterId, type=modality)
    return HttpResponse("<div class='notification'>Ihr Zahlungswunsch wurde entgegen genommen.</div>")

def deleteService(request, identifier):
    deleted = serviceCall.objects.filter(id=identifier).delete()
    return HttpResponse("Service-Anfrage gelöscht!")

def deletePayment(request, identifier):
    deleted = paymentSuccess.objects.filter(id=identifier).delete()
    return HttpResponse("Payment done!")

def deletePaymentRequest(request, identifier):
    deleted = paymentRequest.objects.filter(id=identifier).delete()
    return HttpResponse("Zahlungswunsch gelöscht!")

def create_bill(request, coasterId):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    total_price = 0
    itemList = []
    for bevs in coaster.beverage.all():
        itemList.append(bevs)
    for food in coaster.food.all():
        itemList.append(food)
    for total_food in coaster.food.all():
        total_price += total_food.price
    for total_bev in coaster.beverage.all():
        total_price += total_bev.price
    return render(request, 'bill.html', {'dashboardTemplateData': itemList, 'coasterId': coasterId, 'total_price': total_price})
