from django.urls import path

from . import views

urlpatterns = [
    path('<str:coasterId>/', views.dashboardView, name='dashboardView'),
    path('callService/<str:coasterId>/', views.callService, name='callService'),
    path('requestPayment/<str:coasterId>/<str:modality>/', views.requestPayment, name='requestPayment'),
    path('callService/<str:identifier>/delete', views.deleteService, name='deleteService'),
    path('requestPayment/<str:identifier>/delete', views.deletePaymentRequest, name='deletePaymentRequest'),
]
