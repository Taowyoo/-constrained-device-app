#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from pisense import SenseHAT

class TemperatureSensorEmulatorTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, dataSet=None):
        """
        Constructor of TemperatureSensorEmulatorTask
        Using super class constructor to init
        :param dataSet: Dict for construct object with given data
        """
        super(TemperatureSensorEmulatorTask, self).__init__(sensorType=SensorData.TEMP_SENSOR_TYPE,
                                                            dataSet=dataSet,
                                                            minVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
                                                            maxVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
        self.enableEmulation = True
        configUtil = ConfigUtil()
        enableSenseHAT = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)
        if enableSenseHAT is True:
            self.enableEmulation = False
        else:
            self.enableEmulation = True
        self.sh = SenseHAT(emulate=self.enableEmulation)
        pass

    def generateTelemetry(self) -> SensorData:
        """
        Use pisense API to retrieve the current temperature measurement.
        The temperature is measured in degrees celsius.(in °C)
        :return: Generated SensorData
        """
        data = SensorData(sensorType=self._sensorType)
        data.setValue(self.sh.environ.temperature)
        self._latestSensorData = data
        return self._latestSensorData
        pass
