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
    Data object for storing Actuator command info
    """
    # Default commands
    DEFAULT_COMMAND = 0
    COMMAND_OFF = DEFAULT_COMMAND
    COMMAND_ON = 1

    DEFAULT_RESPONSE_FLAG = False
    DEFAULT_VALUE = 0
    DEFAULT_STATE_DATA = "Default state data string"
    # for now, actuators will be 1..99
    # and displays will be 100..1999

    # Actuator types
    DEFAULT_ACTUATOR_TYPE = 0.0
    HVAC_ACTUATOR_TYPE = 1
    HUMIDIFIER_ACTUATOR_TYPE = 2
    LED_DISPLAY_ACTUATOR_TYPE = 100

    def __init__(self, actuatorType=DEFAULT_ACTUATOR_TYPE, d=None):
        """
        Constructor of ActuatorData:

        Init variables with default value or given dict
        :param d: dict to help init the object
        """
        super(ActuatorData, self).__init__(d=d)
        if d:
            self._actuatorType = d['actuatorType']
            self._command = d['command']
            self._isResponse = d['isResponse']
            self._value = d['value']
            self._stateData = d['stateData']
        else:
            self._actuatorType = actuatorType
            self._command = self.DEFAULT_COMMAND
            self._isResponse = self.DEFAULT_RESPONSE_FLAG
            self._value = self.DEFAULT_VALUE
            self._stateData = self.DEFAULT_STATE_DATA
        pass

    def getActuatorType(self) -> int:
        """
        Return Actuator Type
        :return: Type number
        """
        return self._actuatorType

    def getCommand(self) -> int:
        """
        Return Actuator Command
        :return: Command number
        """
        return self._command
        pass

    def getStateData(self) -> str:
        """
        Return State Data
        :return: State Data String
        """
        return self._stateData
        pass

    def getValue(self) -> float:
        """
        Return Actuator Data value
        :return: Actuator Data value
        """
        return self._value
        pass

    def isResponseFlagEnabled(self) -> bool:
        """
        Check whether Response Flag is enabled
        :return: True, as flag has been implemented
        """
        return True

    def setCommand(self, command: int):
        """
        Set Command
        :param command: Given command number, should use variables in ActuatorData
        """
        self._command = command
        pass

    def setAsResponse(self):
        """
        Set current ActuatorData is a response
        """
        self._isResponse = True
        pass

    def isResponse(self) -> bool:
        """
        Check Whether current ActuatorData is a response
        :return: Whether current ActuatorData is a response
        """
        return self._isResponse
        pass

    def setStateData(self, stateData: str):
        """
        Set state data
        :param stateData: State data string
        """
        self._stateData = stateData
        pass

    def setValue(self, val: float):
        """
        Set actuator target value
        :param stateData: Actuator value
        """
        self._value = val
        pass

    def _handleUpdateData(self, data) -> bool:
        """
        Use given data to update current instance
        :param data: Given ActuatorData
        :return: If update successfully
        """
        if isinstance(data, ActuatorData):
            self._actuatorType = data._actuatorType
            self._value = data._value
            self._command = data._command
            self._stateData = data._stateData
            self._isResponse = data._isResponse
        else:
            return False
        return True
        pass

    def __str__(self):
        """
        Returns a string representation of this instance.

        @return The string representing this instance.
        """

        custom_str = super(ActuatorData, self).__str__() + ', actuatorType=' + str(self._actuatorType) \
                     + ', value=' + str(self._value) + ', command=' + str(self._command) \
                     + ', isResponse=' + str(self._isResponse) + ', stateData=' + str(self._stateData)

        return custom_str
