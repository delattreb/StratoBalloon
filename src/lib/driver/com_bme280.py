from ctypes import c_short

import smbus

from dal import dal_bme280
from lib import com_logger

DEVICE = 0x76  # Default device I2C address

bus = smbus.SMBus(1)  # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1


class BME280:
    def __init__(self):
        pass
    
    @staticmethod
    def getshort(data, index):
        # return two bytes from data as a signed 16-bit value
        return c_short((data[index + 1] << 8) + data[index]).value
    
    @staticmethod
    def getushort(data, index):
        # return two bytes from data as an unsigned 16-bit value
        return (data[index + 1] << 8) + data[index]
    
    @staticmethod
    def getchar(data, index):
        # return one byte from data as a signed char
        result = data[index]
        if result > 127:
            result -= 256
        return result
    
    @staticmethod
    def getuchar(data, index):
        # return one byte from data as an unsigned char
        result = data[index] & 0xFF
        return result
    
    @staticmethod
    def readbme280id(addr = DEVICE):
        # Chip ID Register Address
        REG_ID = 0xD0
        (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
        return chip_id, chip_version
    
    def readbme280alll(self, addr = DEVICE):
        # Register Addresses
        REG_DATA = 0xF7
        REG_CONTROL = 0xF4
        REG_CONFIG = 0xF5
        
        REG_CONTROL_HUM = 0xF2
        REG_HUM_MSB = 0xFD
        REG_HUM_LSB = 0xFE
        
        # Oversample setting - page 27
        OVERSAMPLE_TEMP = 2
        OVERSAMPLE_PRES = 2
        MODE = 1
        
        # Oversample setting for humidity register - page 26
        OVERSAMPLE_HUM = 2
        bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)
        
        control = OVERSAMPLE_TEMP << 5 | OVERSAMPLE_PRES << 2 | MODE
        bus.write_byte_data(addr, REG_CONTROL, control)
        
        # Read blocks of calibration data from EEPROM
        # See Page 22 data sheet
        cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
        cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
        cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)
        
        # Convert byte data to word values
        dig_T1 = self.getushort(cal1, 0)
        dig_T2 = self.getshort(cal1, 2)
        dig_T3 = self.getshort(cal1, 4)
        
        dig_P1 = self.getushort(cal1, 6)
        dig_P2 = self.getshort(cal1, 8)
        dig_P3 = self.getshort(cal1, 10)
        dig_P4 = self.getshort(cal1, 12)
        dig_P5 = self.getshort(cal1, 14)
        dig_P6 = self.getshort(cal1, 16)
        dig_P7 = self.getshort(cal1, 18)
        dig_P8 = self.getshort(cal1, 20)
        dig_P9 = self.getshort(cal1, 22)
        
        dig_H1 = self.getuchar(cal2, 0)
        dig_H2 = self.getshort(cal3, 0)
        dig_H3 = self.getuchar(cal3, 2)
        
        dig_H4 = self.getchar(cal3, 3)
        dig_H4 = (dig_H4 << 24) >> 20
        dig_H4 = dig_H4 | (self.getchar(cal3, 4) & 0x0F)
        
        dig_H5 = self.getchar(cal3, 5)
        dig_H5 = (dig_H5 << 24) >> 20
        dig_H5 = dig_H5 | (self.getuchar(cal3, 4) >> 4 & 0x0F)
        
        dig_H6 = self.getchar(cal3, 6)
        
        # Read temperature/pressure/humidity
        data = bus.read_i2c_block_data(addr, REG_DATA, 8)
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw = (data[6] << 8) | data[7]
        
        # Refine temperature
        var1 = ((((temp_raw >> 3) - (dig_T1 << 1))) * (dig_T2)) >> 11
        var2 = (((((temp_raw >> 4) - (dig_T1)) * ((temp_raw >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1 + var2
        temperature = float(((t_fine * 5) + 128) >> 8)
        
        # Refine pressure and adjust for temperature
        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * dig_P6 / 32768.0
        var2 = var2 + var1 * dig_P5 * 2.0
        var2 = var2 / 4.0 + dig_P4 * 65536.0
        var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * dig_P1
        if var1 == 0:
            pressure = 0
        else:
            pressure = 1048576.0 - pres_raw
            pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
            var1 = dig_P9 * pressure * pressure / 2147483648.0
            var2 = pressure * dig_P8 / 32768.0
            pressure = pressure + (var1 + var2 + dig_P7) / 16.0
        
        # Refine humidity
        humidity = t_fine - 76800.0
        humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
        humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
        if humidity > 100:
            humidity = 100
        elif humidity < 0:
            humidity = 0
        
        return temperature / 100.0, pressure / 100.0, humidity
    
    def read(self, name, connection, cursor, setdb = True):
        temperature, pressure, humidity = self.readbme280alll()
        if setdb:
            # Inssert into database
            dal = dal_bme280.DAL_BME280(connection, cursor)
            dal.set_bme280(name, temperature, humidity, pressure)
        
        # Log
        logger = com_logger.Logger(name)
        logger.debug('Temp: ' + str(temperature) + ' Hum: ' + str(humidity) + ' Pre: ' + str(pressure))
        
        return temperature, humidity, pressure
