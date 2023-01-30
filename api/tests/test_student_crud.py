import pytest

from api.models import Student, StudyGroup

student_data = {
    "first_name": "student",
    "last_name": "student",
    "email": "student@mail.com",
    "password": "simbaLion228",
    "sex": 'female'
}


@pytest.fixture
def another_student_data(specialty_obj):
    stg = StudyGroup.objects.create(
        group_code="G2B4",
        specialty=specialty_obj,
        max_students=1
    )
    return {
        "first_name": "another_student",
        "last_name": "another_student",
        "email": "another_student@mail.com",
        "password": "simbaLion228",
        "sex": 'male',
        "study_group": stg.id
    }


url = '/students/'


# =================================LIST VIEW================================
@pytest.mark.django_db
def test_create_student(api_client):
    response = api_client.post(
        path=url,
        data=student_data
    )

    assert response.status_code == 201
    assert Student.objects.all().count() == 1


# ================================DETAIL VIEW=================================

@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_update_student_authenticated(
        api_client,
        user,
        authenticate,
        student_user,
        another_student_data
):
    stud = student_user
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.put(
        path=url + f'{stud.id}/',
        data=another_student_data,
        format='json'
    )

    if user != 'curator_user':
        new_data = response.data
        assert response.status_code == 200
        assert new_data['email'] == another_student_data['email']
        assert new_data['first_name'] == another_student_data['first_name']
        assert new_data['last_name'] == another_student_data['last_name']
        assert new_data['sex'] == another_student_data['sex']
        assert new_data['study_group'] == another_student_data['study_group']
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_patch_student_authenticated(
        api_client,
        user,
        authenticate,
        student_user,
        another_student_data,
        curator_user
):
    """
    Curator user does not manage the specialty to which group is
    related. So he cannot add user there as well as other users
    """
    stud = student_user
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{stud.id}/',
        data={"study_group": another_student_data['study_group']},
        format='json'
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_patch_student_when_curator_manages_related_specialty_authenticated(
        api_client,
        get_jwt_token,
        student_user,
        another_student_data,
        curator_user,
        specialty_obj
):
    """
    Curator user manages the specialty to which group is
    related. So he cannot add user there as well as other users
    """
    stud = student_user
    cur = curator_user
    spec = specialty_obj

    # set curator for the specialty
    spec.curator = cur
    spec.save()

    token = get_jwt_token(cur)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.patch(
        path=url + f'{stud.id}/',
        data={"study_group": another_student_data['study_group']},
        format='json'
    )

    assert response.status_code == 200
    assert response.data['study_group'] == another_student_data['study_group']

    # =========ADDING_USER_TO_GROUP_WHEN_HE_ALREADY_IN_GROUP===========

    response = api_client.patch(
        path=url + f'{stud.id}/',
        data={"study_group": another_student_data['study_group']},
        format='json'
    )

    assert response.data[0] == 'User is already in the group'

    # =========MAX_STUDENTS_LIMIT_TEST===========

    student = Student.objects.create(
        first_name='student',
        last_name='student',
        email='student1@mail.com',
        sex='male'
    )
    student.set_password('simbaLion228')
    student.save()

    response = api_client.patch(
        path=url + f'{student.id}/',
        data={"study_group": another_student_data['study_group']},
        format='json'
    )

    assert response.data[0] == 'Max amount of students in this group exceeded'

    response = api_client.patch(
        path=url + f'{stud.id}/',
        data={},
        format='json'
    )
    print(response.data)
    assert response.data['study_group'] is None


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user",
    ['admin_user', 'curator_user', 'student_user']
)
def test_delete_curator_authenticated(
        api_client,
        user,
        authenticate,
        student_user
):
    stud = student_user
    token = authenticate(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.delete(path=url + f'{stud.id}/')

    if user != 'curator_user':
        assert response.status_code == 204
    else:
        assert response.status_code == 403
