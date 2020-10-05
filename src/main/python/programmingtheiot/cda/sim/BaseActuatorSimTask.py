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

from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, actuatorType: int = ActuatorData.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
		self.actuatorType = actuatorType
		self.simpleName = simpleName
		self.latestActuatorData = ActuatorData(self.actuatorType)
		pass
		
	def activateActuator(self, val: float) -> bool:
		logging.info(f"Sim actuator received a ON command with value = {val}.")
		self.latestActuatorData.setCommand(ActuatorData.COMMAND_ON)
		self.latestActuatorData.setValue(val)
		return True
		pass
		
	def deactivateActuator(self) -> bool:
		logging.info(f"Sim actuator received a OFF command.")
		self.latestActuatorData.setCommand(ActuatorData.COMMAND_OFF)
		return True
		pass
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		return self.latestActuatorData
		pass
	
	def getSimpleName(self) -> str:
		return self.simpleName
		pass
	
	def updateActuator(self, data: ActuatorData) -> bool:
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
		self.latestActuatorData.setStatusCode(int(ret))
		self.latestActuatorData.setAsResponse()
		return ret
		pass
