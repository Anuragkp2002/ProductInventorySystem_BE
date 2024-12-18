"""
URL configuration for inventory_system project.

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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Define the Bearer token security parameter for Swagger UI
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Inventory API",
#         default_version="v1",
#         description="API documentation for Inventory system",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="support@example.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     # Optional if you want to require authentication
#     permission_classes=(IsAuthenticated,),
#     authentication_classes=[JWTAuthentication],  # Global JWT Authentication
#     security=[{'Bearer': []}]  # Ensure that Bearer is required in Swagger UI
# )

schema_view = get_schema_view(
    openapi.Info(
        title="DRF Tutorial  API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='swagger-ui'),
]
