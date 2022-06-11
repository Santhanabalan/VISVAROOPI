from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('innerpage/', views.innerpage, name='innerpage'),
    path('login/', views.login, name='login'),
    path('portfolio/', views.portfolio, name='portfolio'),
]