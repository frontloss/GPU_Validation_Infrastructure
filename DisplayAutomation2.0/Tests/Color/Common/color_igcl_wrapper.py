#######################################################################################################################
# @file                 color_igcl_wrapper.py
# @brief                The wrapper helps in encapsulating the details of the  arguments required by the IGCL Escapes
# @author               Smitha B
#######################################################################################################################
import ctypes
import logging
from enum import Enum
from Libs.Core.wrapper import control_api_args
from Tests.Color.Common import hdr_utility, color_enums


class IgclColorBlocks(Enum):
    HW3DLUT = 0
    DGLUT = 1
    CSC = 2
    GLUT = 3
    OCSC = 4
    DGLUT_CSC = 5
    DGLUT_CSC_GLUT = 6
    CSC_GLUT = 7
    DGLUT_GLUT = 8
    ALL = 9
    ERROR = 99


def prepare_igcl_args_for_power_caps():
    get_power_caps = control_api_args.ctl_power_optimization_caps_t()
    get_power_caps.Size = ctypes.sizeof(get_power_caps)
    return get_power_caps


def prepare_igcl_args_for_get_power_ftr(pwr_ftr):
    get_pwr_ftr = control_api_args.ctl_power_optimization_settings_t()
    get_pwr_ftr.Size = ctypes.sizeof(get_pwr_ftr)
    get_pwr_ftr.PowerOptimizationFeature = pwr_ftr
    return get_pwr_ftr


def prepare_igcl_args_for_set_power_ftr():
    get_pwr_ftr = control_api_args.ctl_power_optimization_settings_t()
    get_pwr_ftr.Size = ctypes.sizeof(get_pwr_ftr)
    return get_pwr_ftr


def prepare_igcl_set_args_for_elp(user_level, enable_status):
    set_power_settings = prepare_igcl_args_for_get_power_ftr(control_api_args.ctl_power_optimization_flags_v.DPST.value)
    set_power_settings.Enable = enable_status
    set_power_settings.FeatureSpecificData.DPSTInfo.EnabledFeatures = 8
    set_power_settings.FeatureSpecificData.DPSTInfo.Level = user_level
    set_power_settings.PowerSource = control_api_args.ctl_power_source_v.DC.value
    set_power_settings.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value

    return set_power_settings


def prepare_igcl_get_args_for_elp():
    get_power_settings = prepare_igcl_args_for_get_power_ftr(control_api_args.ctl_power_optimization_flags_v.DPST.value)
    get_power_settings.PowerSource = control_api_args.ctl_power_source_v.DC.value
    get_power_settings.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value

    return get_power_settings

def prepare_igcl_set_args_for_3dlut(igcl_get_caps, hw_3dlut_index):
    argsLutConfig = control_api_args.ctl_pixtx_block_config_t()
    argsLutConfig.Size = ctypes.sizeof(argsLutConfig)
    argsLutConfig.BlockType = control_api_args.ctl_pixtx_block_type_v._3D_LUT.value
    argsLutConfig.Config = igcl_get_caps.pBlockConfigs[hw_3dlut_index].Config
    return argsLutConfig


##
# @brief        Prepares the IGCL Arguments to perform a GET Config Call
# @return       igcl_esc_args, color_blk_args
def prepare_igcl_color_esc_args_for_get_config():
    ##
    # Preparing the generic arguments for the escape call
    igcl_esc_args = control_api_args.ctl_pixtx_pipe_get_config_t()
    igcl_esc_args.Size = ctypes.sizeof(igcl_esc_args)
    igcl_esc_args.QueryType = control_api_args.ctl_pixtx_config_query_type_v.CURRENT.value

    # # Preparing the block specific arguments for the escape call which returns info about blocks such as (DGLUT,
    # CSC, GLUT, HW3DLUT, oCSC)
    color_blk_args = control_api_args.ctl_pixtx_block_config_t()
    color_blk_args.Size = ctypes.sizeof(color_blk_args)

    return igcl_esc_args, color_blk_args


