#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 by Andrew D. King
#

import logging
import unittest

from time import sleep
import sys

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector


class mccConnectorTest(unittest.TestCase):
    """
    This test case class contains very basic integration tests for
    mccConnector. It should not be considered complete,
    but serve as a starting point for the student implementing
    additional functionality within their Programming the IoT
    environment.
    """

    @classmethod
    def setUpClass(self):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing mccConnector class...")
        self.cfg = ConfigUtil()
    
    @classmethod
    def tearDownClass(self):
        sys.exit()
    
    def setUp(self):
        self.mcc = CoapClientConnector()
        pass

    def tearDown(self):
        self.mcc.stopClient()
        pass

    @unittest.skip("Ignore for now.")
    def testConnectAndDiscover(self):
        logging.info(">>>sendDiscoveryRequest")
        self.mcc.sendDiscoveryRequest(timeout=3)
        sleep(3)
    
    @unittest.skip("Ignore for now.")
    def testNon(self):
        logging.info(">>>Testing NON Requests")
        msg = "This is a put test."
        logging.info(">>>sendPutRequest")
        self.mcc.sendPutRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
                                enableCON=False, timeout=1)
        sleep(1)
        msg = "This is a post test."
        logging.info(">>>sendPostRequest")
        self.mcc.sendPostRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
                                 enableCON=False, timeout=1)
        sleep(1)
        logging.info(">>>sendGetRequest")
        self.mcc.sendGetRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=False,
                                timeout=1)
        sleep(1)
        logging.info(">>>sendDeleteRequest")
        self.mcc.sendDeleteRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=False,
                                   timeout=1)
        sleep(1)
        pass
    
    @unittest.skip("Ignore for now.")
    def testCon(self):
        logging.info(">>>Testing CON Requests")
        msg = "This is a put test."
        logging.info(">>>sendPutRequest")
        self.mcc.sendPutRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
                                enableCON=True, timeout=1)
        sleep(1)
        msg = "This is a post test."
        logging.info(">>>sendPostRequest")
        self.mcc.sendPostRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
                                 enableCON=True, timeout=1)
        sleep(1)
        logging.info(">>>sendGetRequest")
        self.mcc.sendGetRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=True,
                                timeout=1)
        sleep(1)
        logging.info(">>>sendDeleteRequest")
        self.mcc.sendDeleteRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=True,
                                   timeout=1)
        sleep(1)
        pass

    def testObserve(self):
        logging.info(">>>Testing Observe")
        msg = "Put msg to test observer."
        logging.info(">>>sendPutRequest")
        self.mcc.sendPutRequest(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, payload=msg,
                                enableCON=True, timeout=1)
        sleep(1)
        self.mcc.startObserver(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,ttl=1)
        sleep(1)
        msg = "Post msg to test observer."
        for i in range(5):
            logging.info(">>>sendPostRequest")
            self.mcc.sendPostRequest(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, payload=msg+str(i),
                                    enableCON=True, timeout=1)
            sleep(3)
        self.mcc.stopObserver(ttl=1)
        pass



if __name__ == "__main__":
    unittest.main()
    
