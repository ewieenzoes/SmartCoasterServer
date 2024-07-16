from django.urls import path

from . import views

urlpatterns = [
    path('<str:coasterId>/', views.dashboardView, name='dashboardView'),
    path('requestPayment/<str:coasterId>/<str:modality>/', views.requestPayment, name='requestPayment'),
    path('requestPayment/<str:identifier>/delete', views.deletePaymentRequest, name='deletePaymentRequest'),
    path('bill/<str:checkout_reference>/', views.create_bill, name='create_bill'),
    path('callService/<str:coasterId>/', views.callService, name='callService'),
    path('paymentSuccess/<str:coasterId>/', views.PaymentSuccess, name='paymentSuccess'),
    path('callService/<str:identifier>/delete', views.deleteService, name='deleteService'),
    path('paymentSuccess/<str:coasterId>/delete', views.deletePayment, name='deletePayment'),
    path('<str:coasterId>/selfCheckout', views.selfCheckout, name='selfCheckout'),
    path('<str:coasterId>/selfCheckout/addTip/<str:percent>/<str:fixValue>', views.addTip, name='addTip')
]