##
# @brief        Prepares the IGCL Arguments to perform a GET Capability Call
# @return       igcl_esc_args, color_blk_args
def prepare_igcl_color_esc_args_for_get_caps():
    ##
    # Perform a get capabilities call for the specific Display
    igcl_args_get_caps = control_api_args.ctl_pixtx_pipe_get_config_t()
    igcl_args_get_caps.Size = ctypes.sizeof(igcl_args_get_caps)
    igcl_args_get_caps.QueryType = control_api_args.ctl_pixtx_config_query_type_v.CAPABILITY.value
    return igcl_args_get_caps


##
# @brief        Helps in identifying the Block ID of the Color blocks
# @param[in]    igcl_get_caps  The Capabilities supported based on the mode
# @param[in]    color_blk_index  A dictionary of all the blocks where
#               BlockName would be the Key and BlockID would be the Value updated by the function
# @param[in]    port_type  Details of the display
# @param[in]    pipe  Details of the pipe attached to the display
# @param[in]    gfx_index  Details of the graphics adapter
# @param[in]    platform  Platform details
def fetch_cc_blk_index(igcl_get_caps, color_blk_index, port_type, pipe, gfx_index, platform):

    for index in range(0, igcl_get_caps.NumBlocks):
        ##
        # HW3DLUT
        if igcl_get_caps.pBlockConfigs[index].BlockType.value == \
                control_api_args.ctl_pixtx_block_type_v._3D_LUT.value:
            logging.debug(
                "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} connected to Pipe {3} on adapter {4}"
                    .format(control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.name, index,
                            port_type, pipe, gfx_index))
            color_blk_index['3DLUT'] = index

        ##
        # _3X3_MATRIX_AND_OFFSETS - Linear CSC
        if igcl_get_caps.pBlockConfigs[index].BlockType.value == \
                control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.value:
            logging.debug(
                "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} connected to Pipe {3} on adapter {4}"
                    .format(control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.name, index,
                            port_type, pipe, gfx_index))
            color_blk_index['CSC'] = index

        ##
        # OneDLUT
        # For both DGLUT and GLUT Blocks, the BlockType would be _1D_LUT;
        # Hence trying to identify the block based on the number of channels and SDR\HDR Mode
        if igcl_get_caps.pBlockConfigs[index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._1D_LUT.value:
            ##
            # Verification when both DGLUT and GLUT are expected to be enabled
            if igcl_get_caps.pBlockConfigs[index].Config.OneDLutConfig.NumChannels == 1:
                color_blk_index['DGLUT'] = index

                enabled_mode = hdr_utility.fetch_enabled_mode(gfx_index, platform, pipe)
                if enabled_mode == color_enums.ColorMode.HDR or enabled_mode == color_enums.ColorMode.WCG:
                    logging.error("DGLUT Block support has been reported in {0} Mode". format(enabled_mode))
                    return False

                logging.info(
                    "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} "
                    "connected to Pipe {3} on adapter {4} "
                        .format(control_api_args.ctl_pixtx_block_type_v._1D_LUT.name, index,
                                port_type, pipe, gfx_index))
            else:
                logging.info(
                    "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} connected to Pipe {3} on adapter {4}"
                        .format(control_api_args.ctl_pixtx_block_type_v._1D_LUT.name, index,
                                port_type, pipe, gfx_index))
                color_blk_index['GLUT'] = index

        ##
        # oCSC - NonLinear CSC
        if igcl_get_caps.pBlockConfigs[
            index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX.value:
            logging.debug(
                "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} connected to "
                "Pipe {3} on adapter {4} "
                    .format(control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.name, index,
                            port_type, pipe, gfx_index))
            color_blk_index['oCSC'] = index

def fill_3dlut_data_into_igcl_struct_format(igcl_get_caps, hw_3dlut_index, lut_type):
    output_sample_values = (control_api_args.ctl_pixtx_3dlut_sample_t*4913)()
    ctypes.cast(output_sample_values, ctypes.POINTER(control_api_args.ctl_pixtx_3dlut_sample_t))
    hw_3dlut_data=[]
    red_lut = []
    green_lut = []
    blue_lut = []
    lut_depth = int(igcl_get_caps.pBlockConfigs[hw_3dlut_index].Config.ThreeDLutConfig.NumSamplesPerChannel)

    for i in range(0, lut_depth):
        hw_3dlut_data.append(ctypes.c_double(i / (lut_depth - 1)))

    for index in range(0, lut_depth):
        if lut_type == "NO_RED":
            red_lut.append(0.0)
        else:
            red_lut.append(hw_3dlut_data[index])
    for index in range(0, lut_depth):
        if lut_type == "NO_GREEN":
            green_lut.append(0.0)
        else:
            green_lut.append(hw_3dlut_data[index])
    for index in range(0, lut_depth):
        if lut_type == "NO_BLUE":
            blue_lut.append(0.0)
        else:
            blue_lut.append(hw_3dlut_data[index])

    igcl_get_caps.pBlockConfigs[hw_3dlut_index].Config.ThreeDLutConfig.pSampleValues = output_sample_values
    index=0
    for r_index in range(0, lut_depth):
        for g_index in range(0, lut_depth):
            for b_index in range(0, lut_depth):
                igcl_get_caps.pBlockConfigs[hw_3dlut_index].Config.ThreeDLutConfig.pSampleValues[index].Red = red_lut[r_index]
                igcl_get_caps.pBlockConfigs[hw_3dlut_index].Config.ThreeDLutConfig.pSampleValues[index].Green = green_lut[g_index]
                igcl_get_caps.pBlockConfigs[hw_3dlut_index].Config.ThreeDLutConfig.pSampleValues[index].Blue = blue_lut[b_index]
                index=index+1

def fill_dglut_data_into_igcl_struct_format(igcl_get_caps, dglut_list, dglut_index):
    output_sample_values = (ctypes.c_double * len(dglut_list))()
    ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

    for ind in range(0, dglut_list.__len__()):
        output_sample_values[ind] = dglut_list[ind]
    igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

    for index in range(0, len(dglut_list)):
        output_sample_values[index] = dglut_list[index]
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues[index] \
            = output_sample_values[index]


def fill_csc_data_into_igcl_struct_format(igcl_get_caps, csc_matrix, csc_index):
    for row in range(0, 3):
        for col in range(0, 3):
            igcl_get_caps.pBlockConfigs[csc_index].Config.MatrixConfig.Matrix[row][col] = csc_matrix[row][col]


def fill_glut_data_into_igcl_struct_format(igcl_get_caps, glut_list, glut_index):
    output_sample_values = (ctypes.c_double * len(glut_list))()
    ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

    for ind in range(0, glut_list.__len__()):
        output_sample_values[ind] = glut_list[ind]

    # for ind in range(0, glut_list.__len__()):
    #     output_sample_values[ind] = glut_list[ind]
    igcl_get_caps.pBlockConfigs[glut_index].Config.OneDLutConfig.pSampleValues = output_sample_values


##
# @brief        Helps in identifying the Block ID of the Color blocks
# @param[in]    gfx_index  Details of the graphics adapter
# @param[in]    platform  Platform details
# @param[in]    port_type  Details of the display
# @param[in]    pipe  Details of the pipe attached to the display
# @param[in]    igcl_get_caps  The Capabilities supported based on the mode
# @param[in]    user_block_type  The BlockType to be enabled based on the cmd line args
# @param[in]    num_of_blks_to_be_set  Number of blocks to be enabled based on the cmd line args
# @param[in]    color_blk_dict  A dictionary where the BlockType would be the Key and the Data parsed
#                               from the JSON files based on the cmd args are the Value.
# @param[in]    color_blk_index  A dictionary of all the blocks where
#               BlockName would be the Key and BlockID would be the Value updated by the function
def prepare_igcl_color_escapes_args_for_set(gfx_index, platform, port_type, pipe, igcl_get_caps, user_block_type,
                                            num_of_blks_to_be_set, color_blk_dict, color_blk_index):

    ##
    # Preparing the generic arguments for the escape call
    igcl_esc_args = control_api_args.ctl_pixtx_pipe_set_config_t()
    igcl_esc_args.Size = ctypes.sizeof(igcl_esc_args)
    igcl_esc_args.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.SET_CUSTOM.value
    igcl_esc_args.NumBlocks = num_of_blks_to_be_set
    fetch_cc_blk_index(igcl_get_caps, color_blk_index, port_type, pipe, gfx_index, platform)

    if user_block_type == IgclColorBlocks.HW3DLUT.value:
        hw3dlut_blk_lut_type = str(color_blk_dict['3DLUT'])
        hw3dlut_blk_index = color_blk_index['3DLUT']
        fill_3dlut_data_into_igcl_struct_format(igcl_get_caps, hw3dlut_blk_index, str(hw3dlut_blk_lut_type))

    dglut_list = color_blk_dict['DGLUT']
    dglut_index = color_blk_index['DGLUT']
    if user_block_type == IgclColorBlocks.DGLUT.value:
        fill_dglut_data_into_igcl_struct_format(igcl_get_caps, dglut_list, dglut_index)

    csc_matrix = color_blk_dict['CSC']
    csc_index = color_blk_index['CSC']
    if user_block_type == IgclColorBlocks.CSC.value:
        fill_csc_data_into_igcl_struct_format(igcl_get_caps, csc_matrix, csc_index)

    if user_block_type == IgclColorBlocks.DGLUT_CSC.value:
        fill_dglut_data_into_igcl_struct_format(igcl_get_caps, dglut_list, dglut_index)
        fill_csc_data_into_igcl_struct_format(igcl_get_caps, csc_matrix, csc_index)

    if user_block_type == IgclColorBlocks.DGLUT_GLUT.value:
        dglut_list = color_blk_dict['DGLUT']
        dglut_index = color_blk_index['DGLUT']

        glut_list = color_blk_dict['GLUT']
        glut_index = color_blk_index['GLUT']

        fill_dglut_data_into_igcl_struct_format(igcl_get_caps, dglut_list, dglut_index)
        fill_glut_data_into_igcl_struct_format(igcl_get_caps, glut_list, glut_index)

    if user_block_type == IgclColorBlocks.DGLUT_CSC_GLUT.value:
        ##
        # DGLUT
        dglut_list = color_blk_dict['DGLUT']
        dglut_index = color_blk_index['DGLUT']
        ##
        # CSC
        csc_matrix = color_blk_dict['CSC']
        csc_index = color_blk_index['CSC']
        ##
        # GLUT
        glut_list = color_blk_dict['GLUT']
        glut_index = color_blk_index['GLUT']

        fill_dglut_data_into_igcl_struct_format(igcl_get_caps, dglut_list, dglut_index)
        fill_csc_data_into_igcl_struct_format(igcl_get_caps, csc_matrix, csc_index)
        fill_glut_data_into_igcl_struct_format(igcl_get_caps, glut_list, glut_index)

    if user_block_type == IgclColorBlocks.GLUT.value:
        glut_list = color_blk_dict['GLUT']
        glut_index = color_blk_index['GLUT']
        fill_glut_data_into_igcl_struct_format(igcl_get_caps, glut_list, glut_index)

    if user_block_type == IgclColorBlocks.OCSC.value:
        ocsc_matrix = color_blk_dict['oCSC']
        ocsc_index = color_blk_index['oCSC']
        fill_csc_data_into_igcl_struct_format(igcl_get_caps, ocsc_matrix, ocsc_index)

    return igcl_esc_args


def prepare_igcl_color_esc_args_for_restore_default():
    igcl_esc_restore_default = control_api_args.ctl_pixtx_pipe_set_config_t()
    igcl_esc_restore_default.Size = ctypes.sizeof(igcl_esc_restore_default)
    igcl_esc_restore_default.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.RESTORE_DEFAULT.value

    return igcl_esc_restore_default