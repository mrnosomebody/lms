import pytest

from api.models import Curator

curator_data = {
    "first_name": "curator",
    "last_name": "curator",
    "email": "curator@mail.com",
    "password": "simbaLion228",
    "work_experience": 15,
    "post": "teacher"
}

another_curator_data = {
    "first_name": "another_curator",
    "last_name": "another_curator",
    "email": "another_curator@mail.com",
    "password": "simbaLion228",
    "work_experience": 15,
    "post": "teacher"
}

url = '/curators/'


# =================================LIST VIEW================================


@pytest.mark.django_db
def test_create_curator_unauthenticated(api_client):
    response = api_client.post(
        path=url,
        data=curator_data,
        format='json'
    )

    assert response.status_code == 401
    assert Curator.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_create_curator_authenticated(
        api_client,
        user,
        get_jwt_token,
        request
):
    current_user = request.getfixturevalue(user)
    token = get_jwt_token(current_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.post(
        path=url,
        data=curator_data,
        format='json'
    )

    if user == 'admin_user':
        assert response.status_code == 201
        assert Curator.objects.all().count() == 1
    elif user == 'curator_user':
        assert response.status_code == 403
        assert Curator.objects.all().count() == 1
    else:
        assert response.status_code == 403
        assert Curator.objects.all().count() == 0


@pytest.mark.django_db
def test_list_curators(api_client, curator_user):
    response = api_client.get(path=url)

    assert response.status_code == 200
    assert Curator.objects.all().count() == 1


# ================================DETAIL VIEW=================================

@pytest.mark.django_db
def test_retrieve_curator_unauthenticated(api_client, curator_user):
    cur = curator_user

    response = api_client.get(path=url + f'{cur.id}/')

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_retrieve_curator_authenticated(
        api_client,
        user,
        get_jwt_token,
        request,
        curator_user
):
    cur = curator_user
    current_user = request.getfixturevalue(user)
    token = get_jwt_token(current_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.get(path=url + f'{cur.id}/')

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('method', ['put', 'patch', 'delete'])
def test_unsafe_methods_curator_unauthenticated(
        api_client,
        curator_user,
        method
):
    cur = curator_user

    if method == 'put':
        response = api_client.put(path=url + f'{cur.id}/')
    elif method == 'patch':
        response = api_client.patch(path=url + f'{cur.id}/')
    elif method == 'delete':
        response = api_client.delete(path=url + f'{cur.id}/')

    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_update_curator_authenticated(
        api_client,
        user,
        get_jwt_token,
        request,
        curator_user
):
    cur = curator_user
    current_user = request.getfixturevalue(user)

    token = get_jwt_token(current_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.put(
        path=url + f'{cur.id}/',
        data=another_curator_data,
        format='json'
    )

    if user != 'student_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['email'] == another_curator_data['email']
        assert new_data['first_name'] == another_curator_data['first_name']
        assert new_data['last_name'] == another_curator_data['last_name']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_patch_curator_authenticated(
        api_client,
        user,
        get_jwt_token,
        request,
        curator_user
):
    cur = curator_user
    current_user = request.getfixturevalue(user)

    token = get_jwt_token(current_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{cur.id}/',
        data={"email": another_curator_data['email']},
        format='json'
    )

    if user != 'student_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['email'] == another_curator_data['email']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_delete_curator_authenticated(
        api_client,
        user,
        get_jwt_token,
        request,
        curator_user
):
    cur = curator_user
    current_user = request.getfixturevalue(user)

    token = get_jwt_token(current_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.delete(path=url + f'{cur.id}/')

    if user != 'student_user':
        assert response.status_code == 204
    else:
        assert response.status_code == 403
