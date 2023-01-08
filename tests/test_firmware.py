import json
from podpointclient.pod import Firmware, FirmwareStatus, FirmwareVersion
from datetime import datetime, timezone

def test_complete_firmware():
    firmware_data = json.load(open('./tests/fixtures/complete_firmware.json')).get('data', [])
    firmware = Firmware(data=firmware_data[0])

    assert firmware.serial_number   == '123456789'
    assert firmware.firmware_version == 'A30P-3.1.22-00001'
    assert firmware.update_available == False
    
    version_info = firmware.version_info
    assert isinstance(version_info, FirmwareVersion)
    assert version_info.manifest_id == 'A30P-3.1.22-00001'

    update_status = firmware.update_status
    assert isinstance(update_status, FirmwareStatus)
    assert update_status.is_update_available == False

    assert firmware.dict == {'serial_number': '123456789', 'update_status': {'is_update_available': False}, 'version_info': {'manifest_id': 'A30P-3.1.22-00001'}}

def test_empty_firmware():
    firmware = Firmware(data={})

    assert firmware.serial_number    is None
    assert firmware.firmware_version is None
    assert firmware.update_available is None
    
    assert firmware.version_info  is None
    assert firmware.update_status is None

    assert firmware.dict == { 'serial_number': None, 'version_info': None, 'update_status': None }