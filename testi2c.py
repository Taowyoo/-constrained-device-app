import smbus
import struct
import pisense
se = pisense.SenseEnviron()
print(se.temperature)
print(se.pressure)
print(se.humidity)
# init the I2C bus at the humidity address
# WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
# senseHAT info: https://pinout.xyz/pinout/sense_hat
i2cBus = smbus.SMBus(1)


def read2byte(i2cAddr: int, lowByteAddr: int, highByteAddr: int) -> int:
    data_l = i2cBus.read_byte_data(i2cAddr, lowByteAddr)
    data_h = i2cBus.read_byte_data(i2cAddr, highByteAddr)
    data = data_l | (data_h << 8)
    data = struct.unpack('h', struct.pack('H', data))[0]
    return data


humidAddr = 0x5F  # hts221, doc: https://www.st.com/resource/en/datasheet/hts221.pdf
pressAddr = 0x5C  # lps25h, doc: https://www.pololu.com/file/0J761/LPS25H.pdf


# read pressure sensor tempreture
TEMP_OUT_L = 0x2B
TEMP_OUT_H = 0x2C
# Temperature data are expressed as TEMP_OUT_H & TEMP_OUT_L as 2’s complement numbers
temp = read2byte(pressAddr, TEMP_OUT_L, TEMP_OUT_H)
temp = 42.5 + (temp / 480)
print('pressure sensor, tempreture:', temp)

# read pressure sensor pressure
PRESS_OUT_XL = 0x28
PRESS_OUT_L = 0x29
PRESS_OUT_H = 0x2A
press_xl = i2cBus.read_byte_data(pressAddr, PRESS_OUT_XL)
press_l = i2cBus.read_byte_data(pressAddr, PRESS_OUT_L)
press_h = i2cBus.read_byte_data(pressAddr, PRESS_OUT_H)
"""
The full reference pressure value is composed by PRESS_OUT_H/_L/_XL and is represented as 2’s complement.
Pressure Values exceeding the operating pressure Range are clipped.
"""
press = (press_h << 16) | (press_l << 8) | press_xl
press /= 4096
print('pressure sensor, pressure:', press)


# linear Interpolation helper function for hts221 humidity sensor
def linearInterpolation(x_low: float, x: float, x_hi: float, y_low: float, y_hi: float) -> float:
    return (x - x_low) * (y_hi - y_low) / (x_hi - x_low) + y_low


# read humidity sensor tempreture
# # T0_OUT
# T0_OUT_L = 0x3C
# T0_OUT_H = 0x3D
# T0_OUT = read2byte(humidAddr, T0_OUT_L, T0_OUT_H)
# # T1_OUT
# T1_OUT_L = 0x3E
# T1_OUT_H = 0x3F
# T1_OUT = read2byte(humidAddr, T1_OUT_L, T1_OUT_H)
# # T0_degC_x8
# T0_degC_x8_ADDR = 0x32
# T0_degC_x8 = i2cBus.read_byte_data(humidAddr, T0_degC_x8_ADDR)
# T0_degC = (T0_degC_x8 | (1 << (T0_degC_x8.bit_length() - 1 ))) / 8
# print('T0_degC',T0_degC)
# # T1_degC_x8
# T1_degC_x8_ADDR = 0x33
# T1_degC_x8 = i2cBus.read_byte_data(humidAddr, T1_degC_x8_ADDR)
# T1_degC = (T1_degC_x8 | (1 << (T1_degC_x8.bit_length() - 1))) / 8
# print('T1_degC',T1_degC)

# # TEMP_OUT
# TEMP_OUT_L = 0x2A
# TEMP_OUT_H = 0x2B
# TEMP_OUT = read2byte(humidAddr, TEMP_OUT_L, TEMP_OUT_H)

# temperature = linearInterpolation(T0_OUT, TEMP_OUT, T1_OUT, T1_degC, T0_degC)
# print('humidity sensor, tempreture:', temperature)



# read humidity sensor humidity
# H0_T0_OUT
H0_T0_OUT_L = 0x36
H0_T0_OUT_H = 0x37
H0_T0_OUT = read2byte(humidAddr, H0_T0_OUT_L, H0_T0_OUT_H)
# H1_T0_OUT
H1_T0_OUT_L = 0x3A
H1_T0_OUT_H = 0x3B
H1_T0_OUT = read2byte(humidAddr, H1_T0_OUT_L, H1_T0_OUT_H)
# H0_rH_x2
H0_rH_x2_ADDR = 0x30
H0_rH_x2 = i2cBus.read_byte_data(humidAddr, H0_rH_x2_ADDR)
H0_rH = H0_rH_x2 / 2
# H1_rH_x2
H1_rH_x2_ADDR = 0x31
H1_rH_x2 = i2cBus.read_byte_data(humidAddr, H1_rH_x2_ADDR)
H1_rH = H1_rH_x2 / 2
# H_OUT
HUMIDITY_OUT_L = 0x28
HUMIDITY_OUT_H = 0x29
HUMIDITY_OUT = read2byte(humidAddr, HUMIDITY_OUT_L, HUMIDITY_OUT_H)

# Linear interpolation
humidity = linearInterpolation(H0_T0_OUT, HUMIDITY_OUT, H1_T0_OUT, H0_rH, H1_rH)
# humidity = H0_rH + (H1_rH - H0_rH) * (HUMIDITY_OUT - H0_T0_OUT) / (H1_T0_OUT - H0_T0_OUT)
print('humidity sensor, humidity:',humidity)
