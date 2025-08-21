import pytest
from rest_framework.test import APIClient
from accounts.models import User
from core.models import DonatedResource
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_location_filtering():
    # Create a donor user
    user = User.objects.create_user(username='donor1', password='pass123', role='donor')
    DonatedResource.objects.create(donor=user, title="Water Pack", description="Clean water", category="food", location="Abuja")
    DonatedResource.objects.create(donor=user, title="Food Pack", description="Dry food", category="food", location="Lagos")
    
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    # Filter by location
    response = client.get('/api/donated-resources/?location=Abuja')
    assert response.status_code == 200
    assert all(resource['location'] == 'Abuja' for resource in response.data)
