"""inventoryProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mriic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admin-login/', views.login_request, name='login'),
    path('signup/', views.signup_request, name='signup'),
    path('logout/', views.logout_request, name='logout'),
    path('inventory/', views.inv, name='inv'),
    path('add-inventory/', views.item_add, name='image_upload'),
    path('edit-inventory/<int:Item_id>/', views.item_edit, name='item_edit'),
    path('borrow-request/<int:Item_id>/', views.borrow_request_create, name='borrow_request_create'),
    path('borrow-request/<int:request_id>/update/', views.borrow_request_update, name='borrow_request_update'),
    path('search-inventory/', views.search, name='search'),
    path('products/', views.filter_item, name='filter_item'),
    path('products/<int:Item_id>/', views.itemDesc, name='itemDesc'),
    path('<int:Item_id>/', views.itemDesc, name='itemDesc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
