########################################################################################################################
# @file     brightness_args.py
# @brief    Python wrapper which contains structures used for Brightness3 funtionality.
# @author   Vinod D S
########################################################################################################################
import ctypes


##
# @brief        DXGK_BRIGHTNESS_SENSOR_DATA_CHROMATICITY Structure
class DXGK_BRIGHTNESS_SENSOR_DATA_CHROMATICITY(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('ChromaticityX', ctypes.c_float),
        ('ChromaticityY', ctypes.c_float)
    ]


##
# @brief        DXGK_BRIGHTNESS_SENSOR_DATA Structure
class DXGK_BRIGHTNESS_SENSOR_DATA(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('Size', ctypes.c_uint32),
        ('SensorData', ctypes.c_uint32),
        ('AlsReading', ctypes.c_float),
        ('Chromaticity', DXGK_BRIGHTNESS_SENSOR_DATA_CHROMATICITY),
        ('ColorTemperature', ctypes.c_float)
    ]


##
# @brief        DXGK_BRIGHTNESS_SET_IN Structure
class DXGK_BRIGHTNESS_SET_IN(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ('BrightnessMillinits', ctypes.c_uint32),
        ('TransitionTimeMs', ctypes.c_uint32),
        ('SensorReadings', DXGK_BRIGHTNESS_SENSOR_DATA)
    ]


##
# @brief        BCMEntryFields Structure
class BCMEntryFields(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('DesiredDutyCycle', ctypes.c_uint32, 16),
        ('BrightnessPercent', ctypes.c_uint32, 7),
        ('Reserved', ctypes.c_uint32, 8),
        ('FieldValidBit', ctypes.c_uint32, 1),
    ]


##
# @brief        BCMEntry Union
class BCMEntry(ctypes.Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', BCMEntryFields),
        ('byte_data', ctypes.c_ubyte * 4)
    ]

    ##
    # @brief       Function to get the string format of BCLMEntry object
    # @return      string representation of the BCLMEntry object
    def __repr__(self):
        return "FieldValidBit= {0}, BrightnessPercent= {1}, DesiredDutyCycle= {2}, ByteData= 0x{3}".format(
            self.FieldValidBit, self.BrightnessPercent, self.DesiredDutyCycle, bytearray(self.byte_data).hex())


##
# @brief        BCLMEntryFields Structure
class BCLMEntryFields(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('DutyCycle', ctypes.c_uint16, 8),
        ('Percent', ctypes.c_uint16, 7),
        ('ValidBit', ctypes.c_uint16, 1),
    ]



##
# @brief        BCLMEntry Union
class BCLMEntry(ctypes.Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', BCLMEntryFields),
        ('byte_data', ctypes.c_ubyte * 2)
    ]

    ##
    # @brief       Function to get the string format of BCLMEntry object
    # @return      string representation of the BCLMEntry object
    def __repr__(self):
        return "ValidBit= {0}, Percent= {1}, DutyCycle= {2}, ByteData= 0x{3}".format(
            self.ValidBit, self.Percent, self.DutyCycle, bytearray(self.byte_data).hex())
