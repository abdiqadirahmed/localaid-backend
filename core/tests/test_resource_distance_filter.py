import pytest
from core.models import DonatedResource
from accounts.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_distance_filter():
    donor = User.objects.create_user(username='donor1', password='pass', role='donor')
    resource1 = DonatedResource.objects.create(
        donor=donor, title='Water', description='Clean water', category='food',
        location='CityA', latitude=10.0, longitude=10.0
    )
    resource2 = DonatedResource.objects.create(
        donor=donor, title='Food', description='Canned food', category='food',
        location='CityB', latitude=20.0, longitude=20.0
    )

    client = APIClient()
    client.force_authenticate(user=donor)

    response = client.get('/api/donated-resources/?latitude=10&longitude=10&radius=1500')
    assert response.status_code == 200
    data = response.json()
    assert any(r['title'] == 'Water' for r in data)
    assert not any(r['title'] == 'Food' for r in data)
