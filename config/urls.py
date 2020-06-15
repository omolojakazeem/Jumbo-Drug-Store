from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

from .views import index,dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('allauth.urls')),
    path('drugs/', include('drugs.urls')),
    path('customers/', include('customers.urls')),
    path('expenses/', include('expenses.urls')),
    path('orders/', include('order.urls')),
    path('payment/', include('payment.urls')),

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.png')))

]
