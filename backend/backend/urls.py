"""
URL configuration for backend project.

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
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from accounts.views import email_confirmation, reset_password_confirm, GoogleLogin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', email_confirmation),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('reset/password/confirm/<int:uid>/<str:token>', reset_password_confirm, name="password_reset_confirm"),
    path('api/', include('groups.urls')),
    path('api/', include('invitations.urls')),
    path('api/', include('transactions.urls')),
    path('api/', include('loan.urls')),
    path('api/', include('settlement.urls')),
    path('api/', include('goals.urls')),
    path('api/', include('calculator.urls')),
    # Spectacular Endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]