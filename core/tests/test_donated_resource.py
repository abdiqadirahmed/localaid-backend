import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import DonatedResource

User = get_user_model()

@pytest.mark.django_db
def test_donor_can_post_donated_resource():
    client = APIClient()
    donor = User.objects.create_user(username='donordonor', password='testpass123', role='donor')
    client.force_authenticate(user=donor)

    response = client.post('/api/donated-resources/', {
        'title': 'Tents',
        'description': 'Weather-proof tents',
        'category': 'other',
        'location': 'Camp Alpha'
    }, format='json')

    assert response.status_code == 201
    assert DonatedResource.objects.count() == 1
    assert DonatedResource.objects.first().title == 'Tents'

@pytest.mark.django_db
def test_requester_cannot_post_donated_resource():
    client = APIClient()
    requester = User.objects.create_user(username='requesterguy', password='testpass123', role='requester')
    client.force_authenticate(user=requester)

    response = client.post('/api/donated-resources/', {
        'title': 'Shoes',
        'description': 'New shoes',
        'category': 'clothes',
        'location': 'Camp B'
    }, format='json')

    assert response.status_code == 403  # Forbidden
    assert DonatedResource.objects.count() == 0
