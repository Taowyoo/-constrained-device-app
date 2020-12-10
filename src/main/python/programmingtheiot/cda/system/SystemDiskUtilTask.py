#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import shutil

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
from programmingtheiot.common import ConfigConst


class SystemDiskUtilTask(BaseSystemUtilTask):
	"""
	SystemDiskUtilTask
	"""

	def __init__(self):
		"""
		Initialization of class: SystemDiskUtilTask.
		Initialize the instance by calling super class init method.
		"""
		super(SystemDiskUtilTask, self).__init__()
		self.simpleName = ConfigConst.DISK_UTIL_NAME
		pass

	def _getSystemUtil(self) -> float:
		"""
		Implement the disk method for getting system disk util info

		Retrieve the current disk occupied percentage of root dir value as a float by using method disk_usage(path)
		in shutil.

		@return float System disk occupied percentage of root dir
		"""
		return shutil.disk_usage('/').used/shutil.disk_usage('/').total
		pass
