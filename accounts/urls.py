from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/',views.register,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),   
    ]
