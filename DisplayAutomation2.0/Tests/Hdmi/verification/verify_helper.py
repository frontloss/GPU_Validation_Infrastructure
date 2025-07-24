########################################################################################################################
# @file         verify_helper.py
# @brief        The module verify Register programming
# @details
#               <ul>
#               <li> ref:    verify_register_programming        	    \n copybrief verify_registers \n
#               </li>
#               </ul>
# @author       Girish Y D
########################################################################################################################

import logging


##
# @brief        Validate Feature
# @param[in]    current_value - current value of feature
# @param[in]    expected_value - expected value of feature
# @param[in]    feature - the feature to be validated
# @return       bool - status of verification
def validate_feature(current_value, expected_value, feature):
    if (current_value == expected_value):
        logging.info("PASS: {0}- Expected : {1} Actual : {2}".format(feature, str(expected_value), str(current_value)))
        return True
    else:
        logging.error("FAIL: {0}- Expected : {1} Actual : {2}".format(feature, str(expected_value), str(current_value)))
        return False


##
# @brief        Checks for the platform and calls the correct implementation
# @param[in]    test_parameters - Values from the test
# @param[in]    edid_parameters - Values from EDID
# @return       result - Register Programming result
def verify_register_programming(test_parameters, edid_parameters):
    result = True
    if test_parameters.platform.upper() in ['ICLHP', 'LKF1', 'TGL', 'DG1', 'RKL', 'DG2']:
        from Tests.Hdmi.verification.iclhp_lkf1_tgl import verify_register_programming as verify_registers
        verify_register_programming = verify_registers.VerifyRegisterProgramming(test_parameters,
                                                                                 edid_parameters)
        result &= verify_register_programming.verify_registers()
    elif test_parameters.platform.upper() in ['ICL', 'ICLLP', 'JSL']:
        if test_parameters.platform.upper() == 'JSL':
            test_parameters.platform = 'ICLLP'
        from Tests.Hdmi.verification.icl import icl_verify_register_programming as verify_registers
        icl_verify_register_programming = verify_registers.IclVerifyRegisterProgramming(test_parameters,
                                                                                        edid_parameters)
        result &= icl_verify_register_programming.verify_registers()
    elif test_parameters.platform.upper() == "CNL":
        from Tests.Hdmi.verification.cnl import cnl_verify_register_programming as verify_registers
        cnl_verify_register_programming = verify_registers.CnlVerifyRegisterProgramming(test_parameters,
                                                                                        edid_parameters)
        result &= cnl_verify_register_programming.verify_registers()
    elif test_parameters.platform.upper() == "GLK":
        from Tests.Hdmi.verification.glk import glk_verify_register_programming as verify_registers
        glk_verify_register_programming = verify_registers.GlkVerifyRegisterProgramming(test_parameters,
                                                                                        edid_parameters)
        result &= glk_verify_register_programming.verify_registers()
    else:
        logging.error("Verify registers for Platfrom %s is not IMPLEMENTED" % test_parameters.platform)
        result = False
    return result
