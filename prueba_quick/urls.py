from django.urls import path
from api.api import UserAPI
from api.views import Login
from api.views import Logout
from rest_framework.authtoken import views
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create_user/1.0/', UserAPI.as_view(), name="create_user"),
    path('api_generate_token/', views.obtain_auth_token),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', include('api.urls')),
]