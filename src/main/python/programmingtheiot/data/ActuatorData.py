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

    DEFAULT_RESPONSE_FLAG = False
    DEFAULT_VALUE = 0
    DEFAULT_STATE_DATA = "Default state data string"
    # for now, actuators will be 1..99
    # and displays will be 100..1999
    DEFAULT_ACTUATOR_TYPE = 0.0

    HVAC_ACTUATOR_TYPE = 1
    HUMIDIFIER_ACTUATOR_TYPE = 2
    LED_DISPLAY_ACTUATOR_TYPE = 100

    def __init__(self, actuatorType=DEFAULT_ACTUATOR_TYPE, d=None):
        super(ActuatorData, self).__init__(d=d)
        self._actuatorType = actuatorType
        self._command = self.DEFAULT_COMMAND
        self._isResponse = self.DEFAULT_RESPONSE_FLAG
        self._value = self.DEFAULT_VALUE
        self._stateData = self.DEFAULT_STATE_DATA
        pass

    def getCommand(self) -> int:
        return self._command
        pass

    def getStateData(self) -> str:
        return self._stateData
        pass

    def getValue(self) -> float:
        return self._value
        pass

    def isResponseFlagEnabled(self) -> bool:
        return True

    def setCommand(self, command: int):
        self._command = command
        pass

    def setAsResponse(self):
        self._isResponse = True
        pass

    def setStateData(self, stateData: str):
        self._stateData = stateData
        pass

    def setValue(self, val: float):
        self._value = val
        pass

    def _handleUpdateData(self, data) -> bool:
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
