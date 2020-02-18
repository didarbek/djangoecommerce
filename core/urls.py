from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.ItemList.as_view(),name='home'),
    path('men/', views.MenItemList.as_view(), name='men_form'),
    path('women/', views.WomenItemList.as_view(), name='women_form'),
    path('sale/', views.SaleItemList.as_view(), name='sale_form'),
    path('category/shoes/', views.ShoesView.as_view(), name='category_shoes'),    
    path('category/clothes/', views.ClothesView.as_view(), name='category_clothes'),    
    path('category/accessories/', views.AccessoriesView.as_view(), name='category_accessories'), 
    path('detail/<int:pk>/',views.product_detail,name='product_detail'),
    path('cart/',views.OrderSummaryView.as_view(),name='cart'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('remove-single-item-from-cart/<int:pk>/',views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('checkout/',views.CheckoutView.as_view(),name='checkoutpage'),
    path('payment/<payment_option>/',views.PaymentView.as_view(),name='payment'),
    path('profile/',views.profile,name='profile'),
    path('account_update/',views.update_profile,name='account_update'),
    path('search/',views.SearchResultsView.as_view(),name='search_results'),
    path('filter_search/',views.FilterView, name='filter_search'),
    path('comment/<int:pk>/delete/',views.delete_own_comment,name='comment_delete'),
]