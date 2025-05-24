from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView, VerifyTokenView, UserListView, UserToggleStatusView, UserDetailView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify_token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<str:pk>/toggle-status/', UserToggleStatusView.as_view(), name='user-toggle-status'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
]
