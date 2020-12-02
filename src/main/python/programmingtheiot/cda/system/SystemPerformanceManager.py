#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class SystemPerformanceManager(object):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, pollRate: int = 30):
        """
        Initialization of class: SystemPerformanceManager.
        Setup BackgroundScheduler to pull sensor data with poll rate in background.
        @:parameter pollRate The rate of pulling messages.
        """
        logging.info("Initializing SystemPerformanceManager...")
        # Create tasks
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        # Initialize sensor data values
        self.cpuUtilPct: float = None
        self.memUtilPct: float = None
        # Initialize dataMsgListener
        self.dataMsgListener: IDataMessageListener = None
        # Initialize BackgroundScheduler
        self.scheduler = BackgroundScheduler()
        # Setup the BackgroundScheduler
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=pollRate)
        pass

    def handleTelemetry(self):
        """
        Get system performance telemetry and send it to dataMsgListener as SystemPerformanceData
        :return:
        """
        cpuVal = self.cpuUtilTask.getTelemetryValue()
        memVal = self.memUtilTask.getTelemetryValue()
        sysPerfData = SystemPerformanceData()
        sysPerfData.setCpuUtilization(cpuVal)
        sysPerfData.setMemoryUtilization(memVal)
        logging.info('CPU utilization is %s percent, and memory utilization is %s percent.',
                     str(cpuVal), str(memVal))
        self.dataMsgListener.handleSystemPerformanceMessage(sysPerfData)
        pass

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener is None:
            return False
        self.dataMsgListener = listener
        return True
        pass

    def startManager(self):
        """
        Start the SystemPerformanceManager.

        """
        logging.info("Starting SystemPerformanceManager...")
        self.scheduler.start()
        logging.info("SystemPerformanceManager started.")
        pass

    def stopManager(self):
        """
        Stop the SystemPerformanceManager.

        """
        logging.info("SystemPerformanceManager stopping...")
        self.scheduler.shutdown()
        logging.info("SystemPerformanceManager stopped.")
        pass
