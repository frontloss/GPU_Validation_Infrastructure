########################################################################################################################
# @file         hw_reg_util.py
# @brief        This script contains function to get the register instance
# @author       Shetty,Anjali N
########################################################################################################################
import importlib
import logging

from Libs.Core.sw_sim import driver_interface

##
# @brief            To get register instance
# @param[in]        module_name; name of the register module
# @param[in]        reg_name; name of the register
# @return           instance
def get_register(module_name, reg_name):
    class_name = module_name
    module = importlib.import_module("Tests.MPO.%s" % (module_name))
    class_ = getattr(module, class_name)
    regOffset_ = getattr(module, reg_name)

    reg_val = driver_interface.DriverInterface().mmio_read(regOffset_, 'gfx_0')

    instance = class_()
    instance.asUint = reg_val
    instance.__setattr__('offset', regOffset_)
    return instance


if __name__ == "__main__":
    transa_reg = get_register("TRANS_CONF_REGISTER", "TRANS_CONF_A")
    logging.info((transa_reg))
