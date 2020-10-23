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
from programmingtheiot.cda.embedded.I2cHelper import linearInterpolation, read2byte
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class HumidityI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self):
        super(HumidityI2cSensorAdapterTask, self).__init__(sensorType=SensorData.HUMIDITY_SENSOR_TYPE,
                                                           minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
                                                           maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
        self._sensorName = "HumidityI2cSensor"
        # init the I2C bus
        self.i2cBus = SMBus(1)
        # humidity sensor I2c address
        self.humidAddr = 0x5F  # HTS221
        pass

    def generateTelemetry(self) -> SensorData:
        data = SensorData(sensorType=self._sensorType)
        data.setValue(self._readValueFromI2cBus())
        data.setName()
        self._latestSensorData = data
        return self._latestSensorData
        pass

    def _readValueFromI2cBus(self) -> float:
        # read humidity sensor humidity
        # H0_T0_OUT
        H0_T0_OUT_L = 0x36
        H0_T0_OUT_H = 0x37
        H0_T0_OUT = read2byte(self.i2cBus, self.humidAddr, H0_T0_OUT_L, H0_T0_OUT_H)
        # H1_T0_OUT
        H1_T0_OUT_L = 0x3A
        H1_T0_OUT_H = 0x3B
        H1_T0_OUT = read2byte(self.i2cBus, self.humidAddr, H1_T0_OUT_L, H1_T0_OUT_H)
        # H0_rH_x2
        H0_rH_x2_ADDR = 0x30
        H0_rH_x2 = self.i2cBus.read_byte_data(self.humidAddr, H0_rH_x2_ADDR)
        H0_rH = H0_rH_x2 / 2
        # H1_rH_x2
        H1_rH_x2_ADDR = 0x31
        H1_rH_x2 = self.i2cBus.read_byte_data(self.humidAddr, H1_rH_x2_ADDR)
        H1_rH = H1_rH_x2 / 2
        # H_OUT
        HUMIDITY_OUT_L = 0x28
        HUMIDITY_OUT_H = 0x29
        HUMIDITY_OUT = read2byte(self.i2cBus, self.humidAddr, HUMIDITY_OUT_L, HUMIDITY_OUT_H)
        # Linear interpolation
        humidity = linearInterpolation(H0_T0_OUT, HUMIDITY_OUT, H1_T0_OUT, H0_rH, H1_rH)
        return humidity
        pass
