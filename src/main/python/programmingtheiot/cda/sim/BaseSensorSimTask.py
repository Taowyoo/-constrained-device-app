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
    Shell representation of class for student implementation.

    """
    DEFAULT_DATA_SET_INDEX = 0
    DEFAULT_MIN_VAL = 0.0
    DEFAULT_MAX_VAL = 1000.0
    DEFAULT_RANDOMIZER_FLAG = False

    def __init__(self, sensorType: int = SensorData.DEFAULT_SENSOR_TYPE, dataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
        self._dataSet = dataSet
        self._sensorType = sensorType
        self._minVal = minVal
        self._maxVal = maxVal
        self._curDataIndex = self.DEFAULT_DATA_SET_INDEX
        self._latestSensorData = None
        self._useRandomizer = self.DEFAULT_RANDOMIZER_FLAG
        pass

    def generateTelemetry(self) -> SensorData:
        data = SensorData(sensorType=self._sensorType)
        if self._useRandomizer:
            data.setValue(random.uniform(self._minVal,self._maxVal))
            pass
        else:
            if self._dataSet is None:
                logging.error("Sim data set has not been setup!")
                return None
            data.setValue(self._dataSet.getDataEntry(self._curDataIndex))
            self._curDataIndex += 1
            if self._curDataIndex >= self._dataSet.getDataEntryCount():
                self._curDataIndex = self.DEFAULT_DATA_SET_INDEX
            pass
        self._latestSensorData = data
        return self._latestSensorData
        pass

    def getTelemetryValue(self) -> float:
        if self._latestSensorData is None:
            self.generateTelemetry()
        return self._latestSensorData.getValue()
        pass
