#######################################################################################################################
# @file         dp_ui_constants.py
# @brief        This file contains list of manual user events.
#
# @author       Praburaj Krishnan
#######################################################################################################################

##
# @brief    UI String Constants Class
class UIStringConstants:
    GENERAL_INSTRUCTION = ("1. Make sure all external displays are unplugged before proceeding.\n"
                           "2. Instructions will be provided as alert boxes.\n"
                           "3. Read the instructions carefully and then proceed further action.\n"
                           "4. Press 'OK' after performing the required action.\n"
                           "5. Choose or provide your result based on your observation after each action.\n"
                           "6. Gfx Valsim driver should not be installed.\n\n\n" +
                           "Press 'OK' to continue."
                           )
    GENERAL_FAILURE_MESSAGE = ("1.Failure occured. Check log for failure signature.\n"
                               "2.Press 'OK' to exit."
                               )
    BUILD_MST_TOPOLOGY_STEP_ONE = "Hot Plug {0} panel to {1} port[Depth 1]."
    BUILD_MST_TOPOLOGY_STEP_TWO = "Hot Plug {0} panel to the output port of the first DP MST panel[Depth 2]."
    BUILD_MST_TOPOLOGY_STEP_THREE = "Hot Plug {0} panel to the output port of the second DP MST panel[Depth 3]."
    PLUG_FAILURE = "Hot plug of {0} has failed. Do you want to try plugging {0} panel again"
    DISPLAY_ANOMALY = "Did you observe flickering or corruption or blankout?"
    HOT_PLUG_DISPLAY = "Hot plug {0} panel on port {1}."
    HOTPLUG_SUCCESS = "Hot plug of {0} panel on port {1} is successful."
    UNPLUG_DISPLAY = "Unplug the {0} panel from port {1}."
    UNPLUG_SUCCESS = "Unplug of {0} panel from port {1} is successful."
    CUI_AFTER_PLUG = "Is {0} panel got enumerated in CUI page after hotplug on port {1}?"
    CUI_AFTER_UNPLUG = "Is {0} panel got removed in CUI page after unplug on port {1}?"
    UNPLUG_ALL_DISPLAYS = "Unplug all external displays connected to the system."
