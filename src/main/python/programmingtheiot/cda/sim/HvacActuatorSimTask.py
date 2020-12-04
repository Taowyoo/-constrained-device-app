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
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HvacActuatorSimTask(BaseActuatorSimTask):
	"""
	Implementation of HumidifierActuatorSimTask

	"""

	def __init__(self, actuatorType=ActuatorData.HVAC_ACTUATOR_TYPE, simpleName=ConfigConst.HVAC_ACTUATOR_NAME):
		"""
		Init the HvacActuatorSimTask by using super class constructor with specific values
		:param actuatorType: Type of sim actuator, here is HVAC_ACTUATOR_TYPE
		:param simpleName: Name of sim actuator
		"""
		super(HvacActuatorSimTask, self).__init__(actuatorType=actuatorType, simpleName=simpleName)
		pass

