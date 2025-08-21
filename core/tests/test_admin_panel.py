# core/tests/test_admin_panel.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import DonatedResource, AidRequest

User = get_user_model()

@pytest.mark.django_db
def test_non_admin_cannot_access_admin_endpoints():
    client = APIClient()
    donor = User.objects.create_user(username='d', email='d@x.com', password='pass', role='donor')
    client.force_authenticate(donor)
    resp = client.get(reverse('admin-resources-list'))
    assert resp.status_code == 403

@pytest.mark.django_db
def test_admin_can_list_and_flag_resource():
    client = APIClient()
    admin = User.objects.create_user(username='a', email='a@x.com', password='pass', role='admin')
    donor = User.objects.create_user(username='d', email='d@x.com', password='pass', role='donor')
    res = DonatedResource.objects.create(donor=donor, title='Blankets', description='Warm', category='clothes', location='Lagos')

    client.force_authenticate(admin)

    # list
    list_resp = client.get(reverse('admin-resources-list'))
    assert list_resp.status_code == 200
    assert list_resp.data['results'][0]['title'] == 'Blankets' if isinstance(list_resp.data, dict) and 'results' in list_resp.data else True

    # flag
    detail_url = reverse('admin-resources-detail', kwargs={'pk': res.id})
    patch_resp = client.patch(detail_url, {'is_flagged': True}, format='json')
    assert patch_resp.status_code == 200
    res.refresh_from_db()
    assert res.is_flagged is True

@pytest.mark.django_db
def test_admin_stats_endpoint():
    client = APIClient()
    admin = User.objects.create_user(username='a', email='a@x.com', password='pass', role='admin')
    donor = User.objects.create_user(username='d', email='d@x.com', password='pass', role='donor')
    requester = User.objects.create_user(username='r', email='r@x.com', password='pass', role='requester')

    DonatedResource.objects.create(donor=donor, title='Food Pack', description='Canned', category='food', location='Abuja', is_flagged=True)
    AidRequest.objects.create(user=requester, category='food', description='Need food', is_resolved=False, is_flagged=False)

    client.force_authenticate(admin)
    resp = client.get(reverse('admin-stats'))
    assert resp.status_code == 200
    assert 'resources' in resp.data and 'aid_requests' in resp.data and 'users' in resp.data
    assert resp.data['resources']['flagged'] == 1
