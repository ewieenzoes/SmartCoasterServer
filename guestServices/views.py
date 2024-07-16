from django.http import HttpResponse
from django.shortcuts import render
from untersetzerBroker.sumup import SumupAPI
import uuid 

# Create your views here.
from untersetzerBroker.models import Untersetzer, serviceCall, paymentRequest, paymentSuccess, Checkout, CheckoutPositions


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
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    print(coaster)
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

def deletePayment(request, coasterId):
    paymentSuccess.objects.filter(id=coasterId).delete()
    return HttpResponse("Payment done!")

def deletePaymentRequest(request, identifier):
    deleted = paymentRequest.objects.filter(id=identifier).delete()
    return HttpResponse("Zahlungswunsch gelöscht!")

# def createBill(request, transaction, coasterId):

#     coaster = Untersetzer.objects.filter(identifier=coasterId).get()
#     total_price = 0
#     itemList = []
#     for bevs in coaster.beverage.all():
#         bevs.price = format(bevs.price, '.2f')
#         itemList.append(bevs)
#     for food in coaster.food.all():
#         food.price = format(food.price, '.2f')
#         itemList.append(food)
#     for total_food in coaster.food.all():
#         total_price += total_food.price
#     for total_bev in coaster.beverage.all():
#         total_price += total_bev.price

#     total_price = format(total_price, '.2f')

#     # bill = Bill.objects.get_or_create(transaction=transaction)

#     bill = Bill.objects.create(transaction=transaction,
#                             total_price=total_price,
#                             tip=0,
#                             coaster=Untersetzer.objects.filter(identifier=coasterId)[0])

#     return

def create_bill(request, checkout_reference):
    checkout = Checkout.objects.get(checkout_reference=checkout_reference)

    pos = CheckoutPositions.objects.all()
    print(pos)
    # print(checkout.positions)
    # print(checkout.positions.all())
    # print(checkout.positions.objects.all())
    checkout.total_price =  format(checkout.total_price, '.2f')
    itemList = []
    # for bevs in coaster.beverage.all():
    #     bevs.price = format(bevs.price, '.2f')
    #     itemList.append(bevs)
    # for food in coaster.food.all():
    #     food.price = format(food.price, '.2f')
    #     itemList.append(food)
    # for total_food in coaster.food.all():
    #     total_price += total_food.price
    # for total_bev in coaster.beverage.all():
    #     total_price += total_bev.price

    # total_price = format(total_price, '.2f')

    # Händerinformationen einholen
    service = SumupAPI()
    me = service.get('me')

    checkoutSumup = service.get('checkouts?checkout_reference=' + checkout_reference)
    # print(checkoutSumup[0])
    # checkoutSumup[0].date=time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(checkoutSumup[0].date))

    return render(request, 'bill.html', {'me': me, 'dashboardTemplateData': itemList, 'checkout': checkout, 'checkoutSumup': checkoutSumup[0] })


def selfCheckout(request, coasterId):
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    total_price = 0
    itemList = []
    for bevs in coaster.beverage.all():
        bevs.price = format(bevs.price, '.2f')
        itemList.append(bevs)
    for food in coaster.food.all():
        food.price = format(food.price, '.2f')
        itemList.append(food)
    for total_food in coaster.food.all():
        total_price += total_food.price
    for total_bev in coaster.beverage.all():
        total_price += total_bev.price

    total_price = format(total_price, '.2f')

    return render(request, 'selfCheckout.html', {'coasterId': coasterId, 'dashboardTemplateData': itemList, 'total_price': total_price})

def addTip(request, coasterId, percent, fixValue):
    
    coaster = Untersetzer.objects.filter(identifier=coasterId).get()
    total_price = 0
    checkout_reference = uuid.uuid4()
    checkoutObj = Checkout.objects.create(checkout_reference=checkout_reference,
                        total_price=total_price,
                        tip=tip,
                        coaster=coaster)

    for total_food in coaster.food.all():
        CheckoutPositions.objects.create(checkout=checkoutObj,
                                         name = total_food,
                                         price = total_food.price)
        total_price += total_food.price
    for total_bev in coaster.beverage.all():
        CheckoutPositions.objects.create(checkout=checkoutObj,
                                         name = total_bev,
                                         price = total_bev.price)
        total_price += total_bev.price


    if percent != '-':
        amount = total_price * ( float(percent) / 100 + 1 )
    else:
        amount = float(fixValue)

    tip = amount - total_price 

    service = SumupAPI()
    merchant_code = service.get_merchant_code()
    checkout = service.post('checkouts', {
        "checkout_reference": str(checkout_reference),
        "amount": amount,
                    "items": [
                {
                    "name": "Product/Service",
                    "quantity": 1,
                    "price": total_price,
                    "currency": "EUR",
                    "reference": "product",
                    "unit_amount": {
                        "value": 1,
                        "currency": "EUR"
                    },
                    "unit_tax_amount": {
                        "value": 1,
                        "currency": "EUR"
                    }
                },
                {
                    "name": "Tip",
                    "quantity": 1,
                    "price": tip,
                    "currency": "EUR",
                    "reference": "tip",
                    "unit_amount": {
                        "value": 1,
                        "currency": "EUR"
                    },
                    "unit_tax_amount": {
                        "value": 1,
                        "currency": "EUR"
                    }
                }
            ],
        "currency": "EUR",
        "merchant_code": merchant_code,
        "description": "Untersetzer" + coaster.identifier
    })
    print(checkout_reference)


    return render(request, 'sumupWidget.html', { 'checkout': checkout })