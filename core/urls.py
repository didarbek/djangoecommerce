from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home,name='home'),
    path('detail/',views.product_page,name='product_page'),
]