#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import json
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	"""
	Data util class for encoding or decoding SystemPerformanceData, SensorData, ActuatorData.
	Data will be encoded or decoded in json format, which will be suit for network transmission
	"""

	def __init__(self, encodeToUtf8 = False):
		"""
		Constructor of DataUtil, init some setting parameters
		:param encodeToUtf8: Whether encode Object in UTF8 install of default ascii
		"""
		self.encodeToUtf8 = encodeToUtf8
		pass

	def actuatorDataToJson(self, actuatorData: ActuatorData) -> str:
		"""
		Encode ActuatorData to json string
		:param actuatorData: Given ActuatorData
		:return: Encoded json string of ActuatorData
		"""
		if self.encodeToUtf8:
			jsonData: str = json.dumps(actuatorData, indent=4, cls=JsonDataEncoder, ensure_ascii=False).encode('utf8')
		else:
			jsonData: str = json.dumps(actuatorData, indent=4, cls=JsonDataEncoder, ensure_ascii=True)
		return jsonData

	def sensorDataToJson(self, sensorData: SensorData) -> str:
		"""
		Encode SensorData to json string
		:param sensorData: Given SensorData
		:return: Encoded json string of SensorData
		"""
		if self.encodeToUtf8:
			jsonData: str = json.dumps(sensorData, indent=4, cls=JsonDataEncoder, ensure_ascii=False).encode('utf8')
		else:
			jsonData: str = json.dumps(sensorData, indent=4, cls=JsonDataEncoder, ensure_ascii=True)
		return jsonData

	def systemPerformanceDataToJson(self, sysPerfData: SystemPerformanceData) -> str:
		"""
		Encode SystemPerformanceData to json string
		:param sysPerfData: Given SystemPerformanceData
		:return: Encoded json string of SystemPerformanceData
		"""
		if self.encodeToUtf8:
			jsonData: str = json.dumps(sysPerfData, indent=4, cls=JsonDataEncoder, ensure_ascii=False).encode('utf8')
		else:
			jsonData: str = json.dumps(sysPerfData, indent=4, cls=JsonDataEncoder, ensure_ascii=True)
		return jsonData

	def jsonToActuatorData(self, jsonData) -> ActuatorData:
		"""
		Convert json string to ActuatorData Instance
		:param jsonData: Given json string
		:return: Decoded ActuatorData Instance
		"""
		adDict: dict = json.loads(jsonData)
		ad = ActuatorData(d=adDict)
		return ad

	def jsonToSensorData(self, jsonData) -> SensorData:
		"""
		Convert json string to SensorData Instance
		:param jsonData: Given json string
		:return: Decoded SensorData Instance
		"""
		sdDict: dict = json.loads(jsonData)
		sd = SensorData(d=sdDict)
		return sd

	def jsonToSystemPerformanceData(self, jsonData) -> SystemPerformanceData:
		"""
		Convert json string to SystemPerformanceData Instance
		:param jsonData: Given json string
		:return: Decoded SystemPerformanceData Instance
		"""
		sysPerDict: dict = json.loads(jsonData)
		sysPerData = SystemPerformanceData(d=sysPerDict)
		return sysPerData

class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		"""
		Override default JSONEncoder method
		:param o: Given object
		:return: Use dict format of object as the way to encode object
		"""
		return o.__dict__
