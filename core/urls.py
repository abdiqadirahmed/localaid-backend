from django.urls import path
from django.http import HttpResponse
from .views import (
    AidRequestListCreateView,
    AidRequestDetailView,
    DonatedResourceListCreateView,
    DonatedResourceDetailView,

    AdminDonatedResourceListView,
    AdminDonatedResourceDetailView,
    AdminAidRequestListView,
    AdminAidRequestDetailView,
    AdminStatsView,
    
)

def test_view(request):
    return HttpResponse("Core app is working")

urlpatterns = [
    # puplic
    path('test/', test_view),
    path('aid-requests/', AidRequestListCreateView.as_view(), name='aid-request-list-create'),
    path('aid-requests/<int:pk>/', AidRequestDetailView.as_view(), name='aid-request-detail'),
    path('donated-resources/', DonatedResourceListCreateView.as_view(), name='donatedresource-list'),
    path('donated-resources/<int:pk>/', DonatedResourceDetailView.as_view(), name='donatedresource-detail'),
    

    # admin-only
    path('admin/resources/', AdminDonatedResourceListView.as_view(), name='admin-resources-list'),
    path('admin/resources/<int:pk>/', AdminDonatedResourceDetailView.as_view(), name='admin-resources-detail'),
    path('admin/aid-requests/', AdminAidRequestListView.as_view(), name='admin-aidrequests-list'),
    path('admin/aid-requests/<int:pk>/', AdminAidRequestDetailView.as_view(), name='admin-aidrequests-detail'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
]
