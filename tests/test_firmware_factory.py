from podpointclient.pod import Firmware
from podpointclient.factories import FirmwareFactory
from helpers import Mocks

def test_firmware_factory_single_firmware_creation():
    mocks = Mocks()
    firmware_response = mocks.firmware_response()

    factory = FirmwareFactory()
    firmwares = factory.build_firmwares(firmware_response)
    
    assert 1 == len(firmwares)
    assert isinstance(firmwares[0], Firmware)

def test_firmware_factory_with_no_firmwares():
    factory = FirmwareFactory()
    firmwares = factory.build_firmwares({})

    assert firmwares == []

def test_firmware_factory_with_none_passed():
    factory = FirmwareFactory()
    assert factory.build_firmwares(None) == []
