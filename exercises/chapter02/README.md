# Constrained Device Application (Connected Devices)

## Lab Module 02


### Description

What does your implementation do? 

1. Implement the logic of getting system util data:
   1. Implement Classes: `BaseSystemUtilTask`, `SystemCpuUtilTask`, `SystemMemUtilTask`.
   2. Implement Class: `SystemPerformanceManager`.
   3. Integrate `SystemPerformanceManager` with `SystemCpuUtilTask` and `SystemMemUtilTask`.
   4. Integrate `ConstrainedDeviceApp` with `SystemPerformanceManager`

How does your implementation work?

1. `SystemCpuUtilTask` and `SystemMemUtilTask` is subclass of `BaseSystemUtilTask`, implement the template method to retrieve System Util Info: CPU occupied percentage and Memory occupied percentage.
2. `SystemPerformanceManager` call `SystemCpuUtilTask` and `SystemMemUtilTask` to retrieve Telemetry value and generate Telemetry `SensorData`.
3. `SystemPerformanceManager` use `BackgroundScheduler` to periodically call `SystemCpuUtilTask` and `SystemMemUtilTask` to get Telemetry value according to given `pollRate` which default value is 30 seconds.
4. `ConstrainedDeviceApp`  creates an instance of `SystemPerformanceManager` and start it.

### Code Repository and Branch

URL: https://github.com/NU-CSYE6530-Fall2020/constrained-device-app-Taowyoo

### UML Design Diagram(s)

Here is the UML class diagram of classes we edited so far:
![lab 02 class diagram](./../../doc/UML/Lab02.svg)

### Unit Tests Executed

- ConfigUtilTest
- SystemCpuUtilTaskTest
- SystemMemUtilTaskTest

### Integration Tests Executed

- ConstrainedDeviceAppTest
- SystemPerformanceManagerTest
