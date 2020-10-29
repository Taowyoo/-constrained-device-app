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


class TemperatureI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.
    """

    def __init__(self):
        super(TemperatureI2cSensorAdapterTask, self).__init__(sensorType=SensorData.TEMP_SENSOR_TYPE,
                                                              minVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
                                                              maxVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
        self._sensorName = "TemperatureI2cSensor"
        # init the I2C bus
        self.i2cBus = SMBus(1)
        # use temperature sensor in humidity sensor
        # humidity sensor I2c address
        self.humidAddr = 0x5F  # HTS221
        pass

    def generateTelemetry(self) -> SensorData:
        data = SensorData(sensorType=self._sensorType)
        data.setValue(self._readValueFromI2cBus())
        self._latestSensorData = data
        return self._latestSensorData
        pass

    def _readValueFromI2cBus(self) -> float:
        # read humidity sensor tempreture
        # T0_OUT
        T0_OUT_L = 0x3C
        T0_OUT_H = 0x3D
        T0_OUT = read2byte(self.i2cBus, self.humidAddr, T0_OUT_L, T0_OUT_H)
        # T1_OUT
        T1_OUT_L = 0x3E
        T1_OUT_H = 0x3F
        T1_OUT = read2byte(self.i2cBus, self.humidAddr, T1_OUT_L, T1_OUT_H)
        # T0_degC_x8
        T0_degC_x8_ADDR = 0x32
        T0_degC_x8 = self.i2cBus.read_byte_data(self.humidAddr, T0_degC_x8_ADDR)

        # T1_degC_x8
        T1_degC_x8_ADDR = 0x33
        T1_degC_x8 = self.i2cBus.read_byte_data(self.humidAddr, T1_degC_x8_ADDR)

        # T0_degC_msb, T1_degC_msb
        degC_msb_ADDR = 0x35
        msb = self.i2cBus.read_byte_data(self.humidAddr, degC_msb_ADDR)
        T0_degC_msb = (msb & 0x03) << 8
        T1_degC_msb = (msb & 0x0C) << 6

        T0_degC = (T0_degC_msb | T0_degC_x8) >> 3
        T1_degC = (T1_degC_msb | T1_degC_x8) >> 3

        # TEMP_OUT
        TEMP_OUT_L = 0x2A
        TEMP_OUT_H = 0x2B
        TEMP_OUT = read2byte(self.i2cBus, self.humidAddr, TEMP_OUT_L, TEMP_OUT_H)

        temperature = linearInterpolation(T0_OUT, TEMP_OUT, T1_OUT, T0_degC, T1_degC)
        return temperature
        pass

