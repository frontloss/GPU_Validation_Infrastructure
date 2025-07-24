##
# @file         ptl_clock_helper.py
# @brief        Contains helper methods for PTL clock verifications
# @author       Kiran Kumar Lakshmanan

import logging
from typing import List, Tuple, Dict

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen15 import Gen15NonAutoGenRegs


##
# @brief    Helper class for PTL clock related methods.
class PtlClockHelper:
    # Map of ddi to bspec name convention
    ddi_to_bspec_name_map = dict([
        ('A', 'A'),
        ('B', 'B'),
        ('F', 'USBC1'),
        ('G', 'USBC2'),
        ('H', 'USBC3'),
        ('I', 'USBC4')
    ])

    ##
    # @brief        Get maximum DDI symbol clock frequency for active displays
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @param[in]    ports: List[str]
    #                   List of port names for active display
    # @return       (target_id, symbol_clock_frequency): (int, float)
    #                   returns tuple of target ID, and it's symbol clock frequency
    @classmethod
    def get_max_ddi_symbol_clock_frequency(cls, gfx_index: str, ports: List[str]) -> Tuple[str, float]:
        # Store link rates per panel connected to port for comparison
        symbol_frequencies: Dict[str, float] = dict()

        for port_name in ports:
            port_ddi = cls.ddi_to_bspec_name_map[port_name[-1].upper()]
            offset = eval(
                'Gen15NonAutoGenRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_' + port_ddi.replace('USBC', 'USB'))
            value = DisplayArgs.read_register(offset, gfx_index)
            ddi_clk_valfreq = Gen15NonAutoGenRegs.REG_DDI_CLK_VALFREQ(offset, value)
            logging.info(f'DDI Clk ValFreq = 0x{ddi_clk_valfreq.value:X}')
            logging.info(f"ddi_clk_valfreq_value = {ddi_clk_valfreq.DdiValidationFrequency}")

            valfreq = ddi_clk_valfreq.DdiValidationFrequency / 1000  # KHz to MHz
            logging.info(f"DDI CLK ValFreq for {port_name} = {valfreq} MHz")
            symbol_frequencies[port_name] = valfreq

        logging.info(f"Symbol frequencies - {symbol_frequencies}")
        max_ddi_freq = max(symbol_frequencies.values())
        return list(symbol_frequencies.keys())[list(symbol_frequencies.values()).index(max_ddi_freq)], max_ddi_freq
