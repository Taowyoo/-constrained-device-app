#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from programmingtheiot.data.SensorData import SensorData

class BaseSystemUtilTask():
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self):
		"""
		Initialization of class: BaseSystemUtilTask.
		Set latestSensorData default value to None
		"""
		self.latestSensorData = None
		pass
	
	def generateTelemetry(self) -> SensorData:
		"""
		Retrieve the telemetry value from method _getSystemUtil, package the row data into SensorData.
		Update latestSensorData and return it.
		@return SensorData Packaged latest sensor data
		"""
		sensor_date = SensorData()
		sensor_date.setName('SystemUtilData')
		sensor_date.setValue(self._getSystemUtil())
		self.latestSensorData = sensor_date
		return self.latestSensorData
		pass
		
	def getTelemetryValue(self) -> float:
		"""
		Retrieve the telemetry value as a float from template method _getSystemUtil.

		@return float Telemetry value
		"""
		val = self._getSystemUtil()
		logging.info(self.__class__.__name__ + ": Got telemetry value: " + str(val))
		return val
		pass
	
	def _getSystemUtil(self) -> float:
		"""
		Template method implemented by sub-class.
		
		Retrieve the system utilization value as a float.
		
		@return float System utilization value
		"""
		pass
		