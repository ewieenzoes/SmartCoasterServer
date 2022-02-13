from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testdata', views.overviewTest, name='testdata'),
    path('level/<str:identifier>/<int:glass_level>', views.level, name='level'),
    path('overview/', views.overview, name='overview'),
    path('timeout/<str:identifier>', views.timeout, name='timeout'),
    path('newdrink/<str:identifier>', views.newdrink, name='newdrink'),
    path('table/', views.allTables, name='allTables'),
    path('table/<str:identifier>', views.getTable, name='table'),
    path('table/<str:identifier>/coaster/<str:coasterId>/pay', views.tablePayCoaster, name='PayCoaster'),
    path('table/<str:identifier>/coaster/<str:coasterId>/delete', views.tableDeleteCoaster, name='DeleteCoaster'),
    path('table/<str:identifier>/coaster/<str:coasterId>/new/<str:beverageName>/<str:beverageEdition>',
         views.tableNewBeverage, name='AddToCoaster'),
]
