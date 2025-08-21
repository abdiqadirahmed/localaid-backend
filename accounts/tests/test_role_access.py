import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import AidRequest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register_login_and_role_access():
    client = APIClient()

    # Register users with different roles
    admin_user = User.objects.create_user(username="admin", email="admin@example.com", password="pass1234", role="admin")
    donor_user = User.objects.create_user(username="donor", email="donor@example.com", password="pass1234", role="donor")
    requester_user = User.objects.create_user(username="requester", email="requester@example.com", password="pass1234", role="requester")

    # Helper to login and return access token
    def login(email, password):
        url = reverse('token_obtain_pair')
        response = client.post(url, {'email': email, 'password': password}, format='json')
        assert response.status_code == 200
        return response.data['access']

    admin_token = login(admin_user.email, "pass1234")
    donor_token = login(donor_user.email, "pass1234")
    requester_token = login(requester_user.email, "pass1234")

    # Test admin-only access
    url_admin = reverse('admin_only')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
    response = client.get(url_admin)
    assert response.status_code == 200
    assert 'Hello Admin!' in response.data['message']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + donor_token)
    response = client.get(url_admin)
    assert response.status_code == 403  # donor should be forbidden

    # Test donor-only access
    url_donor = reverse('donor_only')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + donor_token)
    response = client.get(url_donor)
    assert response.status_code == 200
    assert 'Hello Donor!' in response.data['message']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + requester_token)
    response = client.get(url_donor)
    assert response.status_code == 403  # requester forbidden here

    # Test aid-request creation allowed only for requester role
    url_aid = reverse('aid_requests')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + requester_token)
    data = {
        "category": "food",
        "description": "Need food supplies",
        "is_resolved": False
    }
    response = client.post(url_aid, data, format='json')
    assert response.status_code == 201

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + donor_token)
    response = client.post(url_aid, data, format='json')
    assert response.status_code == 403

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
    response = client.post(url_aid, data, format='json')
    assert response.status_code == 403
