from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer
from django.http import JsonResponse
from .models import AidRequest
from .serializers import AidRequestSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from .models import DonatedResource
from .serializers import DonatedResourceSerializer
from accounts.permissions import IsDonor
from rest_framework.exceptions import PermissionDenied
from .permissions import IsDonorOrReadOnly
from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.views import APIView



from accounts.permissions import IsAdmin  
from .models import AidRequest, DonatedResource
from .serializers import (
    AidRequestSerializer,
    AidRequestAdminSerializer,
    DonatedResourceSerializer,
    DonatedResourceAdminSerializer,
)



def home(request):
    return JsonResponse({"message": "Welcome to LocalAid API!"})


class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class AidRequestListCreateView(generics.ListCreateAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields to filter by exact match
    filterset_fields = ['category', 'is_resolved']
    
    # Fields to search in (partial text match)
    search_fields = ['description']
    
    # Fields allowed for ordering results
    ordering_fields = ['created_at', 'category']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return AidRequest.objects.all()
        return AidRequest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AidRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return AidRequest.objects.all()
        return AidRequest.objects.filter(user=self.request.user)


class DonatedResourceListCreateView(generics.ListCreateAPIView): 
    queryset = DonatedResource.objects.all()
    serializer_class = DonatedResourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsDonor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location']  # exact match filters
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Distance filtering
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')  # in km

        if lat and lng and radius:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)

            # Haversine formula approximation using Django ORM
            queryset = queryset.annotate(
                distance=6371 * ACos(
                    Cos(Radians(lat)) * Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - Radians(lng)) +
                    Sin(Radians(lat)) * Sin(Radians(F('latitude')))
                )
            ).filter(distance__lte=radius)

        return queryset

    def perform_create(self, serializer):
        if self.request.user.role != 'donor':
            raise PermissionDenied("Only donors can post resources.")
        serializer.save(donor=self.request.user)



class DonatedResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DonatedResource.objects.all()
    serializer_class = DonatedResourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsDonorOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user.role != 'donor':
            raise PermissionDenied("Only donors can update resources.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.donor:
            raise PermissionDenied("You can only delete your own resource.")
        instance.delete()


# ========= Admin: Donated Resources =========
class AdminDonatedResourceListView(generics.ListAPIView):
    queryset = DonatedResource.objects.all().order_by('-created_at')
    serializer_class = DonatedResourceAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'category']
    ordering_fields = ['created_at', 'category']


class AdminDonatedResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DonatedResource.objects.all()
    serializer_class = DonatedResourceAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


# ========= Admin: Aid Requests =========
class AdminAidRequestListView(generics.ListAPIView):
    queryset = AidRequest.objects.all().order_by('-created_at')
    serializer_class = AidRequestAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'category', 'user__email']
    ordering_fields = ['created_at', 'category']


class AdminAidRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


# ========= Admin: Usage Stats =========
class AdminStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        User = get_user_model()

        stats = {
            "resources": {
                "total": DonatedResource.objects.count(),
                "flagged": DonatedResource.objects.filter(is_flagged=True).count(),
                "claimed": DonatedResource.objects.filter(is_claimed=True).count(),
            },
            "aid_requests": {
                "total": AidRequest.objects.count(),
                "flagged": AidRequest.objects.filter(is_flagged=True).count(),
                "unresolved": AidRequest.objects.filter(is_resolved=False).count(),
            },
            "users": {
                "total": User.objects.count(),
                "by_role": {
                    "admin": User.objects.filter(role='admin').count(),
                    "donor": User.objects.filter(role='donor').count(),
                    "requester": User.objects.filter(role='requester').count(),
                }
            }
        }
        return Response(stats)
