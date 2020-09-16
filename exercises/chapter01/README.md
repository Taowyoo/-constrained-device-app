# Constrained Device Application (Connected Devices)

## Lab Module 01

<!-- Be sure to implement all the PIOT-CDA-* issues (requirements) listed at [PIOT-INF-01-001 - Chapter 01](https://github.com/orgs/programming-the-iot/projects/1#column-9974937). -->

### Description

<!-- NOTE: Include two full paragraphs describing your implementation approach by answering the questions listed below. -->

What does your implementation do? 

1. Development environment configuration

    For python CDA, I already have Anaconda with python 3.7 installed. So I just created a virtual environment by using `virtualenv` in project directory and set related configuration on Eclipse with PyDev. TODO

2. Set CI/CD for auto testing

    For CDA, I just setup a script to run lint with flake8 and run tests (those related to Lab 01) with `unittest` : [unittest workflow file](../../.github/workflows/python-app.yml)

3. Workflow(kanban board) for myself
   
    Like my GDA, I also setup a kanban board on Github Project which is similar to kanban board of our course. I named it: [Course Project - GDA](https://github.com/NU-CSYE6530-Fall2020/constrained-device-app-Taowyoo/projects/1)

How does your implementation work?

1. CI/CD with GitHub Action

    As mentioned above. The .yml files under .github/workflows/ will be read by Github and been run as task automatically when I push or pull request to specific branch. At current, I set it will be triggered on `chapter01`.

    Slightly different to our java GDA, for my python CDA, `unittest` will be used as my main test framework. 
    
    To setup it to be run in a container, the PYTHONPATH should be set:
    
    `export PYTHONPATH=${PYTHONPATH}:./src/main/python:./src/test/python`

    Then I use cmd to run unittest that related to lab 01, so there are two tests:
    1. `./src/test/python/programmingtheiot/part01/unit/common/ConfigUtilTest`
    2. `./src/test/python/programmingtheiot/part01/integration/app/ConstrainedDeviceAppTest`

    Here is how it looks like after several my push's:
    ![workflow screenshot](./pic/workflow.jpg)
    <!-- As you can see, because, the above code will run all tests in part01. So it failed because I haven't finish the part of CPU and memory code. -->

### Code Repository and Branch

<!-- NOTE: Be sure to include the branch (e.g. https://github.com/programming-the-iot/python-components/tree/alpha001). -->

URL: https://github.com/NU-CSYE6530-Fall2020/constrained-device-app-Taowyoo/tree/chapter01

### UML Design Diagram(s)

<!-- NOTE: Include one or more UML designs representing your solution. It's expected each
diagram you provide will look similar to, but not the same as, its counterpart in the
book [Programming the IoT](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/). -->

Here is the class diagram for ConstrainedDeviceApp, ConfigUtil, ConfigConst:

### Unit Tests Executed

<!-- NOTE: TA's will execute your unit tests. You only need to list each test case below
(e.g. ConfigUtilTest, DataUtilTest, etc). Be sure to include all previous tests, too,
since you need to ensure you haven't introduced regressions. -->

- programmingtheiot.part01.unit.common.ConfigUtilTest

### Integration Tests Executed

<!-- NOTE: TA's will execute most of your integration tests using their own environment, with
some exceptions (such as your cloud connectivity tests). In such cases, they'll review
your code to ensure it's correct. As for the tests you execute, you only need to list each
test case below (e.g. SensorSimAdapterManagerTest, DeviceDataManagerTest, etc.) -->

- programmingtheiot.part01.integration.app.ConstrainedDeviceAppTest

