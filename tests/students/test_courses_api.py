import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(api_client, course_factory):
    course = course_factory(_quantity=1)
    response = api_client.get(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1


@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    courses = course_factory(_quantity=10)
    response = api_client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['id'] == courses[i].id


@pytest.mark.django_db
def test_get_course_filter_id(api_client, course_factory):
    courses = course_factory(_quantity=10)
    #response = api_client.get(f'/api/v1/courses/?id={courses[2].id}')
    response = api_client.get('/api/v1/courses/', {'id': courses[2].id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 3


@pytest.mark.django_db
def test_create_course(api_client, course_factory, student_factory):
    count = Course.objects.count()
    response = api_client.post(
        '/api/v1/courses/',
        data={'name': 'course1', 'students': []},
        format='json'
    )
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_change_course(api_client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    new_name = 'new_course_name'
    response = api_client.patch(
        f'/api/v1/courses/{course[0].id}/',
        data={'name': new_name},
        format='json'
    )
    assert response.status_code == 200
    assert response.json()['name'] == new_name #можно проверить сразу
    result = api_client.get(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 200
    assert result.json()['name'] == new_name  # или сделать get запрос


@pytest.mark.django_db
def test_delete_course(api_client, course_factory, student_factory, count=2):
    course = course_factory(_quantity=count)
    response = api_client.delete(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1


@pytest.mark.django_db
def test_course_is_full(course_factory, student_factory, settings):
    students = student_factory(_quantity=settings.MAX_STUDENTS_PER_COURSE - 1)
    course = course_factory(name='Math', students=students)
    assert course.is_full()


@pytest.mark.django_db
def test_course_not_full(course_factory, student_factory, settings):
    students = student_factory(_quantity=settings.MAX_STUDENTS_PER_COURSE - 1)
    course = course_factory(name='Math', students=students)
    assert not course.is_full()
