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

# Import I2C Tasks
from programmingtheiot.cda.embedded.HumidityI2cSensorAdapterTask import HumidityI2cSensorAdapterTask
from programmingtheiot.cda.embedded.PressureI2cSensorAdapterTask import PressureI2cSensorAdapterTask
from programmingtheiot.cda.embedded.TemperatureI2cSensorAdapterTask import TemperatureI2cSensorAdapterTask
from programmingtheiot.cda.embedded.CO2SensorAdapterTask import CO2SensorAdapterTask

class SensorAdapterManager(object):
    """
    Manager to manage all sensor tasks, trigger and sensor tasks periodically and handle their results
    According to config, manager also manage sim data set generation
    """

    def __init__(self, useEmulator: bool = False, enableSenseHAT: bool = False, pollRate: int = 30, allowConfigOverride: bool = True):
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

        configUtil = ConfigUtil()
        self.enableSenseHAT = enableSenseHAT
        self.enableSenseHATI2C = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SENSE_HAT_I2C_KEY,False)
        self.enableCO2Sensor = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_CO2_SENSOR_KEY,False)
        if self.enableCO2Sensor is True:
            self.co2SensorTask = CO2SensorAdapterTask()
        if self.enableSenseHATI2C is True:
            logging.info("SensorAdapterManager is using I2C to communiate with SenseHAT.")
            self.humiditySensorI2cTask = HumidityI2cSensorAdapterTask()
            self.pressureSensorI2cTask = PressureI2cSensorAdapterTask()
            self.temperatureSensorI2cTask = TemperatureI2cSensorAdapterTask()
            pass
        elif self.useEmulator is True or self.enableSenseHAT is True:
            if self.enableSenseHAT is True:
                logging.info("SensorAdapterManager is using pisense to communiate with SenseHAT.")
            else:
                logging.info("SensorAdapterManager is using SenseHAT emulator.")
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
        # get telemetries from SenseHAT
        if self.enableSenseHAT:
            if self.enableSenseHATI2C:
                humidityTelemetry = self.humiditySensorI2cTask.generateTelemetry()
                logging.info("SenserHAT I2c humidity data: %s" % humidityTelemetry.__str__())

                pressureTelemetry = self.pressureSensorI2cTask.generateTelemetry()
                logging.info("SenserHAT I2c pressure data: %s" % pressureTelemetry.__str__())

                tempTelemetry = self.temperatureSensorI2cTask.generateTelemetry()
                logging.info("SenserHAT I2c temperature data: %s" % tempTelemetry.__str__())
            else:
                humidityTelemetry = self.humidityEmulator.generateTelemetry()
                logging.info("SenserHAT humidity data: %s" % humidityTelemetry.__str__())

                pressureTelemetry = self.pressureEmulator.generateTelemetry()
                logging.info("SenserHAT pressure data: %s" % pressureTelemetry.__str__())

                tempTelemetry = self.tempEmulator.generateTelemetry()
                logging.info("SenserHAT temperature data: %s" % tempTelemetry.__str__())
        elif self.useEmulator is False:
            humidityTelemetry = self.humiditySensorSimTask.generateTelemetry()
            logging.info("Simulated humidity data: %s" % humidityTelemetry.__str__())

            pressureTelemetry = self.pressureSensorSimTask.generateTelemetry()
            logging.info("Simulated pressure data: %s" % pressureTelemetry.__str__())

            tempTelemetry = self.temperatureSensorSimTask.generateTelemetry()
            logging.info("Simulated temperature data: %s" % tempTelemetry.__str__())
        else:
            humidityTelemetry = self.humidityEmulator.generateTelemetry()
            logging.info("Emulated humidity data: %s" % humidityTelemetry.__str__())

            pressureTelemetry = self.pressureEmulator.generateTelemetry()
            logging.info("Emulated pressure data: %s" % pressureTelemetry.__str__())

            tempTelemetry = self.tempEmulator.generateTelemetry()
            logging.info("Emulated temperature data: %s" % tempTelemetry.__str__())
        # upload sensehat telemtries
        self.dataMsgListener.handleSensorMessage(tempTelemetry)
        self.dataMsgListener.handleSensorMessage(pressureTelemetry)
        self.dataMsgListener.handleSensorMessage(humidityTelemetry)
        # CO2 sensor
        if self.enableCO2Sensor:
            co2Telemetry = self.co2SensorTask.generateTelemetry()
            logging.info("CO2 sensor data: %s" % co2Telemetry.__str__())
            self.dataMsgListener.handleSensorMessage(co2Telemetry)
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
