from smbus import SMBus
import struct


def linearInterpolation(x_low: float, x: float, x_hi: float, y_low: float, y_hi: float) -> float:
    """
    Helper function to compute linear interpolation of a given value x, and the line i defined by two points

    :param x_low: first point x
    :type x_low: float
    :param x: Input value x
    :type x: float
    :param x_hi: second point x
    :type x_hi: float
    :param y_low: first point y
    :type y_low: float
    :param y_hi: second point y
    :type y_hi: float
    :return: the linear interpolation of given x
    :rtype: float
    """
    return (x - x_low) * (y_hi - y_low) / (x_hi - x_low) + y_low


def read2byte(i2cBus: SMBus, i2cAddr: int, lowByteAddr: int, highByteAddr: int) -> int:
    """
    Read two byte from i2c Bus by using SMBus library

    :param i2cBus: SMBus instance
    :type i2cBus: SMBus
    :param i2cAddr: i2c address, a one byte address
    :type i2cAddr: int
    :param lowByteAddr: the low byte for input address
    :type lowByteAddr: int
    :param highByteAddr: the high byte for input address
    :type highByteAddr: int
    :return: response data
    :rtype: int
    """
    data_l = i2cBus.read_byte_data(i2cAddr, lowByteAddr)
    data_h = i2cBus.read_byte_data(i2cAddr, highByteAddr)
    data = data_l | (data_h << 8)
    data = struct.unpack('h', struct.pack('H', data))[0]
    return data
