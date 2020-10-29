
import logging
import unittest

from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter
from programmingtheiot.data.SensorData import SensorData

class RedisClientAdapterTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing PersistenceClientAdapterTest class...")
        self.redisPersistenceAdapter = RedisPersistenceAdapter()
        self.assertIsNotNone(self, obj=self.redisPersistenceAdapter, msg="Cannot construct RedisPersistenceAdapter instance!")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnectClient(self):
        logging.info("Testing connectClient method...")
        ret = self.redisPersistenceAdapter.connectClient()
        self.assertTrue(ret)
        logging.info("Test connectClient method finished.\n")
        pass

    def testDisconnectClient(self):
        logging.info("Testing disconnectClient method...")
        ret = self.redisPersistenceAdapter.disconnectClient()
        self.assertTrue(ret)
        logging.info("Test disconnectClient method finished.\n")
        pass

    def testStoreSensorData(self):
        logging.info("Testing storeData method...")
        ret = self.redisPersistenceAdapter.connectClient()
        self.assertTrue(ret)
        testData = SensorData()
        testData.setName('TestRedisClientAdapter')
        testData.setValue(123.456)
        ret = self.redisPersistenceAdapter.storeData(testData, ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)
        self.assertTrue(ret)
        ret = self.redisPersistenceAdapter.disconnectClient()
        self.assertTrue(ret)
        logging.info("Test storeData method finished.\n")
        pass



if __name__ == "__main__":
    unittest.main()

