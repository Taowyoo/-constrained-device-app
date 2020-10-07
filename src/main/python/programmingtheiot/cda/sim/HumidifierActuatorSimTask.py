#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
	Implementation of HumidifierActuatorSimTask
	
	"""
	DEFAULT_NAME = "HUMIDIFIER"

	def __init__(self, actuatorType=ActuatorData.HUMIDIFIER_ACTUATOR_TYPE, simpleName=DEFAULT_NAME):
		"""
		Init the HumidifierActuatorSimTask by using super class constructor with specific values
		:param actuatorType: Type of sim actuator, here is HUMIDIFIER_ACTUATOR_TYPE
		:param simpleName: Name of sim actuator, here is {DEFAULT_NAME}
		"""
		super(HumidifierActuatorSimTask, self).__init__(actuatorType=actuatorType,
														simpleName=simpleName)
		pass
