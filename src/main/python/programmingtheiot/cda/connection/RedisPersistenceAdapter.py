

import logging

from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData
import redis


class RedisPersistenceAdapter:

    def __init__(self)
        """
        Constructor, do some basic configrations
        """
        self.dataUtil = DataUtil()
        self.configUtil = ConfigUtil()
        self.host = self.configUtil.getProperty(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.HOST_KEY)
        self.port = self.configUtil.getInteger(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.PORT_KEY)
        self.enableCrypt = self.configUtil.getBoolean(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.ENABLE_CRYPT_KEY)
        if self.enableCrypt:
            self.credFilePath = self.configUtil.getProperty(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.CRED_FILE_KEY)
            # TODO: init redis with encryption
        logging.info("Redis client setting: host = {0}, port = {1}.".format(self.host, self.port))
        # Init with no connection established
        self.curConnection: redis.client.Redis = None

    def connectClient(self) -> bool:
        """
        Connect to redis
        :return: whether success
        """
        if self.curConnection is None:
            logging.info("Redis client connecting to server...")
            try:
                self.curConnection = redis.client.Redis(host=self.host, port=self.port)
                logging.info("Redis client successfully connect to server.")
            except BaseException as be:
                self.curConnection = None
                logging.error("Cannot connect to Redis server, meet exception: " + be.__str__())
                return False
            return True
        else:
            logging.warning("Redis client has already connected!")
            return True

    def disconnectClient(self) -> bool:
        """
        Disconnect to redis
        :return: whether success
        """
        if self.curConnection is None:
            logging.warning("Redis client has already disconnected!")
            return True
        else:
            logging.info("Redis client disconnecting...!")
            self.curConnection.close()
            self.curConnection = None
            logging.info("Redis client disconnect successfully.")
            return True

    def storeData(self, data: SensorData, resource: ResourceNameEnum = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE) -> bool:
        """
        Store a SensorData to the key which defined by given ResourceNameEnum

        :param data: SensorData instance to store which will be convert to json string
        :param resource: ResourceNameEnum instance which will be convert to string, defaults to ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
        :return: whether success
        """
        topicName: str = resource.value
        jsonStr = self.dataUtil.sensorDataToJson(data)
        if self.curConnection:
            subNums = self.curConnection.publish(channel=topicName, message=jsonStr)
            logging.debug("Published msg:\n{0}\nto {1} with {2} subscribers.".format(jsonStr, topicName, subNums))
            return True
        else:
            logging.error("Cannot store data to Redis, because client has not connected to server yet!")
            return False
        pass
