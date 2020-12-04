#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

from programmingtheiot.common import ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
	"""
	Base class for ActuatorSimTask
	
	"""

	def __init__(self, actuatorType: int = ActuatorData.DEFAULT_ACTUATOR_TYPE, simpleName: str = ConfigConst.NOT_SET):
		"""
		Init BaseActuatorSimTask with default values
		:param actuatorType: Type of actuator
		:param simpleName: Name of actuator
		"""
		self.actuatorType = actuatorType
		self.simpleName = simpleName
		self.latestActuatorData = ActuatorData(self.actuatorType, self.simpleName)
		pass
		
	def activateActuator(self, val: float) -> bool:
		"""
		Turn actuator on with given target value
		As a sim actuator, there is no real action
		:param val: Given target actuator value
		:return: If succeed to activate Actuator, always True as a sim actuator
		"""
		logging.info("\n======\nSim %s actuator ON, with value = %d.\n======" % (self.getSimpleName(), val))
		self.latestActuatorData.setCommand(ActuatorData.COMMAND_ON)
		self.latestActuatorData.setValue(val)
		return True
		pass
		
	def deactivateActuator(self) -> bool:
		"""
		Turn actuator off with given target value
		As a sim actuator, there is no real action
		:return: If succeed to deactivate Actuator, always True as a sim actuator
		"""
		logging.info("\n======\nSim %s actuator OFF.\n======" % self.getSimpleName())
		self.latestActuatorData.setCommand(ActuatorData.COMMAND_OFF)
		return True
		pass
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		"""
		Get latest actuator data
		:return: Latest ActuatorData
		"""
		return self.latestActuatorData
		pass
	
	def getSimpleName(self) -> str:
		"""
		Get name of the sim actuator
		:return: Name string
		"""
		return self.simpleName
		pass
	
	def updateActuator(self, data: ActuatorData) -> bool:
		"""
		Use ActuatorData as command:
		Update current maintained latest ActuatorData
		Use given ActuatorData to execute command
		:param data: Given ActuatorData
		:return: If succeed to update and execute
		"""
		if data is None:
			logging.error("Got an invalid ActuatorData, which is None!")
			return False
		if not isinstance(data, ActuatorData):
			logging.error("Got an invalid ActuatorData, which type is not ActuatorData!")
			return False
		if data.getCommand() is not ActuatorData.COMMAND_ON and data.getCommand() is not ActuatorData.COMMAND_OFF:
			logging.error("Got an invalid ActuatorData, whose command is invalid!")
			return False
		ret = False
		if data.getCommand() is ActuatorData.COMMAND_ON:
			ret = self.activateActuator(data.getValue())
		else:
			ret = self.deactivateActuator()
		self.latestActuatorData.updateData(data)
		self.latestActuatorData.setName(self.simpleName)
		self.latestActuatorData.setStatusCode(int(ret))
		self.latestActuatorData.setAsResponse()
		return ret
		pass
