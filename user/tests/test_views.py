import pytest
from django.urls import reverse


@pytest.mark.slow
def test_login_page(client):
    url = reverse('user:login')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Login</h1>' in response.content.decode('UTF-8')
