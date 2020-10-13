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

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

# Import SimTasks
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
    """
    Manager to manage all sensor tasks, trigger and sensor tasks periodically and handle their results
    According to config, manager also manage sim data set generation
    """

    def __init__(self, useEmulator: bool = False, pollRate: int = 5, allowConfigOverride: bool = True):
        """
        Init the SensorAdapterManager, if using simulator, setup data sets and sim tasks for simulation

        :param useEmulator: Whether use Emulator
        :param pollRate: Interval seconds for polling sensor data
        :param allowConfigOverride: If allow to override config
        """
        logging.info("SensorAdapterManager is initializing...")
        # Init basic config variables
        self.useEmulator = useEmulator
        self.pollRate = pollRate
        self.allowConfigOverride = allowConfigOverride
        # Init data message listener
        self.dataMsgListener: IDataMessageListener = None
        # Init scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)

        # create sim sensor tasks and sim data tasks if needed
        if self.useEmulator is True:
            logging.info("SensorAdapterManager is using emulator.")

            humidityModule = __import__('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask',
                                        fromlist=['HumiditySensorEmulatorTask'])
            huClass = getattr(humidityModule, 'HumiditySensorEmulatorTask')
            self.humidityEmulator = huClass()

            pressureModule = __import__('programmingtheiot.cda.emulated.PressureSensorEmulatorTask',
                                        fromlist=['PressureSensorEmulatorTask'])
            prClass = getattr(pressureModule, 'PressureSensorEmulatorTask')
            self.pressureEmulator = prClass()

            tempModule = __import__('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask',
                                    fromlist=['TemperatureSensorEmulatorTask'])
            teClass = getattr(tempModule, 'TemperatureSensorEmulatorTask')
            self.tempEmulator = teClass()
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
        """
        Handle received sensor data
        If it is using simulator, got sensor data from sim tasks
        """
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
        else:
            humidityTelemetry = self.humidityEmulator.generateTelemetry()
            logging.info("Emulated humidity data: %s" % humidityTelemetry.__str__())
            self.dataMsgListener.handleSensorMessage(humidityTelemetry)

            pressureTelemetry = self.pressureEmulator.generateTelemetry()
            logging.info("Emulated pressure data: %s" % pressureTelemetry.__str__())
            self.dataMsgListener.handleSensorMessage(pressureTelemetry)

            tempTelemetry = self.tempEmulator.generateTelemetry()
            logging.info("Emulated temperature data: %s" % tempTelemetry.__str__())
            self.dataMsgListener.handleSensorMessage(tempTelemetry)
        pass

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """
        Set DataMessageListener for manager
        :param listener: Given listener
        :return: If setup listen successfully
        """
        if listener is None:
            logging.info("Given DataMessageListener is invalid!")
            return False
        logging.info("Set %s as DataMessageListener." % listener.__str__())
        self.dataMsgListener = listener
        return True
        pass

    def startManager(self):
        """
        Start SensorAdapterManager
        """
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Started SensorAdapterManager.")
        pass

    def stopManager(self):
        """
        Stop SensorAdapterManager
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("Stopped SensorAdapterManager.")
        pass
