from smbus import SMBus
import struct


def linearInterpolation(x_low: float, x: float, x_hi: float, y_low: float, y_hi: float) -> float:
    return (x - x_low) * (y_hi - y_low) / (x_hi - x_low) + y_low


def read2byte(i2cBus: SMBus, i2cAddr: int, lowByteAddr: int, highByteAddr: int) -> int:
    data_l = i2cBus.read_byte_data(i2cAddr, lowByteAddr)
    data_h = i2cBus.read_byte_data(i2cAddr, highByteAddr)
    data = data_l | (data_h << 8)
    data = struct.unpack('h', struct.pack('H', data))[0]
    return data
