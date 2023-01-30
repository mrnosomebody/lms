import pytest

from api.models import Discipline

discipline_data = {
    "name": "testBrat",
    "description": "Tri sestrizi pod oknom"
                   " pryali pozdno vecherkom"
}

another_discipline_data = {
    "name": "anotherBrat",
    "description": "Dve sestrizi pod oknom"
                   " pryali pozdno vecherkom"
}

url = '/disciplines/'


# =================================LIST VIEW================================

@pytest.mark.django_db
@pytest.mark.parametrize(
    'user',
    ['admin_user', 'curator_user', 'student_user']
)
def test_create_discipline_authenticated(api_client, user, authenticate):
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.post(
        path=url,
        data=discipline_data,
        format='json'
    )

    if user == 'admin_user':
        assert response.status_code == 201
        assert Discipline.objects.all().count() == 1
    else:
        assert response.status_code == 403
        assert Discipline.objects.all().count() == 0


# ================================DETAIL VIEW=================================


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_update_discipline_authenticated(
        api_client,
        user,
        authenticate,
        discipline_obj
):
    dis = discipline_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.put(
        path=url + f'{dis.id}/',
        data=another_discipline_data,
        format='json'
    )

    if user == 'admin_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['name'] == another_discipline_data['name']
        assert new_data['description'] == \
               another_discipline_data['description']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_patch_discipline_authenticated(
        api_client,
        user,
        authenticate,
        discipline_obj
):
    dis = discipline_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{dis.id}/',
        data={"name": another_discipline_data['name']},
        format='json'
    )

    if user == 'admin_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['name'] == another_discipline_data['name']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_delete_discipline_authenticated(
        api_client,
        user,
        authenticate,
        discipline_obj
):
    dis = discipline_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.delete(path=url + f'{dis.id}/')

    if user == 'admin_user':
        assert response.status_code == 204
    else:
        assert response.status_code == 403
