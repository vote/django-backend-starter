import pytest
from model_bakery import baker

from ..models import User


@pytest.mark.django_db
def test_user():
    user = baker.make("first_party_app.User", email="great@cool.com")
    assert str(user) == "great@cool.com"
    assert User.objects.count() == 1
