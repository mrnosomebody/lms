import pytest

from api.models import StudyGroup

url = '/study-groups/'


@pytest.fixture
def study_group_data(specialty_obj) -> dict:
    spec = specialty_obj
    return {
        "group_code": "A322",
        "specialty": spec.id
    }


@pytest.fixture
def another_study_group_data(specialty_obj) -> dict:
    spec = specialty_obj
    return {
        "group_code": "B228",
        "specialty": spec.id
    }


# =================================LIST VIEW================================

@pytest.mark.django_db
@pytest.mark.parametrize(
    'user',
    ['admin_user', 'curator_user', 'student_user']
)
def test_create_study_group_authenticated(
        api_client,
        user,
        authenticate,
        study_group_data
):
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.post(
        path=url,
        data=study_group_data,
        format='json'
    )

    if user == 'curator_user':
        assert response.status_code == 201
        assert StudyGroup.objects.all().count() == 1
    else:
        assert response.status_code == 403
        assert StudyGroup.objects.all().count() == 0


# ================================DETAIL VIEW=================================
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_update_study_group_authenticated(
        api_client,
        user,
        authenticate,
        study_group_obj,
        another_study_group_data
):
    stg = study_group_obj
    new_stg_data = another_study_group_data
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.put(
        path=url + f'{stg.id}/',
        data=new_stg_data,
        format='json'
    )

    if user == 'curator_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['group_code'] == new_stg_data['group_code']
        assert new_data['specialty']['id'] == new_stg_data['specialty']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_patch_study_group_authenticated(
        api_client,
        user,
        authenticate,
        study_group_obj,
        another_study_group_data
):
    stg = study_group_obj
    new_stg_data = another_study_group_data
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{stg.id}/',
        data={"group_code": new_stg_data['group_code']},
        format='json'
    )

    if user == 'curator_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['group_code'] == new_stg_data['group_code']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_delete_study_group_authenticated(
        api_client,
        user,
        authenticate,
        study_group_obj
):
    stg = study_group_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.delete(path=url + f'{stg.id}/')

    if user == 'curator_user':
        assert response.status_code == 204
    else:
        assert response.status_code == 403
