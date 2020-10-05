#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.BaseIotData import BaseIotData


class SensorData(BaseIotData):
    """
    Shell representation of class for student implementation.

    """
    DEFAULT_VAL = 0.0
    DEFAULT_SENSOR_TYPE = 0

    # These are just sensor type samples - these can be changed however
    # you'd like; you can also create an enum representing the values
    HUMIDITY_SENSOR_TYPE = 1
    PRESSURE_SENSOR_TYPE = 2
    TEMP_SENSOR_TYPE = 3
    SYS_UTIL_TYPE = 4

    def __init__(self, sensorType = DEFAULT_SENSOR_TYPE, d=None):
        super(SensorData, self).__init__(d=d)
        self._sensorType = sensorType
        self._value = SensorData.DEFAULT_VAL
        pass

    def getSensorType(self) -> int:
        """
        Returns the sensor type to the caller.

        @return int
        """
        return self._sensorType

    def getValue(self) -> float:
        """
        Returns the sensor value to the caller.

        @return float
        """
        return self._value
        pass

    def setValue(self, newVal: float):
        """
        Upadtes the sensor value by input value.

        """
        self._value = newVal
        pass

    def _handleUpdateData(self, data) -> bool:
        """
        Implemented template method for super data.
        Update sensor data part variables.
        @param data The Sensor data to apply to this instance.
        """
        if isinstance(data, SensorData):
            self._value = data._value
            self._sensorType = data._sensorType
        else:
            return False
        return True
        pass

    def __str__(self):
        """
        Returns a string representation of this instance.

        @return The string representing this instance.
        """

        custom_str = super(SensorData, self).__str__() + ', sensorType=' \
                     + str(self._sensorType) + ', value=' + str(self._value)

        return custom_str
