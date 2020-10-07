#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

# Import Client Connectors
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

# Import Managers
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

# Import Modules for Config
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

# Import Modules for Data Structures
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
    """
    This class is the heart and soul of the CDA. It handles all data processing within the application, and marshals all
    the requests to the appropriate destination.

    """

    def __init__(self, enableMqtt: bool = True, enableCoap: bool = False):
        """
        Constructor for DeviceDataManager:
        1. Got configuration info from config file

        :param enableMqtt: Whether enable Mqtt Client
        :param enableCoap: Whether enable CoAP Client
        """
        logging.info("Initializing DeviceDataManager...")
        # Retrieving configs
        self.configUtil = ConfigUtil()
        self.enableEmulator = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)

        self.enableHandleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,
                                                                         ConfigConst.ENABLE_HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)

        self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE,
                                                             ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)

        self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE,
                                                               ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)
        # Init managers
        self.systemPerformanceManager = SystemPerformanceManager()
        self.systemPerformanceManager.setDataMessageListener(self)
        self.sensorAdapterManager = SensorAdapterManager(useEmulator=self.enableEmulator)
        self.sensorAdapterManager.setDataMessageListener(self)
        self.actuatorAdapterManager = ActuatorAdapterManager(useEmulator=self.enableEmulator)
        self.actuatorAdapterManager.setDataMessageListener(self)

        # Init DataUtil for converting data
        self.dataUtil = DataUtil()
        pass

    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        """
        Interface of IDataMessageListener:
        Handling callback ActuatorData, convert it to json format and upload it
        :param data: Callback ActuatorData
        :return: Whether hand the data successfully
        """
        logging.info("Callback: Handling an ActuatorCommandResponse")
        logging.debug("ActuatorData: %s" % data.__str__())
        jsonData = self.dataUtil.actuatorDataToJson(data)
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, jsonData)
        return True
        pass

    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Interface of IDataMessageListener:
        Handling callback IncomingMessage: forward it to data analysis and convert it ActuatorData instance
        :param resourceEnum: Enum that shows incoming message type
        :param msg: Incoming message string
        :return: Whether hand the data successfully
        """
        logging.info("Callback: Handling an IncomingMessage")
        logging.debug("IncomingMessage: %s" % msg)
        # actuatorData: ActuatorData = self.dataUtil.jsonToActuatorData(msg)
        self._handleIncomingDataAnalysis(msg)
        return True
        pass

    def handleSensorMessage(self, data: SensorData) -> bool:
        """
        Interface of IDataMessageListener:
        Handling callback SensorData: forward it to data analysis, convert it to json format and upload it
        :param data: Callback SensorData instance
        :return: Whether hand the data successfully
        """
        logging.info("Callback: Handling an SensorMessage")
        logging.debug("SensorData: %s" % data.__str__())
        jsonData = self.dataUtil.sensorDataToJson(data)
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, jsonData)
        self._handleSensorDataAnalysis(data)
        return True
        pass

    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        """
        Interface of IDataMessageListener:
        Handling callback SystemPerformanceData: convert it to json format and upload it
        :param data: Callback SystemPerformanceData instance
        :return: Whether hand the data successfully
        """
        logging.info("Callback: Handling an SystemPerformanceMessage")
        logging.debug("SystemPerformanceData: %s" % data.__str__())
        jsonData = self.dataUtil.sensorDataToJson(data)
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, jsonData)
        return True
        pass

    def startManager(self):
        """
        Start the DeviceDataManager.
        """
        logging.info("DeviceDataManager starting...")
        self.systemPerformanceManager.startManager()
        self.sensorAdapterManager.startManager()
        logging.info("DeviceDataManager stated.")
        pass

    def stopManager(self):
        """
        Stop the DeviceDataManager
        """
        logging.info("DeviceDataManager stopping.")
        self.systemPerformanceManager.stopManager()
        self.sensorAdapterManager.stopManager()
        logging.info("DeviceDataManager stopped.")
        pass

    def _handleIncomingDataAnalysis(self, msg: str):
        """
        Call this from handleIncomeMessage() to determine if there's
        any action to take on the message. Steps to take:
        1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
        2) Convert msg: Use DataUtil to convert if appropriate.
        3) Act on msg: Determine what - if any - action is required, and execute.
        """
        logging.debug("Handling analysis on IncomingData...")
        # TODO: validate msg in more detail
        if msg is None or len(msg) == 0:
            logging.warning("Handling analysis on an invalid IncomingData string!")
            return
        # Convert msg
        actuatorData: ActuatorData = self.dataUtil.jsonToActuatorData(msg)
        # Act on msg
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        pass

    def _handleSensorDataAnalysis(self, data: SensorData):
        """
        Call this from handleSensorMessage() to determine if there's
        any action to take on the message. Steps to take:
        1) Check config: Is there a rule or flag that requires immediate processing of data?
        2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
        """
        logging.debug("Handling analysis on SensorData...")
        if self.enableHandleTempChangeOnDevice is True:
            if data.getSensorType() is SensorData.TEMP_SENSOR_TYPE:
                localActuatorCmd = ActuatorData(actuatorType=ActuatorData.HVAC_ACTUATOR_TYPE)
                if data.getValue() < self.triggerHvacTempFloor:
                    logging.debug("Turn on HVAC as current temperature: %f is lower than floor: %f."
                                  % (data.getValue(), self.triggerHvacTempFloor))
                    localActuatorCmd.setCommand(ActuatorData.COMMAND_ON)
                    self.actuatorAdapterManager.sendActuatorCommand(localActuatorCmd)
                    pass
                elif data.getValue() > self.triggerHvacTempCeiling:
                    logging.debug("Turn off HVAC as current temperature: %f is higher than ceiling: %f."
                                  % (data.getValue(), self.triggerHvacTempCeiling))
                    localActuatorCmd.setCommand(ActuatorData.COMMAND_OFF)
                    self.actuatorAdapterManager.sendActuatorCommand(localActuatorCmd)
                    pass

        pass

    def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
        """
        Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
        to determine if the message should be sent upstream. Steps to take:
        1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
        2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
        """
        logging.debug("Handling upstream transmission...")
        # TODO: upload the json string
        pass
