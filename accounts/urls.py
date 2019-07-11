from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('login',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('activate_account',views.activate_account,name='activate_account'),
    path('login_r',views.login_r,name='login_r'),
    path('login_realtor',views.login_realtor,name='login_realtor'),
    path('register_r/',views.register_r,name='register_r'),

    path('register_realtor/',views.register_realtor,name='register_realtor'),
    path('register_listing/',views.register_listing,name='register_listing'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('dashboard_r',views.dashboard_r,name='dashboard_r'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate_account, name='activate'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)