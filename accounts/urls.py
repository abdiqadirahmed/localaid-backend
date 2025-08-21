from django.urls import path
from .views import (
    RegisterView,
    ProtectedView,
    CustomTokenObtainPairView,
    UserProfileView,
    DonorOnlyView,
    AdminOnlyView,
    AidRequestListCreateView,

    AdminUserListView,
    AdminUserDetailView, 
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # auth/role routes...
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # Role based access URLs
    path('aid-requests/', AidRequestListCreateView.as_view(), name='aid_requests'),
    path('donor-only/', DonorOnlyView.as_view(), name='donor_only'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),

     # admin users
    path('admin/users/', AdminUserListView.as_view(), name='admin-users-list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-users-detail'),
    
]
