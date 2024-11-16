from django.urls import path
from .views import ProductViewSet, SignupAPIView, LoginAPIView, UserProfileAPIView, DeleteAccountAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(),
         name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('delete/', DeleteAccountAPIView.as_view(), name='delete-account'),

    path('products/create/', ProductViewSet.as_view(), name='product-create'),
    path('products/', ProductViewSet.as_view(), name='product-list'),
    path('products/add-stock/', ProductViewSet.as_view(), name='product-add-stock'),
    path('products/remove-stock/', ProductViewSet.as_view(), name='product-remove-stock'),
]
