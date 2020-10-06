#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask

class SensorAdapterManager(object):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, useEmulator: bool = False, pollRate: int = 5, allowConfigOverride: bool = True):
        logging.info("SensorAdapterManager is initializing...")
        self.useEmulator = useEmulator
        self.pollRate = pollRate
        self.allowConfigOverride = allowConfigOverride
        self.dataMsgListener: IDataMessageListener = None
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)

        if self.useEmulator is True:
            logging.info("SensorAdapterManager is using emulator.")
        else:
            logging.info("SensorAdapterManager is using simulators.")
            self.dataGenerator = SensorDataGenerator()
            configUtil = ConfigUtil()
            humidityFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_FLOOR_KEY,
                                                SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
            humidityCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_CEILING_KEY,
                                                  SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
            pressureFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_FLOOR_KEY,
                                                SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
            pressureCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_CEILING_KEY,
                                                  SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
            tempFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_FLOOR_KEY,
                                            SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
            tempCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_CEILING_KEY,
                                              SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
            humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(minValue=humidityFloor,
                                                                                      maxValue=humidityCeiling,
                                                                                      useSeconds=False)
            pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(minValue=pressureFloor,
                                                                                      maxValue=pressureCeiling,
                                                                                      useSeconds=False)
            tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(minValue=tempFloor,
                                                                                maxValue=tempCeiling,
                                                                                useSeconds=False)
            self.humiditySensorSimTask = HumiditySensorSimTask(dataSet=humidityData, minVal=humidityFloor,
                                                               maxVal=humidityCeiling)
            self.pressureSensorSimTask = PressureSensorSimTask(dataSet=pressureData, minVal=pressureFloor,
                                                               maxVal=pressureCeiling)
            self.temperatureSensorSimTask = TemperatureSensorSimTask(dataSet=tempData, minVal=tempFloor,
                                                                     maxVal=tempCeiling)
        pass

    def handleTelemetry(self):
        logging.info("SensorAdapterManager is trying to get Telemetries...")
        if self.useEmulator is False:
            humidityTelemetry = self.humiditySensorSimTask.generateTelemetry()
            logging.info("Simulated humidity data: %s" % humidityTelemetry.__str__())
            self.dataMsgListener.handleSensorMessage(humidityTelemetry)

            pressureTelemetry = self.pressureSensorSimTask.generateTelemetry()
            logging.info("Simulated pressure data: %s" % pressureTelemetry.__str__())
            self.dataMsgListener.handleSensorMessage(pressureTelemetry)

            tempTelemetry = self.pressureSensorSimTask.generateTelemetry()
            logging.info("Simulated temperature data: %s" % tempTelemetry.__str__())
            self.dataMsgListener.handleSensorMessage(tempTelemetry)
        pass

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener is None:
            logging.info("Given DataMessageListener is invalid!")
            return False
        logging.info("Set %s as DataMessageListener." % listener.__str__())
        self.dataMsgListener = listener
        return True
        pass

    def startManager(self):
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Started SensorAdapterManager.")
        pass

    def stopManager(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("Stopped SensorAdapterManager.")
        pass
