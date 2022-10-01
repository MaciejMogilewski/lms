import pytest


@pytest.mark.smoke
@pytest.mark.slow
def test_create_user(user, django_user_model):
    users = django_user_model.objects.all()
    assert len(users) == 2


@pytest.mark.skip(reason='Not working od Windwos')
@pytest.mark.slow
def test_change_password(user):
    user.set_password('secret')
    assert user.check_password('secret') is True
