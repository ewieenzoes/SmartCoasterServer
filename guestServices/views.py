from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from untersetzerBroker.models import Untersetzer, serviceCall, paymentRequest


def dashboardView(request, coasterId):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    itemList = []
    for bevs in coaster.beverage.all():
        itemList.append(bevs)
    for food in coaster.food.all():
        itemList.append(food)
    return render(request, 'guestServices.html', {'dashboardTemplateData': itemList, 'coasterId': coasterId})

def callService(request, coasterId):
    #coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    # Send Notification
    s = serviceCall.objects.get_or_create(coaster_id=coasterId)
    return HttpResponse("Service benachrichtigt")

def requestPayment(request, coasterId, modality):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    # Send Notification
    p = paymentRequest.objects.get_or_create(coaster_id=coasterId, type=modality)
    return HttpResponse("<div class='notification'>Ihr Zahlungswunsch wurde entgegen genommen.</div>")

def deleteService(request, identifier):
    deleted = serviceCall.objects.filter(id=identifier).delete()
    return HttpResponse("Service-Anfrage gelöscht!")

def deletePaymentRequest(request, identifier):
    deleted = paymentRequest.objects.filter(id=identifier).delete()
    return HttpResponse("Zahlungswunsch gelöscht!")
