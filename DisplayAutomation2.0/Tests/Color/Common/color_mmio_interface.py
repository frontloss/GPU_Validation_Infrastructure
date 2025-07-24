#######################################################################################################################
# @file         color_mmio_interface.py
# @brief        Contains color interface implementation for mmio read and write
# @author       Vimalesh D
#######################################################################################################################
from Libs.Core.sw_sim import driver_interface

# TO-DO Need to handle the simulation case
SIMULATION = False


##
# @brief    ColorMMioInterface for mmio read and write interface
class ColorMmioInterface:
    ##
    # @brief        Helper function to call mmio_read to get offset value
    # @param[in]    gfx_index - gfx_0 or gfx_1
    # @param[in]    offset -  MMIO offset
    # @return       offset_value
    def read(self, gfx_index: str, offset: int) -> int:
        if SIMULATION:
            pass
        else:
            return driver_interface.DriverInterface().mmio_read(offset, gfx_index)

    ##
    # @brief        Helper function to call mmio_write to write the value for offset
    # @param[in]    gfx_index - gfx_0 or gfx_1
    # @param[in]    offset - MMIO offset
    # @param[in]    value - MMIO DWORD value
    # @return       Status (True/False)
    def write(self, gfx_index: str, offset: int, value: int) -> bool:
        if SIMULATION:
            pass
        else:
            return driver_interface.DriverInterface().mmio_write(offset, value, gfx_index)
