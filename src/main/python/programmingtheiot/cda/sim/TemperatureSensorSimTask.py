#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from programmingtheiot.data.SensorData import SensorData


class TemperatureSensorSimTask(BaseSensorSimTask):
    """
    Implementation of TemperatureSensorSimTask
    """


    def __init__(self, sensorType: int = SensorData.TEMP_SENSOR_TYPE, dataSet=None,
                 minVal: float = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
                 maxVal: float = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP):
        """
        Init TemperatureSensorSimTask by using super class constructor with values especially for TemperatureSensorSimTask
        :param sensorType: Sensor Type, here is temperature sensor
        :param dataSet: Using local generated default data set
        :param minVal: Using default indoor temperature from SensorDataGenerator
        :param maxVal: Using default indoor temperature from SensorDataGenerator
        """
        super(TemperatureSensorSimTask, self).__init__(sensorType=sensorType, dataSet=dataSet, minVal=minVal, maxVal=maxVal)
        self._sensorName = "TemperatureSimSensor"
        pass
