#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from smbus import SMBus
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator


class PressureI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.
    
    """

    def __init__(self):
        super(PressureI2cSensorAdapterTask, self).__init__(sensorType=SensorData.PRESSURE_SENSOR_TYPE,
                                                           minVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
                                                           maxVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
        # init the I2C bus
        self.i2cBus = SMBus(1)
        # pressure sensor I2c address
        self.pressAddr = 0x5C  # LPS25H
        pass

    def generateTelemetry(self) -> SensorData:
        data = SensorData(sensorType=self._sensorType)
        data.setValue(self._readValueFromI2cBus())
        self._latestSensorData = data
        return self._latestSensorData
        pass

    def _readValueFromI2cBus(self) -> float:
        PRESS_OUT_XL = 0x28
        PRESS_OUT_L = 0x29
        PRESS_OUT_H = 0x2A
        press_xl = self.i2cBus.read_byte_data(self.pressAddr, PRESS_OUT_XL)
        press_l = self.i2cBus.read_byte_data(self.pressAddr, PRESS_OUT_L)
        press_h = self.i2cBus.read_byte_data(self.pressAddr, PRESS_OUT_H)
        """
        The full reference pressure value is composed by PRESS_OUT_H/_L/_XL and is represented as 2’s complement.
        Pressure Values exceeding the operating pressure Range are clipped.
        """
        press = (press_h << 16) | (press_l << 8) | press_xl
        press /= 4096
        return press
        pass
