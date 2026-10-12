import unittest
from unittest.mock import patch

import numpy as np

from sensor import Sensor
from tire_pressure_monitoring import Alarm
from unittest.mock import create_autospec

def get_mock_sensor(reading: float | list[float]):
    mock_sensor = create_autospec(Sensor)
    mock_sensor.pop_next_pressure_psi_value.side_effect = reading if isinstance(reading, list) else [reading]
    return mock_sensor


class AlarmTest(unittest.TestCase):

    def test_alarm_is_off_by_default(self):
        alarm = Alarm()
        assert not alarm.is_alarm_on

    def test_alarm_is_alarm_off_in_threshold_low(self):
        with patch('sensor.Sensor.pop_next_pressure_psi_value', return_value=17):
            alarm = Alarm()
            alarm.check()
            assert not alarm.is_alarm_on

    def test_alarm_is_alarm_off_in_threshold_top(self):
        with patch('sensor.Sensor.pop_next_pressure_psi_value', return_value=21):
            alarm = Alarm()
            alarm.check()
            assert not alarm.is_alarm_on

    def test_alarm_is_on_when_pressure_below_threshold(self):
        with patch('sensor.Sensor.pop_next_pressure_psi_value', return_value=17-np.inf):
            alarm = Alarm()
            alarm.check()
            assert alarm.is_alarm_on

    def test_alarm_is_on_when_pressure_above_threshold(self):
        with patch('sensor.Sensor.pop_next_pressure_psi_value', return_value=21+np.inf):
            alarm = Alarm()
            alarm.check()
            assert alarm.is_alarm_on

    def test_alarm_is_on_outside_range(self):
        alarm = Alarm(get_mock_sensor(16.9))
        alarm.check()
        assert alarm.is_alarm_on

        alarm = Alarm(get_mock_sensor(21.1))
        alarm.check()
        assert alarm.is_alarm_on

    def test_alarm_is_off_in_range(self):
        alarm = Alarm(get_mock_sensor(17))
        alarm.check()
        assert not alarm.is_alarm_on

        alarm = Alarm(get_mock_sensor(21))
        alarm.check()
        assert not alarm.is_alarm_on

    def test_alarm_stays_on_after_pressure_returns_to_normal(self):
        alarm = Alarm(get_mock_sensor([16.9, 17]))
        alarm.check()
        alarm.check()
        assert alarm.is_alarm_on

        alarm = Alarm(get_mock_sensor([21.1, 21]))
        alarm.check()
        alarm.check()
        assert alarm.is_alarm_on
