from podpointclient.schedule import Schedule, ScheduleStatus


def test_schedule_serialisation():
    schedule = Schedule(
        uid=123,
        start_day=1,
        start_time="10:00",
        end_day=1,
        end_time="11:00",
        status=ScheduleStatus(is_active=True)
    )

    assert schedule.dict == {"uid": 123, "start_day": 1, "start_time": "10:00", "end_day": 1, "end_time": "11:00", "status": {"is_active": True}}
    assert schedule.to_json() == '{"uid": 123, "start_day": 1, "start_time": "10:00", "end_day": 1, "end_time": "11:00", "status": {"is_active": true}}'

    # uid is optional (used when sending new schedules)
    schedule = Schedule(
        start_day=1,
        start_time="10:00",
        end_day=1,
        end_time="11:00",
        status=ScheduleStatus(is_active=True)
    )
    assert schedule.dict == {"start_day": 1, "start_time": "10:00", "end_day": 1, "end_time": "11:00", "status": {"is_active": True}}
    assert schedule.to_json() == '{"start_day": 1, "start_time": "10:00", "end_day": 1, "end_time": "11:00", "status": {"is_active": true}}'

    # Check that False is respected
    schedule = Schedule(
        start_day=1,
        start_time="10:00",
        end_day=1,
        end_time="11:00",
        status=ScheduleStatus(is_active=False)
    )
    assert schedule.dict == {"start_day": 1, "start_time": "10:00", "end_day": 1, "end_time": "11:00", "status": {"is_active": False}}
    assert schedule.to_json() == '{"start_day": 1, "start_time": "10:00", "end_day": 1, "end_time": "11:00", "status": {"is_active": false}}'
