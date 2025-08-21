import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import DonatedResource
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.mark.django_db
class TestResourceSearch:

    @pytest.fixture
    def donor_user(self):
        user = User.objects.create_user(
            username='donor1',
            password='testpass',
            role='donor'
        )
        return user

    @pytest.fixture
    def api_client(self, donor_user):
        client = APIClient()
        refresh = RefreshToken.for_user(donor_user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    @pytest.fixture
    def resources(self, donor_user):
        return [
            DonatedResource.objects.create(
                donor=donor_user,
                title='Water Bottle',
                description='Clean drinking water',
                category='food',
                location='Hargeisa'
            ),
            DonatedResource.objects.create(
                donor=donor_user,
                title='Blanket',
                description='Warm blanket for winter',
                category='clothes',
                location='Burco'
            ),
            DonatedResource.objects.create(
                donor=donor_user,
                title='Hammer',
                description='Heavy duty hammer',
                category='tools',
                location='Hargeisa'
            ),
        ]

    def test_filter_by_category(self, api_client, resources):
        response = api_client.get('/api/donated-resources/', {'category': 'clothes'})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Blanket'

    def test_filter_by_location(self, api_client, resources):
        response = api_client.get('/api/donated-resources/', {'location': 'Hargeisa'})
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_search_title_description(self, api_client, resources):
        response = api_client.get('/api/donated-resources/', {'search': 'water'})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Water Bottle'

    def test_ordering_by_title(self, api_client, resources):
        response = api_client.get('/api/donated-resources/', {'ordering': 'title'})
        assert response.status_code == 200
        titles = [res['title'] for res in response.data]
        assert titles == sorted(titles)

    def test_ordering_by_created_at_desc(self, api_client, resources):
        response = api_client.get('/api/donated-resources/', {'ordering': '-created_at'})
        assert response.status_code == 200
        # Newest resource first
        assert response.data[0]['title'] == 'Hammer'
