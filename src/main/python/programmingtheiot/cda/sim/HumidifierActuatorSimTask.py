#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
#
from programmingtheiot.common import ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
	Implementation of HumidifierActuatorSimTask
	
	"""

	def __init__(self, actuatorType=ActuatorData.HUMIDIFIER_ACTUATOR_TYPE, simpleName=ConfigConst.HUMIDIFIER_ACTUATOR_NAME):
		"""
		Init the HumidifierActuatorSimTask by using super class constructor with specific values
		:param actuatorType: Type of sim actuator, here is HUMIDIFIER_ACTUATOR_TYPE
		:param simpleName: Name of sim actuator
		"""
		super(HumidifierActuatorSimTask, self).__init__(actuatorType=actuatorType,
														simpleName=simpleName)
		pass
