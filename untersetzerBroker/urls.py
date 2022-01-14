from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testdata', views.overviewTest, name='testdata'),
    path('level/<str:identifier>/<int:glass_level>', views.level, name='level'),
]