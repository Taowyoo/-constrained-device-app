#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

from programmingtheiot.data.SensorData import SensorData

class BaseSensorSimTask():
    """
    Base class for SensorSimTask

    """
    DEFAULT_DATA_SET_INDEX = 0
    DEFAULT_MIN_VAL = 0.0
    DEFAULT_MAX_VAL = 1000.0
    DEFAULT_RANDOMIZER_FLAG = False
    DEFAULT_NAME = "DefaultSimSensor"

    def __init__(self, sensorType: int = SensorData.DEFAULT_SENSOR_TYPE, dataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
        """
        Init BaseSensorSimTask with default values
        :param sensorType: Sensor Type
        :param dataSet: Data set for sim
        :param minVal: Min value of dataSet or randomizer range
        :param maxVal: Max value of dataSet or randomizer range
        """
        self._dataSet = dataSet
        self._sensorType = sensorType
        self._sensorName = self.DEFAULT_NAME
        self._minVal = minVal
        self._maxVal = maxVal
        self._curDataIndex = self.DEFAULT_DATA_SET_INDEX
        self._latestSensorData = None
        self._useRandomizer = self.DEFAULT_RANDOMIZER_FLAG
        pass

    def generateTelemetry(self) -> SensorData:
        """
        Generate sim SensorData
        If useRandomizer is enable, generate SensorData with random value, else use data in generated data set
        :return: Generated sim SensorData
        """
        data = SensorData(sensorType=self._sensorType)
        data.setName(self._sensorName)
        if self._useRandomizer:
            data.setValue(random.uniform(self._minVal, self._maxVal))
            pass
        elif self._dataSet is None:
            logging.warning("Sim data set has not been setup! Using data from Randomizer!")
            data.setValue(random.uniform(self._minVal, self._maxVal))
            pass
        else:
            data.setValue(self._dataSet.getDataEntry(self._curDataIndex))
            self._curDataIndex += 1
            if self._curDataIndex >= self._dataSet.getDataEntryCount():
                self._curDataIndex = self.DEFAULT_DATA_SET_INDEX
            pass
        self._latestSensorData = data
        return self._latestSensorData
        pass

    def getTelemetryValue(self) -> float:
        """
        Get latest generated data value
        :return: Sensor data value
        """
        if self._latestSensorData is None:
            self.generateTelemetry()
        return self._latestSensorData.getValue()
        pass
