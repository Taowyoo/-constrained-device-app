#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
from programmingtheiot.common import ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData


class SystemPerformanceData(BaseIotData):
    """
    Data object for storing System Performance info:

    System cpu occupied percentage
    System memory occupied percentage
    System disk occupied bytes
    """
    DEFAULT_VAL = 0.0

    def __init__(self, name: str = ConfigConst.SYS_PERF_DATA, d=None):
        """
        Constructor of SystemPerformanceData:

        Init variables with default value or given dict
        :param d: dict to help init the object
        """
        super(SystemPerformanceData, self).__init__(name=name, d=d)
        if d:
            self.cpuUtil = d.get('cpuUtil', self.DEFAULT_VAL)
            self.diskUtil = d.get('diskUtil', self.DEFAULT_VAL)
            self.memUtil = d.get('memUtil', self.DEFAULT_VAL)
        else:
            self.cpuUtil = self.DEFAULT_VAL
            self.diskUtil = self.DEFAULT_VAL
            self.memUtil = self.DEFAULT_VAL
        pass

    def getCpuUtilization(self) -> float:
        """
        Return System cpu occupied percentage
        :return: Percentage value
        """
        return self.cpuUtil
        pass

    def getDiskUtilization(self) -> float:
        """
        Return System disk occupied bytes
        :return: Bytes valueB
        """
        return self.diskUtil
        pass

    def getMemoryUtilization(self) -> float:
        """
        Return System disk occupied percentage
        :return: Percentage value
        """
        return self.memUtil
        pass

    def setCpuUtilization(self, cpuUtil):
        """
        Set System cpu occupied percentage
        :param cpuUtil: Given value
        """
        self.cpuUtil = cpuUtil
        pass

    def setDiskUtilization(self, diskUtil):
        """
        Set System cpu occupied bytes
        :param diskUtil: Given value
        """
        self.diskUtil = diskUtil
        pass

    def setMemoryUtilization(self, memUtil):
        """
        Set System memory occupied percentage
        :param memUtil: Given value
        """
        self.memUtil = memUtil
        pass

    def _handleUpdateData(self, data) -> bool:
        """
        Use given data to update current instance
        :param data: Given SystemPerformanceData
        :return: If update successfully
        """
        if isinstance(data, SystemPerformanceData):
            self.cpuUtil = data.cpuUtil
            self.memUtil = data.memUtil
            self.diskUtil = data.diskUtil
        else:
            return False
        return True
        pass

    def __str__(self):
        """
        Returns a string representation of this instance.

        @return The string representing this instance.
        """

        custom_str = super(SystemPerformanceData, self).__str__() + ', CpuUtilization = ' + str(self.cpuUtil) \
                     + ', DiskUtilization = ' + str(self.diskUtil) + ', MemoryUtilization = ' + str(self.memUtil)

        return custom_str
