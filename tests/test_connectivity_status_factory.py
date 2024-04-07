from podpointclient.connectivity_status import ConnectivityStatus
from podpointclient.factories import ConnectivityStatusFactory
from helpers import Mocks

def test_charge_factory_charge_array_creation():
    mocks = Mocks()
    connectivity_status_response = mocks.connectivity_status_response()

    factory = ConnectivityStatusFactory()
    connectivity_status = factory.build_connectivity_status(connectivity_status_response)

    assert ConnectivityStatus == type(connectivity_status)

def test_charge_factory_with_none_passed():
    factory = ConnectivityStatusFactory()
    assert factory.build_connectivity_status(None) == None
