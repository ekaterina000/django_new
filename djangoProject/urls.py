"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

from FirstProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name='info'),
    path('showresident/<int:id_user>/', views.show_resident, name='show_resident'),
    path('governmentView/<str:name_city>/<int:id_district>/<int:id_user>/addhousing/', views.create_housing,
         name='create_housing'),
    path('governmentView/<str:name_city>/<int:id_district>/<int:id_user>/<int:area_housing>/deletehousing/',
         views.delete_housing, name='delete_housing'),
    path('', views.show_index, name='home'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('user_logout/', views.logout_user, name='logout_user'),
    path('register_resident/', views.register_resident, name='register_resident'),

    path('governmentView/<str:name_city>/', views.show_district_ofCity, name='resident_ofCities'),
    path('governmentView/<str:name_city>/<int:id_district>/', views.show_residentFromDistrict,
         name='resident_fromDistrict'),
    path('governmentView/<str:name_city>/<int:id_district>/<int:id_user>/', views.show_residentFromGovernment,
         name='show_residentFromGovernment'),

    path('ajax/validate_username', views.validate_username, name='validate_username'),
    path('ajax/validate_email', views.validate_email, name='validate_email')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


