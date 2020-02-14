from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.ItemList.as_view(),name='home'),
    path('detail/<int:pk>/',views.product_detail,name='product_detail'),
    path('cart/',views.cart,name='cart'),
    path('profile/',views.profile,name='profile'),
    path('account_update/',views.update_profile,name='account_update'),
    path('filter_search/',views.FilterView, name='filter_search'),
]