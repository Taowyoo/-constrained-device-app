#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

class ActuatorAdapterManager(object):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, useEmulator: bool = False):
        logging.info("ActuatorAdapterManager is initializing...")
        self.useEmulator = useEmulator
        self.dataMsgListener: IDataMessageListener = None
        if self.useEmulator is True:
            logging.info("ActuatorAdapterManager is using emulator.")
            # create emulated humidifier actuator
            humidifierModule = __import__('programmingtheiot.cda.emulated.HumidifierEmulatorTask',
                                          fromlist=['HumidifierEmulatorTask'])
            humidifierClass = getattr(humidifierModule, 'HumidifierEmulatorTask')
            self.humidifierEmulator = humidifierClass()
            # create emulated HVAC actuator
            hvacModule = __import__('programmingtheiot.cda.emulated.HvacEmulatorTask',
                                          fromlist=['HvacEmulatorTask'])
            hvacClass = getattr(hvacModule, 'HvacEmulatorTask')
            self.hvacEmulator = hvacClass()
            # create emulated LED Display
            ledModule = __import__('programmingtheiot.cda.emulated.LedDisplayEmulatorTask',
                                    fromlist=['LedDisplayEmulatorTask'])
            ledClass = getattr(ledModule, 'LedDisplayEmulatorTask')
            self.ledEmulator = ledClass()
        else:
            logging.info("ActuatorAdapterManager is using simulators.")
            # create simulated humidifier actuator
            self.humidifierActuator = HumidifierActuatorSimTask()
            # create simulated HVAC actuator
            self.hvacActuator = HvacActuatorSimTask()

        pass

    def sendActuatorCommand(self, data: ActuatorData) -> bool:
        logging.debug("Got ActuatorData: {}".format(data.__str__()))
        if data.isResponse():
            logging.info("Ignore response ActuatorData.")
            return True
        if self.useEmulator is False:
            logging.info("Sending ActuatorData to simulated Actuators.")
            if data.getActuatorType() is ActuatorData.HUMIDIFIER_ACTUATOR_TYPE:
                self.humidifierActuator.updateActuator(data)
                pass
            elif data.getActuatorType() is ActuatorData.HVAC_ACTUATOR_TYPE:
                self.hvacActuator.updateActuator(data)
                pass
            else:
                logging.warning("Got ActuatorData for Actuator that has not been simulated.")
        else:
            logging.info("Sending ActuatorData to emulated Actuators.")
            if data.getActuatorType() is ActuatorData.HUMIDIFIER_ACTUATOR_TYPE:
                self.humidifierEmulator.updateActuator(data)
                pass
            elif data.getActuatorType() is ActuatorData.HVAC_ACTUATOR_TYPE:
                self.hvacEmulator.updateActuator(data)
                pass
            elif data.getActuatorType() is ActuatorData.LED_DISPLAY_ACTUATOR_TYPE:
                self.ledEmulator.updateActuator(data)
                pass
            else:
                logging.warning("Got ActuatorData for Actuator that has not been simulated.")
        return True
        pass

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener is None:
            logging.info("Given DataMessageListener is invalid!")
            return False
        logging.info("Set %s as DataMessageListener." % listener.__str__())
        self.dataMsgListener = listener
        return True
        pass
