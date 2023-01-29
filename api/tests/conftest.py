import pytest

from django.contrib.auth.models import Permission

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient

from api.models import User, Curator, Student


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture(params=['admin_user', 'curator_user', 'student_user'])
def user_fixture(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user):
        token = AccessToken.for_user(user)
        return f'Bearer {token}'

    return _get_jwt_token


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        first_name='admin',
        last_name='admin',
        email='admin@mail.com',
        password='simbaLion228',
        is_admin=True
    )


@pytest.fixture
def curator_user():
    curator = Curator.objects.create(
        first_name='curator',
        last_name='curator',
        email='curator@mail.com',
        work_experience=1,
        post='teacher'
    )
    curator.set_password('simbaLion228')

    perms = Permission.objects.filter(
        codename__in=('change_student', 'change_studygroup')
    )
    curator.user_permissions.set(perms)

    curator.save()
    return curator


@pytest.fixture
def student_user():
    return Student.objects.create_user(
        first_name='student',
        last_name='student',
        email='student@mail.com',
        password="simbaLion228"
    )
