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


class HumiditySensorSimTask(BaseSensorSimTask):
    """
    Implementation of HumiditySensorSimTask

    """

    def __init__(self, sensorType: int = SensorData.HUMIDITY_SENSOR_TYPE, dataSet = None,
                 minVal: float = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
                 maxVal: float = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY):
        """
        Init HumiditySensorSimTask by using super class constructor with values especially for HumiditySensorSimTask
        :param sensorType: Sensor Type, here is humidity sensor
        :param dataSet: Using local generated default data set
        :param minVal: Using default environment humidity from HumiditySensorSimTask
        :param maxVal: Using default environment humidity from HumiditySensorSimTask
        """
        super(HumiditySensorSimTask, self).__init__(sensorType=sensorType, dataSet=dataSet,	minVal=minVal, maxVal=maxVal)
        pass
