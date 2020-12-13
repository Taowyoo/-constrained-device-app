#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

# Import logging and setup it
import logging,logging.config
logging.config.fileConfig("logging.conf")

from time import sleep

from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager


class ConstrainedDeviceApp():
	"""
	Definition of the ConstrainedDeviceApp class.
	
	"""
	
	def __init__(self):
		"""
		Initialization of class.
		
		Create DeviceDataManager instance.
		"""
		logging.info("Initializing CDA...")
		self.devDataManager = DeviceDataManager()

	def startApp(self):
		"""
		Start the CDA:
		Start DeviceDataManager.
		"""
		logging.info("Starting CDA...")
		self.devDataManager.startManager()
		logging.info("CDA started.")

	def stopApp(self, code: int):
		"""
		Stop the CDA.
		Stop DeviceDataManager.
		"""
		logging.info("CDA stopping...")
		self.devDataManager.stopManager()
		logging.info("CDA stopped with exit code %s.", str(code))
		
	def parseArgs(self, args):
		"""
		Parse command line args.
		
		@param args The arguments to parse.
		"""
		logging.info("Parsing command line args...")

def main():
	"""
	Main function definition for running client as application.
	
	Current implementation runs for 65 seconds then exits.
	"""
	run_time = ConfigUtil().getInteger(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.TEST_CDA_RUN_TIME_KEY,-1)
	cda = ConstrainedDeviceApp()
	cda.startApp()
	
	import asyncio 

	if run_time < 0:
		loop = asyncio.get_event_loop()
		try:
			loop.run_forever()
		finally:
			loop.close()
	else:
		sleep(run_time)
	cda.stopApp(0)

if __name__ == '__main__':
	"""
	Attribute definition for when invoking as app via command line
	
	"""
	main()
	