from django.urls import path
from .views import ProductViewSet, AttributeViewSet, AttributeValueViewSet, SignupAPIView, LoginAPIView, UserProfileAPIView, DeleteAccountAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(),
         name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('delete/', DeleteAccountAPIView.as_view(), name='delete-account'),
    path('products/',
    ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('attributes/', AttributeViewSet.as_view(
    {'get': 'list', 'post': 'create'}), name='attribute-list'),
    path('attribute-values/', AttributeValueViewSet.as_view(
    {'get': 'list', 'post': 'create'}), name='attribute-value-list'),
        
]
