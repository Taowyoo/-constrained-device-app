#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_COMMAND = 0
	COMMAND_OFF = DEFAULT_COMMAND
	COMMAND_ON = 1

	# for now, actuators will be 1..99
	# and displays will be 100..1999
	DEFAULT_ACTUATOR_TYPE = 0
	
	HVAC_ACTUATOR_TYPE = 1
	HUMIDIFIER_ACTUATOR_TYPE = 2
	LED_DISPLAY_ACTUATOR_TYPE = 100

	def __init__(self, actuatorType = DEFAULT_ACTUATOR_TYPE, d = None):
		super(ActuatorData, self).__init__(d = d)
		pass
	
	def getCommand(self) -> int:
		pass
	
	def getStateData(self) -> str:
		pass
	
	def getValue(self) -> float:
		pass
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		pass
	
	def setAsResponse(self):
		pass
		
	def setStateData(self, stateData: str):
		pass
	
	def setValue(self, val: float):
		pass
		
	def _handleUpdateData(self, data):
		pass
		