#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import psutil

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemCpuUtilTask(BaseSystemUtilTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		"""
		Initialization of class: SystemCpuUtilTask.
		"""
		super(SystemCpuUtilTask, self).__init__()
		pass
	
	def _getSystemUtil(self) -> float:
		"""
		Implement the template method for getting current system CPU occupied percentage

		Retrieve the current system CPU occupied percentage value as a float by using method cpu_percent() in psutil.

		@return float System CPU occupied percentage
		"""
		return psutil.cpu_percent()
		pass
