#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.BaseIotData import BaseIotData


class SystemPerformanceData(BaseIotData):
    """
    Shell representation of class for student implementation.
    
    """
    DEFAULT_VAL = 0.0

    def __init__(self, d=None):
        super(SystemPerformanceData, self).__init__(d=d)
        self._cpuUtil = self.DEFAULT_VAL
        self._diskUtil = self.DEFAULT_VAL
        self._memUtil = self.DEFAULT_VAL
        pass

    def getCpuUtilization(self) -> float:
        return self._cpuUtil
        pass

    def getDiskUtilization(self) -> float:
        return self._diskUtil
        pass

    def getMemoryUtilization(self) -> float:
        return self._memUtil
        pass

    def setCpuUtilization(self, cpuUtil):
        self._cpuUtil = cpuUtil
        pass

    def setDiskUtilization(self, diskUtil):
        self._diskUtil = diskUtil
        pass

    def setMemoryUtilization(self, memUtil):
        self._memUtil = memUtil
        pass

    def _handleUpdateData(self, data) -> bool:
        if isinstance(data, SystemPerformanceData):
            self._cpuUtil = data._cpuUtil
            self._memUtil = data._memUtil
            self._diskUtil = data._diskUtil
        else:
            return False
        return True
        pass

    def __str__(self):
        """
        Returns a string representation of this instance.

        @return The string representing this instance.
        """

        custom_str = super(SystemPerformanceData, self).__str__() + ', CpuUtilization = ' + str(self._cpuUtil) \
                     + ', DiskUtilization = ' + str(self._diskUtil) + ', MemoryUtilization = ' + str(self._memUtil)

        return custom_str
