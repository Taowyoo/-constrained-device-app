#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import socket

from coapthon import defines
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri, generate_random_token

from programmingtheiot.common import ConfigUtil
from programmingtheiot.common import ConfigConst

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

class CoapClientConnector(IRequestResponseClient):
    """
    CoAP Client Connector class. Implement functions to connect to CoAP server.
    """

    def __init__(self):
        """
        Constructor of CoAP Client
        Init CoAP Client with host and port from config.
        """
        self.config = ConfigUtil.ConfigUtil()
        self.dataMsgListener = None
        self.coapClient: HelperClient = None

        self.host = self.config.getProperty(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY,
                                            ConfigConst.DEFAULT_HOST)
        self.port = self.config.getInteger(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY,
                                           ConfigConst.DEFAULT_COAP_PORT)

        self.url = "coap://" + self.host + ":" + str(self.port) + "/"
        try:
            logging.info("Parsing URL: " + self.url)

            self.host, self.port, self.path = parse_uri(self.url)
            tmpHost = socket.gethostbyname(self.host)

            if tmpHost:
                self.host = tmpHost
                self._initClient()
            else:
                logging.error("Can't resolve host: " + self.host)

        except socket.gaierror:
            logging.info("Failed to resolve host: " + self.host)

        logging.info('\tCoAP Server Host: ' + self.host)
        logging.info('\tCoAP Server Port: ' + str(self.port))
        pass

    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send Discover to CoAP server to get list of all available resources
        :param timeout: Timeout seconds of this request
        :return: Whether succeed to send request
        """
        logging.info('Discovering remote resources...')
        self.coapClient.discover(callback=self._onDiscoveryResponse, timeout=timeout)
        # self.coapClient.get(path='/.well-known/core', callback=self._onDiscoveryResponse, timeout=timeout)
        return True
        pass

    def sendDeleteRequest(self, resource: ResourceNameEnum, enableCON = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send Delete to CoAP server to delete sth.
        :param resource: The resource name of what need to be deleted
        :param enableCON: Whether send a CON CoAP msg
        :param timeout: Timeout seconds of this request
        :return: Whether succeed to send request
        """
        if resource:
            logging.debug("Issuing DELETE with path: " + resource.value)
            request = self.coapClient.mk_request(defines.Codes.DELETE, path=resource.value)
            request.token = generate_random_token(2)

            if not enableCON:
                request.type = defines.Types["NON"]

            self.coapClient.send_request(request=request, callback=self._onDeleteResponse, timeout=timeout)
            return True
        else:
            logging.warning("Can't DELETE - no path or path list provided.")
            return False
        pass

    def sendGetRequest(self, resource: ResourceNameEnum, enableCON = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send Get to CoAP server to get sth.
        :param resource: The resource name of what need to get
        :param enableCON: Whether send a CON CoAP msg
        :param timeout: Timeout seconds of this request
        :return: Whether succeed to send request
        """
        if resource:
            logging.debug("Issuing GET with path: " + resource.value)
            request = self.coapClient.mk_request(defines.Codes.GET, path=resource.value)
            request.token = generate_random_token(2)

            if not enableCON:
                request.type = defines.Types["NON"]

            self.coapClient.send_request(request=request, callback=self._onGetResponse, timeout=timeout)
            return True
        else:
            logging.warning("Can't GET - no path or path list provided.")
            return False
        pass

    def sendPostRequest(self, resource: ResourceNameEnum, payload: str, enableCON = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send data to CoAP server by requesting a POST
        :param resource: The resource name of where to post
        :param payload: Data to send
        :param enableCON: Whether send a CON CoAP msg
        :param timeout: Timeout seconds of this request
        :return: Whether succeed to send request
        """
        if resource:
            logging.debug("Issuing POST with path: " + resource.value)
            request = self.coapClient.mk_request(defines.Codes.POST, path=resource.value)
            request.token = generate_random_token(2)
            request.payload = payload

            if not enableCON:
                request.type = defines.Types["NON"]

            self.coapClient.send_request(request=request, callback=self._onPostResponse, timeout=timeout)
            return True
        else:
            logging.warning("Can't test POST - no path or path list provided.")
            return False
        pass

    def sendPutRequest(self, resource: ResourceNameEnum, payload: str, enableCON = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send data to CoAP server by requesting a PUT
        :param resource: The resource name of where to PUT
        :param payload: Data to send
        :param enableCON: Whether send a CON CoAP msg
        :param timeout: Timeout seconds of this request
        :return: Whether succeed to send request
        """
        if resource:
            logging.debug("Issuing PUT with path: " + resource.value)
            request = self.coapClient.mk_request(defines.Codes.PUT, path=resource.value)
            request.token = generate_random_token(2)
            request.payload = payload

            if not enableCON:
                request.type = defines.Types["NON"]

            self.coapClient.send_request(request=request, callback=self._onPutResponse, timeout=timeout)
            return True
        else:
            logging.warning("Can't PUT - no path or path list provided.")
            return False
        pass

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """
        Set IDataMessageListener that can be used to process data received
        :param listener: IDataMessageListener
        :return: Set successfully
        """
        self.dataMsgListener = listener
        return True
        pass

    def startObserver(self, resource: ResourceNameEnum, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        if resource:
            logging.debug("Starting an Observer on path: " + resource.value)
            self.coapClient.observe(path=resource.value, callback=self._onGetResponse, timeout=ttl)
            return True
        else:
            logging.warning("Can't Starting an Observer - no path or path list provided.")
            return False

    def stopObserver(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
            logging.debug("Stopping all Observers...")
            self.coapClient.cancel_observing(None,False)

    def stopClient(self):
        """
        Stop the client
        :return: None
        """
        self.coapClient.stop()

    def _initClient(self):
        """
        Method to init client
        :return: None
        """
        if not self.coapClient:
            self.coapClient = HelperClient(server=(self.host, self.port))
        pass


    def _onDiscoveryResponse(self, response):
        """
        Callback for process response of Discovery Request
        :param response: A list of available resources
        :return: None
        """
        if response:
            logging.info(response.pretty_print())

            # get the payload and convert to a list of paths
            self.pathList = response.payload.split(',')
            index = 0

            # the following is optional, but provides an easy way to track all the returned resource names
            for path in self.pathList:
                for char in '<\>':
                    path = path.replace(char, '')

                self.pathList[index] = path

                logging.info('  Path entry [' + str(index) + ']:' + self.pathList[index])
                index += 1
        else:
            logging.info("No response received.")

    def _onGetResponse(self, response):
        """
        Callback for process response of GET Request
        :param response: CoAP server response
        :return: None
        """
        logging.info('GET response received.')

        if response:
            logging.info("Response: "+response.pretty_print())

            #
            # NOTE: This next section is optional if you want to send a callback to the self.dataMsgListener instance
            #

            # TODO: get the URI and convert to ResourceNameEnum
            resource = None

            if self.dataMsgListener:
                self.dataMsgListener.handleIncomingMessage(resource, str(response.payload))

    def _onPutResponse(self, response):
        """
        Callback for process response of PUT Request
        :param response: CoAP server response
        :return: None
        """
        logging.info('PUT response received.')

        if response:
            logging.info("Response: "+response.pretty_print())

    def _onPostResponse(self, response):
        """
        Callback for process response of POST Request
        :param response: CoAP server response
        :return: None
        """
        logging.info('POST response received.')

        if response:
            logging.info("Response: "+response.pretty_print())

    def _onDeleteResponse(self, response):
        """
        Callback for process response of DELETE Request
        :param response: CoAP server response
        :return: None
        """
        logging.info('DELETE response received.')

        if response:
            logging.info("Response: "+response.pretty_print())