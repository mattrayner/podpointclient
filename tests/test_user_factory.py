from podpointclient.user import User
from podpointclient.factories import UserFactory
from helpers import Mocks

def test_user_factory_full_user_creation():
    mocks = Mocks()
    user_response = mocks.user_response()

    factory = UserFactory()
    user = factory.build_user(user_response)

    assert isinstance(user, User)

def test_user_factory_with_no_data():
    factory = UserFactory()
    user = factory.build_user({})

    assert user is None


def test_user_factory_with_None():
    factory = UserFactory()
    user = factory.build_user(None)

    assert user is None
