from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.ItemList.as_view(),name='home'),
    path('detail/<int:pk>/',views.product_detail,name='product_detail'),
    path('search/',views.SearchResultsView.as_view(),name='search_results'),
    path('cart/',views.OrderSummaryView.as_view(),name='cart'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('remove-single-item-from-cart/<int:pk>/',views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('profile/',views.profile,name='profile'),
    path('checkout/',views.CheckoutView.as_view(),name='checkoutpage'),
    path('account_update/',views.update_profile,name='account_update'),
    path('filter_search/',views.FilterView, name='filter_search'),
]