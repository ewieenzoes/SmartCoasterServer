from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from untersetzerBroker.models import Untersetzer, serviceCall, paymentRequest


def dashboardView(request, coasterId):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    itemList = []
    for items in coaster:
        for bevs in coaster.beverage.all():
            itemList.append(bevs.name)
        for food in coaster.food.all():
            itemList.append(food.name)
    return HttpResponse("Deine Speisen --> Template")

def callService(request, coasterId):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    # Send Notification
    s = serviceCall.objects.create(coaster_id=coasterId)
    return HttpResponse("Service benachrichtigt")

def requestPayment(request, coasterId, modality):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    # Send Notification
    p = paymentRequest.objects.create(coaster_id=coasterId, type=modality)
    return HttpResponse("Zahlung")
