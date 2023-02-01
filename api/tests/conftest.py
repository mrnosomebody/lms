import pytest

from django.contrib.auth.models import Permission

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient

from api.models import (
    User,
    Curator,
    Student,
    Discipline,
    Specialty,
    StudyGroup
)


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def authenticate(get_jwt_token, request):
    def _authenticate(user) -> str:
        current_user = request.getfixturevalue(user)
        token = get_jwt_token(current_user)
        return token

    return _authenticate


@pytest.fixture(params=['admin_user', 'curator_user', 'student_user'])
def user_fixture(request) -> User:
    return request.getfixturevalue(request.param)


@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user) -> str:
        token = AccessToken.for_user(user)
        return f'Bearer {token}'

    return _get_jwt_token


@pytest.fixture
def admin_user() -> User:
    return User.objects.create_user(
        first_name='admin1',
        last_name='admin1',
        email='admin1@mail.com',
        password='simbaLion228',
        is_admin=True
    )


@pytest.fixture
def curator_user() -> Curator:
    curator = Curator.objects.create(
        first_name='curator',
        last_name='curator',
        email='curator@mail.com',
        work_experience=1,
        post='teacher'
    )
    curator.set_password('simbaLion228')

    perms = Permission.objects.filter(
        codename__in=('change_student', 'add_studygroup', 'change_studygroup')
    )
    curator.user_permissions.set(perms)

    curator.save()
    return curator


@pytest.fixture
def student_user() -> Student:
    student = Student.objects.create(
        first_name='student',
        last_name='student',
        email='student@mail.com',
        sex='male'
    )
    student.set_password('simbaLion228')
    student.save()
    return student


@pytest.fixture
def discipline_obj() -> Discipline:
    return Discipline.objects.create(
        name="testBrat",
        description="Tri sestrizi pod oknom"
    )


@pytest.fixture
def specialty_obj() -> Specialty:
    return Specialty.objects.create(
        name="coolSpec"
    )


@pytest.fixture
def study_group_obj(specialty_obj) -> StudyGroup:
    return StudyGroup.objects.create(
        group_code="A322",
        specialty=specialty_obj
    )
