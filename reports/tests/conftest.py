import pytest
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient

from api.models import User


@pytest.fixture()
def celery_config():
    return {
        'broker_url': 'redis://0.0.0.0:6379/0',
        'result_backend': 'redis://0.0.0.0:6379/0',
    }


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user) -> str:
        token = AccessToken.for_user(user)
        return f'Bearer {token}'

    return _get_jwt_token


@pytest.fixture
def admin_user() -> User:
    return User.objects.create_user(
        first_name='admin',
        last_name='admin',
        email='admin@mail.com',
        password='simbaLion228',
        is_admin=True
    )
