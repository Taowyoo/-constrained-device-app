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

class SystemMemUtilTask(BaseSystemUtilTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		"""
		Initialization of class: SystemMemUtilTask.
		Initialize the instance by calling super class init method.
		"""
		super(SystemMemUtilTask, self).__init__()
		self.simpleName = 'SystemMemUtil'
		pass

	def _getSystemUtil(self) -> float:
		"""
		Implement the template method for getting system cpu util info

		Retrieve the current system virtual memory occupied percentage value as a float by using method virtual_memory()
		in psutil.

		@return float System virtual memory occupied percentage
		"""
		return psutil.virtual_memory().percent
		pass
