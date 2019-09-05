
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('get_details/',views.getdetails),
    path('search_restaurants/',views.searchrestaurants),
    path('show_cities/',views.showcities),
    path('data_page/',views.datapage, name='data_page'),
 
]