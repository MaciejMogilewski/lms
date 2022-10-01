import io

import pytest
from PIL import Image
from django.contrib.auth.models import Permission, Group

from courses.models import Subject


@pytest.fixture(scope='function')
def password():
    return 'TestPass12#'


@pytest.fixture(scope='function')
def email():
    return 'a@a.pl'


@pytest.fixture(scope='function')
def user(db, django_user_model, email, password):
    """User instance from default django user model"""
    yield django_user_model.objects.create_user(email=email, fullname='Sasin', password=password)


@pytest.fixture(scope='function')
def user_instructor(db, django_user_model, email, password):
    """User instance from default django user model with instructor permissions"""
    user = django_user_model.objects.create_user(email=email, fullname='Sasin', password=password)
    permission = Permission.objects.get(name='Can add course')
    instructor_group = Group.objects.get(name='instructors')
    user.groups.add(instructor_group)
    user.user_permissions.add(permission)
    user.is_instructor = True
    user.save()
    yield user


@pytest.fixture(scope='function')
def logged_user(user_instructor, client, email, password):
    # client.force_login(user_instructor)
    client.login(email=user_instructor.email, password=password)


@pytest.fixture(scope='function')
def subject(db):
    return Subject.objects.create(title='HTML')


@pytest.fixture(scope='function')
def image():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file
