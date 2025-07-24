########################################################################################################################
# @file         display_genlock_base.py
# @brief        Base module for display genlock
# @author       diksonch
########################################################################################################################

import ctypes
import logging

from Tests.Matrox.matrox_base import MatroxBase
from Libs.Core.display_config import display_config
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from enum import IntEnum

##
# @brief        Exposed enum class for Genlock actions
class Action(IntEnum):
    VALIDATE = 0
    ENABLE = 1
    DISABLE = 2

##
# @brief - Genlock Base Class
class Genlock(MatroxBase):
    args = control_api_args.ctl_genlock_args_t()
    args.Size = ctypes.sizeof(args)
    args.Version = 0  # dummy value
    args.GenlockTopology.IsPrimaryGenlockSystem = True
    
    enable_flag = False
    possible_flag = False

    ##
    # @brief        API to perform genlock
    # @param[in]    gfx - Graphics adapter index string
    # @param[in]    port - eg DP_B , HDMI_B string
    # @param[in]    action - to be performed of type Action(IntEnum)
    # @param[in]    display_data - of type DisplayAndAdapterInfo
    # @return       None
    def perform_display_genlock(self, gfx, port, action, display_data=None):
        if display_data is None:
            display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(port=port, gfx_index=gfx)

        if action == Action.VALIDATE:
            Genlock.args.Operation = control_api_args.ctl_genlock_operation_v.VALIDATE
        
        elif action == Action.ENABLE:
            Genlock.args.Operation = control_api_args.ctl_genlock_operation_v.ENABLE
        
        elif action == Action.DISABLE:
            Genlock.args.Operation = control_api_args.ctl_genlock_operation_v.DISABLE
        
        status = control_api_wrapper.display_genlock(Genlock.args, display_and_adapter_info=display_data)
        
        if status:
            logging.info(f"PASS: Display Genlock called for action {action} on port {port}")
            return status
        else:
            logging.info(f"FAIL: Display Genlock called for action {action} on port {port}")
            return status

    ##
    # @brief        Check if genlock is possible, this is different from the genlock topology's is possible
    # @return       None
    def verify_validate_functionality(self):
        if Genlock.args.IsGenlockPossible:
            logging.info(f"IsGenlockPossible: {Genlock.args.IsGenlockPossible}")
            return True

        logging.error(f"IsGenlockPossible: {Genlock.args.IsGenlockPossible}")
        return False

    ##
    # @brief        Check if genlock is enabled, by default parameter always return False
    # @return       None
    def verify_enable_functionality(self):
        if Genlock.args.IsGenlockEnabled and Genlock.args.IsGenlockPossible:
            logging.info("Genlock enabled sucessfully")
            logging.info(f"IsGenlockEnabled: {Genlock.args.IsGenlockEnabled}")
            logging.info(f"IsGenlockPossible: {Genlock.args.IsGenlockPossible}")
            Genlock.enable_flag = Genlock.args.IsGenlockEnabled
            Genlock.possible_flag = Genlock.args.IsGenlockPossible
            return True

        logging.error("Genlock is not enabled or not possible")
        logging.error(f"IsGenlockEnabled: {Genlock.args.IsGenlockEnabled}")
        logging.error(f"IsGenlockEnabled: {Genlock.args.IsGenlockPossible}")
        return False
    ##
    # @brief        Check if genlock is disabled, by default parameter always return False
    # @return       None
    def verify_disable_functionality(self):
        if (Genlock.enable_flag ^ Genlock.args.IsGenlockEnabled) \
            and (Genlock.possible_flag ^ Genlock.args.IsGenlockPossible):
                logging.info("Genlock disabled")
                logging.info(f"IsGenlockEnabled: Has changed from {Genlock.enable_flag} to {Genlock.args.IsGenlockEnabled}")
                logging.info(f"IsGenlockPossible: Has changed from {Genlock.possible_flag} to {Genlock.args.IsGenlockPossible}")
                return True
        
        logging.error("Genlock remains unchanged")
        return False
        

