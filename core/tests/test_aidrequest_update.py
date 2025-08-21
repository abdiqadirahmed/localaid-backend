import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import AidRequest

User = get_user_model()

@pytest.mark.django_db
def test_put_update_aid_request():
    client = APIClient()
    
    # Create user and authenticate
    user = User.objects.create_user(username="testuser", password="pass1234")
    client.force_authenticate(user=user)
    
    # Create AidRequest
    aid_request = AidRequest.objects.create(
        user=user,
        category="food",
        description="Need urgent food aid",
        is_resolved=False
    )

    # Full update using PUT
    url = f"/api/aid-requests/{aid_request.id}/"
    data = {
        "category": "water",
        "description": "Updated request for clean water",
        "is_resolved": True
    }
    response = client.put(url, data, format="json")

    assert response.status_code == 200
    assert response.data["category"] == "water"
    assert response.data["description"] == "Updated request for clean water"
    assert response.data["is_resolved"] is True


@pytest.mark.django_db
def test_patch_update_aid_request():
    client = APIClient()
    
    # Create user and authenticate
    user = User.objects.create_user(username="testuser2", password="pass1234")
    client.force_authenticate(user=user)
    
    # Create AidRequest
    aid_request = AidRequest.objects.create(
        user=user,
        category="shelter",
        description="Need temporary shelter",
        is_resolved=False
    )

    # Partial update using PATCH
    url = f"/api/aid-requests/{aid_request.id}/"
    data = {
        "is_resolved": True
    }
    response = client.patch(url, data, format="json")

    assert response.status_code == 200
    assert response.data["is_resolved"] is True
