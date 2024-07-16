from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testdata', views.overviewTest, name='testdata'),
    path('level/<str:identifier>/<int:glass_level>', views.level, name='level'),
    path('overview/', views.overview, name='overview'),
    path('timeout/<str:identifier>/<str:tableId>', views.timeout, name='timeout'),
    path('newdrink/<str:identifier>/<str:tableId>', views.newdrink, name='newdrink'),
    path('table/', views.allTables, name='allTables'),
    path('table/<str:identifier>', views.getTable, name='table'),
    path('table/<str:identifier>/group', views.getTableGroupOrder, name='tableGroupOrder'),
    path('table/<str:identifier>/round', views.getTableBuyARound, name='tableBuyARound'),
    path('table/<str:identifier>/coaster/<str:coasterId>/pay', views.tablePayCoaster, name='PayCoaster'),
    path('table/<str:identifier>/pay', views.tablePayTable, name='PayTable'),
    path('table/<str:identifier>/coaster/<str:coasterId>/delete', views.tableDeleteCoaster, name='DeleteCoaster'),
    path('table/<str:identifier>/coaster/<str:coasterId>/new/<str:beverageName>/<str:beverageEdition>',
         views.tableNewBeverage, name='AddToCoaster'),
    path('table/<str:identifier>/coaster/<str:coasterId>/newfood/<str:foodName>/',
         views.tableNewFood, name='AddToFoodCoaster'),
    path('table/<str:identifier>/coaster/<str:coasterId>/new/multi',
         views.tableNewBeverageMulti, name='AddToCoasterMulti'),
    path('table/<str:identifier>/coaster/<str:coasterId>/new/multifood',
         views.tableNewFoodMulti, name='AddToCoasterMultiFood'),
    path('lastBeverages/<str:identifier>/delete', views.newDrinksDeleteLatest, name='newDrinksDeleteLatest'),
    path('table/<str:identifier>/group/order/', views.groupOrder, name='groupOrder'),
    path('table/<str:identifier>/round/order/', views.rundeAusgeben, name='rundeAusgeben'),
    path('table/<str:identifier>/subgroup/', views.getSubGroups, name='getSubGroups'),
    path('table/<str:identifier>/subgroup/new/', views.createSubGroup, name='createSubGroup'),
    path('table/<str:identifier>/subgroup/delete/', views.subGroupDelete, name='subGroupDelete'),
    path('table/<str:identifier>/subgroup/pay/', views.tablePayTempGroup, name='tablePayTempGroup'),
    path('table/<str:identifier>/subgroup/paydelete/', views.tablePayAndDeleteTempGroup, name='tablePayAndDeleteTempGroup'),
    path('table/<str:identifier>/undo/', views.coasterUndo, name='coasterUndo'),

    path('admin/sumup', views.sumup, name="sumup")
]
