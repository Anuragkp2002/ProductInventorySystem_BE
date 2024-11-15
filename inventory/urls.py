from django.urls import path
from .views import SignupAPIView, LoginAPIView, UserProfileAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(),
         name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
        
]
