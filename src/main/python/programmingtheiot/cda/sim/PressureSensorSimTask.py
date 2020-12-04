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
from programmingtheiot.common import ConfigConst

from programmingtheiot.data.SensorData import SensorData


class PressureSensorSimTask(BaseSensorSimTask):
    """
    Implementation of PressureSensorSimTask

    """

    def __init__(self, sensorType: int = SensorData.PRESSURE_SENSOR_TYPE, dataSet = None,
                 minVal: float = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
                 maxVal: float = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE):
        """
        Init HumiditySensorSimTask by using super class constructor with values especially for PressureSensorSimTask
        :param sensorType: Sensor Type, here is pressure sensor
        :param dataSet: Using local generated default data set
        :param minVal: Using default environment pressure from PressureSensorSimTask
        :param maxVal: Using default environment pressure from PressureSensorSimTask
        """
        super(PressureSensorSimTask, self).__init__(sensorType=sensorType, dataSet=dataSet,	minVal=minVal, maxVal=maxVal)
        self._sensorName = ConfigConst.PRESSURE_SENSOR_NAME
        pass
