import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_donor_can_post_donated_resource():
    client = APIClient()
    donor = User.objects.create_user(username="donoruser", email="donor@example.com", password="testpass", role="donor")
    client.force_authenticate(user=donor)

    url = reverse('donatedresource-list')  # Update this with your url name for list-create
    data = {
        "title": "Food Package",
        "description": "Canned food for refugees",
        "category": "food",
        "location": "Camp 1"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_non_donor_cannot_post_donated_resource():
    client = APIClient()
    requester = User.objects.create_user(username="requesteruser", email="req@example.com", password="testpass", role="requester")
    client.force_authenticate(user=requester)

    url = reverse('donatedresource-list')  # Update this with your url name
    data = {
        "title": "Food Package",
        "description": "Canned food for refugees",
        "category": "food",
        "location": "Camp 1"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_requester_can_post_aid_request():
    client = APIClient()
    requester = User.objects.create_user(username="requesteruser", email="req@example.com", password="testpass", role="requester")
    client.force_authenticate(user=requester)

    url = reverse('aid_requests')  # Update with your url name for aid request list-create
    data = {
        "category": "food",
        "description": "Need rice and beans",
        "is_resolved": False
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_non_requester_cannot_post_aid_request():
    client = APIClient()
    donor = User.objects.create_user(username="donoruser", email="donor@example.com", password="testpass", role="donor")
    client.force_authenticate(user=donor)

    url = reverse('aid_requests')
    data = {
        "category": "food",
        "description": "Need rice and beans",
        "is_resolved": False
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 403
