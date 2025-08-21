import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "strongpass123"
    }
    response = client.post(reverse('register'), data, format='json')
    assert response.status_code == 201
    assert User.objects.filter(email="testuser@example.com").exists()


@pytest.mark.django_db
def test_user_login_returns_token():
    # Create user with email and password
    User.objects.create_user(username="testuser", email="testuser@example.com", password="strongpass123")

    client = APIClient()
    login_data = {
        "email": "testuser@example.com",
        "password": "strongpass123"
    }
    response = client.post(reverse('token_obtain_pair'), login_data, format='json')
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert "user" in response.data


@pytest.mark.django_db
def test_access_protected_view_requires_auth():
    client = APIClient()
    response = client.get(reverse('protected'))
    assert response.status_code == 401  # Unauthorized


@pytest.mark.django_db
def test_access_protected_view_with_token():
    user = User.objects.create_user(username="testuser", email="testuser@example.com", password="strongpass123")

    client = APIClient()
    login_response = client.post(reverse('token_obtain_pair'), {
        "email": "testuser@example.com",
        "password": "strongpass123"
    }, format='json')
    token = login_response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(reverse('protected'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_profile_authenticated():
    user = User.objects.create_user(username="testuser", email="testuser@example.com", password="strongpass123")

    client = APIClient()
    login_response = client.post(reverse('token_obtain_pair'), {
        "email": "testuser@example.com",
        "password": "strongpass123"
    }, format='json')
    token = login_response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(reverse('user-profile'))
    assert response.status_code == 200
    assert response.data['email'] == "testuser@example.com"


@pytest.mark.django_db
def test_access_protected_view_requires_auth():
    client = APIClient()
    response = client.get(reverse('protected'))
    # Accept 401 Unauthorized or 403 Forbidden depending on your auth setup
    assert response.status_code in (401, 403)