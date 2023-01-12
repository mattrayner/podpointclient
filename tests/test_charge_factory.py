from podpointclient.charge import Charge
from podpointclient.factories import ChargeFactory
from helpers import Mocks

def test_charge_factory_charge_array_creation():
    mocks = Mocks()
    charge_response = mocks.charge_response()

    factory = ChargeFactory()
    charges = factory.build_charges(charge_response)
    
    assert 10 == len(charges)
    assert Charge == type(charges[0])

def test_charve_factory_with_no_charges():
    factory = ChargeFactory()
    charges = factory.build_charges({})

    assert charges == []

def test_charge_factory_with_none_passed():
    factory = ChargeFactory()
    assert factory.build_charges(None) == []
