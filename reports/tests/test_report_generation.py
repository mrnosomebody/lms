import pytest


@pytest.mark.django_db
def test_generate_report_unauthenticated(
        celery_app,
        celery_worker,
        api_client
):
    response = api_client.post('/reports/')

    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_generate_report_authenticated(
        celery_app,
        celery_worker,
        api_client,
        get_jwt_token,
        admin_user
):
    token = get_jwt_token(admin_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')
    response = api_client.post('/reports/')

    assert response.status_code == 200
    assert response.data.get('task_id') is not None


@pytest.mark.django_db(transaction=True)
def test_get_task_status_authenticated(
        celery_app,
        celery_worker,
        api_client,
        get_jwt_token,
        admin_user
):
    token = get_jwt_token(admin_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'{token}')

    task_id = api_client.post('/reports/').data.get('task_id')

    response = api_client.get('/tasks/' + task_id + '/')

    assert response.status_code == 200
    assert response.data.get('status') is not None
