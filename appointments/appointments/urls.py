"""
URL configuration for appointments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Home.urls")),
    path('accounts/', include("accounts.urls")),
    path('professionals/', include("professionals.urls")),
    path('bookings/', include("bookings.urls")),
    
    # Legacy URLs for backward compatibility (will redirect to new structure)
    path('usersignup/', include("UserSignup.urls")),
    path('adminlogin/', include("AdminLogin.urls")),
    path('adminsignup/', include("AdminSignup.urls")),
    path('userlogin/', include("UserLogin.urls")),
    path('userhome/', include("UserHome.urls")),
    path('bookingpage/', include("BookingPage.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
