#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import paho.mqtt.client as mqttClient

from programmingtheiot.common import ConfigUtil
from programmingtheiot.common import ConfigConst

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

DEFAULT_QOS = 1

class MqttClientConnector(IPubSubClient):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, clientID: str = None):
        """
        Default constructor. This will set remote broker information and client connection
        information based on the default configuration file contents.

        @param clientID Defaults to None. Can be set by caller. If this is used, it's
        critically important that a unique, non-conflicting name be used so to avoid
        causing the MQTT broker to disconnect any client using the same name. With
        auto-reconnect enabled, this can cause a race condition where each client with
        the same clientID continuously attempts to re-connect, causing the broker to
        disconnect the previous instance.
        """
        self.config = ConfigUtil.ConfigUtil()
        self.host = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY,
                                            ConfigConst.DEFAULT_HOST)

        self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY,
                                           ConfigConst.DEFAULT_MQTT_PORT)

        self.keepAlive = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY,
                                                ConfigConst.DEFAULT_KEEP_ALIVE)

        logging.info('\tMQTT Broker Host: ' + self.host)
        logging.info('\tMQTT Broker Port: ' + str(self.port))
        logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
        self.dataMsgListener: IDataMessageListener = None
        self.clientID = ""
        if clientID is not None:
            self.clientID = clientID
        self.mc: mqttClient.Client = None
        pass

    def connect(self) -> bool:
        if not self.mc:
            logging.info("Creating MQTT client...")
            self.mc = mqttClient.Client(client_id=self.clientID, clean_session=True)
            self.mc.on_connect = self.onConnect
            self.mc.on_disconnect = self.onDisconnect
            self.mc.on_message = self.onMessage
            self.mc.on_publish = self.onPublish
            self.mc.on_subscribe = self.onSubscribe
            logging.info("Succeed to create MQTT client!")
        if not self.mc.is_connected():
            logging.info("Connecting MQTT client to broker at {0}:{1}...".format(self.host, self.port))
            self.mc.connect(self.host, self.port, self.keepAlive)
            self.mc.loop_start()
            return True
        else:
            logging.warning('MQTT client is already connected. Ignoring connect request.')
            return False
        pass

    def disconnect(self) -> bool:
        if self.mc is not None:
            if self.mc.is_connected():
                logging.info("MQTT client is disconnecting from broker...")
                self.mc.disconnect()
                self.mc.loop_stop()
                return True
        logging.warning('MQTT client is already disconnected. Ignoring disconnect request.')
        return False
        pass

    def onConnect(self, client, userdata, flags, rc):
        logging.info("MQTT client Connection returned result: " + mqttClient.connack_string(rc))
        pass

    def onDisconnect(self, client, userdata, rc):
        if rc != 0:
            logging.warning("MQTT client meets Unexpected disconnection!")
        else:
            logging.info("MQTT client succeed to disconnect from broker.")
        pass

    def onMessage(self, client, userdata, msg):
        logging.info("MQTT client received message '" + str(msg.payload) + "' on topic '"
                     + msg.topic + "' with QoS " + str(msg.qos))
        resource = ResourceNameEnum.getResourceNameByValue(val=msg.topic)
        if resource:
            if self.dataMsgListener:
                self.dataMsgListener.handleIncomingMessage(resource, msg)
            else:
                logging.warning("dataMsgListener has not been initialized!")
        else:
            logging.warning("Incoming message comes from invalid topic!")
        pass

    def onPublish(self, client, userdata, mid):
        logging.info("MQTT client succeed to publish a message, id: " + str(mid))
        pass

    def onSubscribe(self, client, userdata, mid, granted_qos):
        logging.info("MQTT client succeed to subscribe, id: {}, QoS: {}".format(mid, granted_qos))
        pass

    def publishMessage(self, resource: ResourceNameEnum, msg, qos: int = IPubSubClient.DEFAULT_QOS):
        if resource is None:
            logging.warning("Got invalid ResourceNameEnum when publishing!")
        if qos > 2 or qos < 0:
            qos = IPubSubClient.DEFAULT_QOS
            logging.warning("Got invalid QoS value, change to use default QoS: {}".format(qos))
        logging.debug("MQTT client send msg:'{}' to topic '{}' with qos {}.".format(msg, resource.name, qos))
        self.mc.publish(topic=resource.name, payload=msg, qos=qos)
        pass

    def subscribeToTopic(self, resource: ResourceNameEnum, qos: int = IPubSubClient.DEFAULT_QOS):
        if resource is None:
            logging.warning("Got invalid ResourceNameEnum when subscribing!")
        if qos > 2 or qos < 0:
            qos = IPubSubClient.DEFAULT_QOS
            logging.warning("Got invalid QoS value, change to use default QoS: {}".format(qos))
        logging.debug("MQTT client subscribe to topic '{}' with qos {}.".format(resource.name, qos))
        self.mc.subscribe(topic=resource.name, qos=qos)
        pass

    def unsubscribeFromTopic(self, resource: ResourceNameEnum):
        logging.debug("MQTT client MQTT client unsubscribe to topic '{}'.".format(resource.name))
        self.mc.unsubscribe(topic=resource.name)
        pass

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener is None:
            logging.info("Given DataMessageListener is invalid!")
            return False
        logging.info("Set %s as DataMessageListener." % listener.__str__())
        self.dataMsgListener = listener
        return True
        pass
