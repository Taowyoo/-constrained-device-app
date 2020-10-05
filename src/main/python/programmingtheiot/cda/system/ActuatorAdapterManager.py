#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, useEmulator: bool = False):
		logging.info("ActuatorAdapterManager is initializing...")
		self.useEmulator = useEmulator
		self.dataMsgListener: IDataMessageListener = None
		if self.useEmulator is True:
			logging.info("ActuatorAdapterManager is using emulator.")
		else:
			logging.info("ActuatorAdapterManager is using simulators.")
			# create the humidifier actuator
			self.humidifierActuator = HumidifierActuatorSimTask()
			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()

		pass

	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		if data.isResponse():
			logging.debug("Ignore response ActuatorData.")
			return True
		if self.useEmulator is False:
			logging.info("Sending ActuatorData to simulated Actuators.")
			if data.getActuatorType() is ActuatorData.HUMIDIFIER_ACTUATOR_TYPE:
				self.humidifierActuator.updateActuator(data)
				pass
			elif data.getActuatorType() is ActuatorData.HVAC_ACTUATOR_TYPE:
				self.hvacActuator.updateActuator(data)
				pass
			else:
				logging.warning("Got ActuatorData for Actuator that has not been simulated.")
		return True
		pass
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener is None:
			logging.info("Given DataMessageListener is invalid!")
			return False
		logging.info("Set %s as DataMessageListener." % listener.__str__())
		self.dataMsgListener = listener
		return True
		pass
