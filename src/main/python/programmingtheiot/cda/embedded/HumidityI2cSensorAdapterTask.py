#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import smbus
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask


class HumidityI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self):
        super(HumidityI2cSensorAdapterTask, self).__init__(sensorType=SensorData.HUMIDITY_SENSOR_TYPE,
                                                           minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
                                                           maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
        self.humidAddr = 0x5F

        # init the I2C bus at the humidity address
        # WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
        self.i2cBus = smbus.SMBus(1)
        self.i2cBus.write_byte_data(self.humidAddr, 0, 0)
        pass

    def generateTelemetry(self) -> SensorData:
        pass

    def getTelemetryValue(self) -> float:
        pass
