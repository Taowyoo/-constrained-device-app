#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT


class HumidifierEmulatorTask(BaseActuatorSimTask):
    """
    Implementation of HumidifierEmulatorTask.
    According to config, choose emulated SenseHAT or real SenseHAT to execute actuation
    """

    def __init__(self):
        """
        Constructor of HumidifierEmulatorTask.
        Init emulated or not SenseHAT instance according to config.
        """
        super(HumidifierEmulatorTask, self).__init__(actuatorType=ActuatorData.HUMIDIFIER_ACTUATOR_TYPE,
                                                     simpleName="HUMIDIFIER")
        self.enableEmulation = True
        configUtil = ConfigUtil()
        enableSenseHAT = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)
        if enableSenseHAT is True:
            self.enableEmulation = False
        else:
            self.enableEmulation = True
        self.sh = SenseHAT(emulate=self.enableEmulation)
        pass

    def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
        """
        Execute actuation by print info to SenseHAT screen
        :param cmd: Command number
        :param val: Command value
        :param stateData: StateData string
        :return: Execution state number
        """
        if cmd == ActuatorData.COMMAND_ON:
            if self.sh.screen:
                msg = "{} ON with: {}".format(self.simpleName, str(val))
                logging.debug("Scroll text: {}".format(msg))
                self.sh.screen.scroll_text(text=msg)
            else:
                logging.warning("No SenseHAT LED screen instance to update.")
                return -1
        else:
            if self.sh.screen:
                msg = "{} OFF".format(self.simpleName)
                logging.debug("Scroll text: {}".format(msg))
                self.sh.screen.scroll_text(text=msg)
            else:
                logging.warning("No SenseHAT LED screen instance to clear / close.")
                return -1
        return 0
        pass

    def updateActuator(self, data: ActuatorData) -> bool:
        """
        Override super class method.
        Use _handleActuation to execute actuation
        :param data: Given ActuatorData
        :return: If succeed to update and execute
        """
        if data is None:
            logging.error("Got an invalid ActuatorData, which is None!")
            return False
        if not isinstance(data, ActuatorData):
            logging.error("Got an invalid ActuatorData, which type is not ActuatorData!")
            return False
        cmd = data.getCommand()
        if cmd != ActuatorData.COMMAND_ON and cmd != ActuatorData.COMMAND_OFF:
            logging.error("Got an invalid ActuatorData, whose command is invalid!")
            return False
        ret = self._handleActuation(cmd, data.getValue(), data.getStateData())
        self.latestActuatorData.updateData(data)
        self.latestActuatorData.setStatusCode(int(ret))
        self.latestActuatorData.setAsResponse()
        return ret >= 0
        pass
