from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from core.models import AidRequest
from core.serializers import AidRequestSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.permissions import IsAdmin
from .serializers import AdminUserSerializer

from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
)
from .permissions import IsRequester, IsDonor, IsAdmin

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Authenticated user",
            "user": request.user.email
        })


# Example: Only Requesters can create and list AidRequests
class AidRequestListCreateView(generics.ListCreateAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsRequester]

    def get_queryset(self):
        if self.request.user.is_staff:
            return AidRequest.objects.all()
        return AidRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Example view only accessible by Donors
class DonorOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsDonor]

    def get(self, request):
        return Response({
            "message": "Hello Donor! You can access donor-only resources here."
        })


# Example view only accessible by Admins
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({
            "message": "Hello Admin! You have full access."
        })


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']


class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]