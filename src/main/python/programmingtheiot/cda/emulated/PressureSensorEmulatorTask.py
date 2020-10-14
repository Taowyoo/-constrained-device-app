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

class PressureSensorEmulatorTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, dataSet=None):
        """
        Constructor of PressureSensorEmulatorTask
        Using super class constructor to init
        :param dataSet: Dict for construct object with given data
        """
        super(PressureSensorEmulatorTask, self).__init__(sensorType=SensorData.PRESSURE_SENSOR_TYPE,
                                                         dataSet=dataSet,
                                                         minVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
                                                         maxVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
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
        Use pisense API to retrieve the current pressure measurement.
        The pressure is measured in millibars (aka hectopascals).(in mbar or hPa)
        :return: Generated SensorData
        """
        data = SensorData(sensorType=self._sensorType)
        data.setValue(self.sh.environ.pressure)
        self._latestSensorData = data
        return self._latestSensorData
        pass
