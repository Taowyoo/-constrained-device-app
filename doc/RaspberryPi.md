# Note for setting RaspberryPi

## SenseHAT

### Problems Solved

#### SenseHat

1. Basice python dependencies

    ```bash
    sudo apt-get install sense-hat
    ```

2. RTIMU not found

- Description

    When use pisense or sense_hat library to do operation on SenseHAT:
    ```python
    # use sense_hat
    from sense_hat import SenseHat
    sense = SenseHat()
    # use pisense
    from pisense import SenseHAT
    sh = SenseHAT(emulate=False)
    ```
    May meet may occur RTIMU module not found problem:

    `ImportError: no module named RTIMU`

- Solution

    Install RTIMU lib:

    `pip install RTIMULib`

3. SenseHat cannot be detected

- Description

    When use pisense or sense_hat library to do operation on SenseHAT, may meet following error:

    `OSError: Cannot detect RPi-Sense FB device`

- Solution

    Try following method one by one:

    1. enabling the dev-tree

        `sudo raspi-config and turning it on in Advanced options`


    2. enabling i2c

        `sudo raspi-config and turning it on in Advanced options`

    3. Modify config of raspberry pi

        Add `dtoverlay=rpi-sense` to the bottom of `/boot/config.txt` then reboot
