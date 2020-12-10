import logging

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
import programmingtheiot.common.ConfigConst as ConfigConst

import board
import busio
import adafruit_ccs811

import time

class CO2SensorAdapterTask(BaseSensorSimTask):
    """
    CO2 sensor task implemented by using CCS811 Air Quality Sensor

    """
    # eCO2 measurement range, unit: ppm
    MINVAL_ECO2 = 400
    MAXVAL_ECO2 = 8192
    # TVOC measurement range, unit: ppb
    MINVAL_TVOC = 0
    MAXVAL_TVOC = 1187
    def __init__(self):
        super(CO2SensorAdapterTask, self).__init__(sensorType=SensorData.CO2_SENSOR_TYPE)
        self._sensorName = ConfigConst.CO2_SENSOR_NAME
        self.i2c = busio.I2C(board.SCL, board.SDA)
        time.sleep(0.5)  # wait i2c instance fully init
        self.ccs811 = adafruit_ccs811.CCS811(self.i2c)
        pass

    def generateTelemetry(self) -> SensorData:
        data = SensorData(sensorType=self._sensorType)
        telemetry = self._readValueFromSensor()
        if telemetry < self.MINVAL_ECO2 or telemetry > self.MAXVAL_ECO2:
            data.setStatusCode(-1)
            pass
        data.setValue(telemetry)
        data.setName(self._sensorName)
        self._latestSensorData = data
        return self._latestSensorData
        pass

    def _readValueFromSensor(self) -> float:
        # Wait for the sensor to be ready
        ret = 0
        while not self.ccs811.data_ready:
            pass
        ret = self.ccs811.eco2
        return ret
