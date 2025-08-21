import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import DonatedResource
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_donated_resource():
    client = APIClient()
    response = client.post('/api/donated-resources/', {
        'resource_type': 'water',
        'quantity': 10,
        'donated_by': 'SomeOrg'
    })
    assert response.status_code == 403

@pytest.mark.django_db
def test_authenticated_user_can_create_donated_resource():
    user = User.objects.create_user(
        username='testuser',
        password='testpass',
        role='donor'
    )

    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    # 👇 Update this payload to match your serializer/model
    payload = {
        'title': 'Water Filter',
        'description': 'Portable water filtration device',
        'category': 'tools',
        'location': 'Abuja'
    }

    response = client.post('/api/donated-resources/', payload)

    print("Response data:", response.data)  # 🔍 Add this line if needed to debug

    assert response.status_code == 201