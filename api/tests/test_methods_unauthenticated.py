import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/curators/',
    '/study-groups/',
    '/disciplines/',
    '/specialties/',
])
def test_create_methods_unauthenticated(api_client, url):
    response = api_client.post(
        path=url,
        data={}
    )

    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/curators/',
    '/study-groups/',
    '/disciplines/',
    '/specialties/',
    '/students/',
])
def test_lists(api_client, url):
    response = api_client.get(path=url)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url, obj', [
    ('/curators/', 'curator_user'),
    ('/students/', 'student_user'),
    ('/study-groups/', 'study_group_obj'),
    ('/disciplines/', 'discipline_obj'),
    ('/specialties/', 'specialty_obj')
])
def test_retrieves_unauthenticated(api_client, obj, url, request):
    current_obj = request.getfixturevalue(obj)

    response = api_client.get(path=url + f'{current_obj.id}/')

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url, obj', [
    ('/curators/', 'curator_user'),
    ('/students/', 'student_user'),
    ('/study-groups/', 'study_group_obj'),
    ('/disciplines/', 'discipline_obj'),
    ('/specialties/', 'specialty_obj')
])
@pytest.mark.parametrize('method', ['put', 'patch', 'delete'])
def test_unsafe_methods_unauthenticated(
        api_client,
        obj,
        url,
        method,
        request
):
    current_obj = request.getfixturevalue(obj)

    if method == 'put':
        response = api_client.put(path=url + f'{current_obj.id}/')
    elif method == 'patch':
        response = api_client.patch(path=url + f'{current_obj.id}/')
    elif method == 'delete':
        response = api_client.delete(path=url + f'{current_obj.id}/')

    assert response.status_code == 401
