import pytest

from api.models import Specialty, Discipline

specialty_data = {
    "name": "testSpec"
}


@pytest.fixture
def another_specialty_data(curator_user, discipline_obj):
    cur = curator_user
    dis = discipline_obj
    return {
        "name": "anotherTestSpec",
        "curator": cur.id,
        "disciplines": [dis.id]
    }


url = '/specialties/'


# =================================LIST VIEW================================


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_create_specialty_authenticated(
        api_client,
        user,
        authenticate
):
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.post(
        path=url,
        data=specialty_data,
        format='json'
    )

    if user == 'admin_user':
        assert response.status_code == 201
        assert Specialty.objects.all().count() == 1
    else:
        assert response.status_code == 403
        assert Specialty.objects.all().count() == 0


# ================================DETAIL VIEW=================================
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_update_specialty_authenticated(
        api_client,
        user,
        authenticate,
        specialty_obj,
        another_specialty_data
):
    spec = specialty_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.put(
        path=url + f'{spec.id}/',
        data=another_specialty_data,
        format='json'
    )

    if user == 'admin_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['name'] == another_specialty_data['name']
        assert new_data['curator']['id'] == another_specialty_data['curator']

        dis_list = []
        for dis in new_data['disciplines']:
            dis_list.append(dis['id'])

        assert dis_list == another_specialty_data['disciplines']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_patch_specialty_authenticated(
        api_client,
        user,
        authenticate,
        specialty_obj,
        another_specialty_data
):
    spec = specialty_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{spec.id}/',
        data={"curator": another_specialty_data["curator"]},
        format='json'
    )

    if user == 'admin_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['curator']['id'] == another_specialty_data['curator']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_delete_specialty_authenticated(
        api_client,
        user,
        authenticate,
        specialty_obj
):
    spec = specialty_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.delete(path=url + f'{spec.id}/')

    if user == 'admin_user':
        assert response.status_code == 204
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_add_specialty_disciplines_authenticated(
        api_client,
        user,
        authenticate,
        specialty_obj
):
    dis1 = Discipline.objects.create(
        name="dis1",
        description="Tsdfsdfm"
    )
    dis2 = Discipline.objects.create(
        name="dis2",
        description="Tlore sksadm"
    )
    dis_list = [dis1.id, dis2.id]

    spec = specialty_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{spec.id}/' + 'add_disciplines/',
        data={"disciplines": dis_list}
    )

    if user == 'admin_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['disciplines'] == dis_list
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_remove_specialty_disciplines_authenticated(
        api_client,
        user,
        authenticate,
        specialty_obj
):
    dis1 = Discipline.objects.create(
        name="dis1",
        description="Tsdfsdfm"
    )
    dis2 = Discipline.objects.create(
        name="dis2",
        description="Tlore sksadm"
    )
    dis_list = [dis1.id, dis2.id]

    spec = specialty_obj
    spec.disciplines.set(dis_list)
    spec.save()

    token = authenticate(user)

    assert list(
        Specialty.objects.get(id=spec.id).disciplines.all()
    ) == [dis1, dis2]

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{spec.id}/' + 'remove_disciplines/',
        data={"disciplines": dis_list}
    )

    if user == 'admin_user':
        new_data = response.data
        assert response.status_code == 200

        assert new_data['disciplines'] == []
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_add_specialty_disciplines_authenticated_invalid_data(
        api_client,
        user,
        authenticate,
        specialty_obj
):
    spec = specialty_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{spec.id}/' + 'add_disciplines/',
        data={'disciplines': 'kek'}
    )

    if user == 'admin_user':
        assert response.status_code == 400
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_remove_specialty_disciplines_authenticated_invalid_data(
        api_client,
        user,
        authenticate,
        specialty_obj
):
    spec = specialty_obj
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{spec.id}/' + 'remove_disciplines/',
        data={'disciplines': 'kek'}
    )

    if user == 'admin_user':
        assert response.status_code == 400
    else:
        assert response.status_code == 403
