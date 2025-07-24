import ctypes
import logging
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Tests.Color.Common import color_igcl_wrapper, color_igcl_escapes
from Tests.Color.Verification import feature_basic_verify


def select_reference_matrix_for_csc_block(self):
    logging.info("Matrix Info is {0}".format(self.csc))
    if self.csc in 'NONE':
        self.matrix_info = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def fetch_igcl_color_ftrs_caps_and_verify(gfx_index, platform, connector_port_type, pipe, display_and_adapter_info,
                                          requested_color_blk):
    igcl_args_get_caps = color_igcl_wrapper.prepare_igcl_color_esc_args_for_get_caps()
    if color_igcl_escapes.get_color_capability(igcl_args_get_caps, display_and_adapter_info) is False:
        return False
    logging.debug(" Input Pixel Format BitsPerColor - {}".format(igcl_args_get_caps.InputPixelFormat.BitsPerColor))
    logging.debug(" Input Pixel Format EncodingType - {}".format(igcl_args_get_caps.InputPixelFormat.EncodingType))
    logging.debug(" Input Pixel Format ColorSpace   - {}".format(igcl_args_get_caps.InputPixelFormat.ColorSpace))
    logging.debug(" Input Pixel Format ColorModel   - {}".format(igcl_args_get_caps.InputPixelFormat.ColorModel))
    logging.debug(" Ouput Pixel Format BitsPerColor - {}".format(igcl_args_get_caps.OutputPixelFormat.BitsPerColor))
    logging.debug(" Ouput Pixel Format EncodingType - {}".format(igcl_args_get_caps.OutputPixelFormat.EncodingType))
    logging.debug(" Ouput Pixel Format ColorSpace   - {}".format(igcl_args_get_caps.OutputPixelFormat.ColorSpace))
    logging.debug(" Ouput Pixel Format ColorModel   - {}".format(igcl_args_get_caps.OutputPixelFormat.ColorModel))
    hw3dlut_status, dglut_status, csc_status, glut_status, ocsc_status = False, False, False, False, False

    if feature_basic_verify.hdr_status(gfx_index, platform, pipe) and igcl_args_get_caps.NumBlocks == 5:
        logging.error("Reporting support for 5 Blocks in HDR Mode")
        return False, igcl_args_get_caps

    ##
    # Iterate through the blocks and verify if the requested blocks have been enabled
    logging.info("Total Number of Blocks {0}".format(igcl_args_get_caps.NumBlocks))
    for index in range(0, igcl_args_get_caps.NumBlocks):
        ##
        # HW3DLUT
        if igcl_args_get_caps.pBlockConfigs[index].BlockType.value == \
                control_api_args.ctl_pixtx_block_type_v._3D_LUT.value:
            logging.info(
                "PASS : IGCL Support for {0} has been reported by the driver on {1} connected to Pipe {2} on "
                "adapter {3} ".format(control_api_args.ctl_pixtx_block_type_v._3D_LUT.name, connector_port_type,
                                      pipe, gfx_index))

            hw3dlut_status = True

        ##
        # _3X3_MATRIX_AND_OFFSETS - Linear CSC
        if igcl_args_get_caps.pBlockConfigs[
            index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.value:
            logging.info(
                "PASS : IGCL Support for {0} has been reported by the driver on {1} connected to Pipe {2} on adapter {3}"
                    .format(control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.name,
                            connector_port_type, pipe, gfx_index))
            csc_status = True

        ##
        # OneDLUT
        if igcl_args_get_caps.pBlockConfigs[
            index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._1D_LUT.value:
            logging.info(
                "PASS : IGCL Support for {0} has been reported by the driver on {1} connected to Pipe {2} on "
                "adapter {3} "
                    .format(control_api_args.ctl_pixtx_block_type_v._1D_LUT.name, connector_port_type, pipe,
                            gfx_index))

            logging.info("Number of Channels is {0}".format(
                igcl_args_get_caps.pBlockConfigs[index].Config.OneDLutConfig.NumChannels))

            ##
            # Verification when both DGLUT and GLUT are expected to be enabled
            if igcl_args_get_caps.pBlockConfigs[index].Config.OneDLutConfig.NumChannels == 1:
                dglut_status = True
                logging.info("DGLUT Index is {0} and BlockType is {1}".format(index,
                                                                              igcl_args_get_caps.pBlockConfigs[
                                                                                  index].BlockType.value))

            else:
                logging.info("GLUT Index is {0} and BlockType is {1}".format(index,
                                                                             igcl_args_get_caps.pBlockConfigs[
                                                                                 index].BlockType.value))
                glut_status = True

        ##
        # oCSC - NonLinear CSC
        if igcl_args_get_caps.pBlockConfigs[
            index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX.value:
            logging.info(
                "PASS : IGCL Support for {0} has been reported by the driver on {1} connected to Pipe {2} on "
                "adapter {3} "
                    .format(control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX.name, connector_port_type, pipe,
                            gfx_index))
            ocsc_status = True

    if feature_basic_verify.hdr_status(gfx_index, platform, pipe):
        if hw3dlut_status is True or dglut_status is True:
            return False, igcl_args_get_caps

    logging.info(
        "All Status HW3DLUT_Status : {0} DGLUT_Status : {1} CSC_Status :{2} GLUT_Status {3} oCSC Status {4}".format(
            hw3dlut_status, dglut_status, csc_status, glut_status, ocsc_status))
    logging.info("Requested Color Block is {0}".format(requested_color_blk))
    ##
    # Based on the command line parameters, checking if the specific blocks are enabled by the driver
    # HW3DLUT
    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.HW3DLUT.value and hw3dlut_status is True:
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.DGLUT.value and dglut_status is True:
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.CSC.value and csc_status is True:
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.GLUT.value and glut_status is True:
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.DGLUT_CSC.value and (
            dglut_status is True and csc_status is True):
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.DGLUT_CSC_GLUT.value and (
            dglut_status is True and csc_status is True and glut_status is True):
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.DGLUT_GLUT.value and (
            dglut_status is True and glut_status is True):
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.ALL.value and (
            dglut_status is True and csc_status is True and glut_status is True and hw3dlut_status is True and ocsc_status is True):
        return True, igcl_args_get_caps

    if requested_color_blk == color_igcl_wrapper.IgclColorBlocks.OCSC.value and ocsc_status is True:
        return True, igcl_args_get_caps

    return False, igcl_args_get_caps


def fetch_blk_index(igcl_get_caps, color_blk_index, port_type, pipe, gfx_index, platform):
    ##
    # Preparing the block(DGLUT, CSC, GLUT, HW3DLUT, oCSC) specific arguments for the escape call
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
        if igcl_get_caps.pBlockConfigs[index].BlockType.value == control_api_args.ctl_pixtx_block_type_v._1D_LUT.value:
            ##
            # Verification when both DGLUT and GLUT are expected to be enabled
            if igcl_get_caps.pBlockConfigs[index].Config.OneDLutConfig.NumChannels == 1:
                color_blk_index['DGLUT'] = index

                ##
                # Verifying if DGLUT is enabled in HDR Mode
                if feature_basic_verify.hdr_status(gfx_index, platform, pipe):
                    return False
                logging.info(
                    "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} connected to Pipe {3} on adapter {4}"
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
                "PASS : IGCL Support for {0} with Block Index {1} has been reported by the driver on {2} connected to Pipe {3} on adapter {4}"
                    .format(control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX_AND_OFFSETS.name, index,
                            port_type, pipe, gfx_index))
            color_blk_index['oCSC'] = index


def prepare_igcl_color_escapes_args_for_set(gfx_index, platform, port_type, pipe, igcl_get_caps, user_block_type,
                                            num_of_blks_to_be_set, color_blk_dict, color_blk_index):
    dglut_list = []
    dglut_index = -1
    ##
    # Preparing the generic arguments for the escape call
    igcl_esc_args = control_api_args.ctl_pixtx_pipe_set_config_t()
    igcl_esc_args.Size = ctypes.sizeof(igcl_esc_args)
    igcl_esc_args.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.SET_CUSTOM.value
    igcl_esc_args.NumBlocks = num_of_blks_to_be_set

    fetch_blk_index(igcl_get_caps, color_blk_index, port_type, pipe, gfx_index, platform)
    if user_block_type == color_igcl_wrapper.IgclColorBlocks.HW3DLUT.value:
        pass

    ##
    # Common information to be updated for DGLUT
    if color_blk_dict['DGLUT'] is not None:
        dglut_list = color_blk_dict['DGLUT']
        dglut_index = color_blk_index['DGLUT']

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.DGLUT.value:
        output_sample_values = (ctypes.c_double * len(dglut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, dglut_list.__len__()):
            output_sample_values[ind] = dglut_list[ind]
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

        for index in range(0, len(dglut_list)):
            output_sample_values[index] = dglut_list[index]
            igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues[index] \
                = output_sample_values[index]

    csc_matrix = color_blk_dict['CSC']
    csc_index = color_blk_index['CSC']
    if user_block_type == color_igcl_wrapper.IgclColorBlocks.CSC.value:
        for row in range(0, 3):
            for col in range(0, 3):
                igcl_get_caps.pBlockConfigs[csc_index].Config.MatrixConfig.Matrix[row][col] = csc_matrix[row][col]

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.DGLUT_CSC.value:
        output_sample_values = (ctypes.c_double * len(dglut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, dglut_list.__len__()):
            output_sample_values[ind] = dglut_list[ind]
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values
        ##
        # DGLUT
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

        for index in range(0, len(dglut_list)):
            output_sample_values[index] = dglut_list[index]
            igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues[index] \
                = output_sample_values[index]

        ##
        # CSC
        for row in range(0, 3):
            for col in range(0, 3):
                igcl_get_caps.pBlockConfigs[csc_index].Config.MatrixConfig.Matrix[row][col] = csc_matrix[row][col]

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.DGLUT_GLUT.value:
        dglut_list = color_blk_dict['DGLUT']
        dglut_index = color_blk_index['DGLUT']

        output_sample_values = (ctypes.c_double * len(dglut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, dglut_list.__len__()):
            output_sample_values[ind] = dglut_list[ind]
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values
        ##
        # DGLUT
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

        for index in range(0, len(dglut_list)):
            output_sample_values[index] = dglut_list[index]
            igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues[index] \
                = output_sample_values[index]

        ##
        # GLUT
        glut_list = color_blk_dict['GLUT']
        glut_index = color_blk_index['GLUT']
        output_sample_values = (ctypes.c_double * len(glut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, glut_list.__len__()):
            output_sample_values[ind] = glut_list[ind]

        # for ind in range(0, glut_list.__len__()):
        #     output_sample_values[ind] = glut_list[ind]
        igcl_get_caps.pBlockConfigs[glut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.DGLUT_CSC_GLUT.value:
        dglut_list = color_blk_dict['DGLUT']
        dglut_index = color_blk_index['DGLUT']

        output_sample_values = (ctypes.c_double * len(dglut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, dglut_list.__len__()):
            output_sample_values[ind] = dglut_list[ind]
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values
        ##
        # DGLUT
        igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

        for index in range(0, len(dglut_list)):
            output_sample_values[index] = dglut_list[index]
            igcl_get_caps.pBlockConfigs[dglut_index].Config.OneDLutConfig.pSampleValues[index] \
                = output_sample_values[index]

        ##
        # GLUT
        glut_list = color_blk_dict['GLUT']
        glut_index = color_blk_index['GLUT']
        output_sample_values = (ctypes.c_double * len(glut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, glut_list.__len__()):
            output_sample_values[ind] = glut_list[ind]

        # for ind in range(0, glut_list.__len__()):
        #     output_sample_values[ind] = glut_list[ind]
        igcl_get_caps.pBlockConfigs[glut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

        csc_matrix = color_blk_dict['CSC']
        csc_index = color_blk_index['CSC']

        ##
        # CSC
        for row in range(0, 3):
            for col in range(0, 3):
                igcl_get_caps.pBlockConfigs[csc_index].Config.MatrixConfig.Matrix[row][col] = csc_matrix[row][col]

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.GLUT.value:
        glut_list = color_blk_dict['GLUT']
        glut_index = color_blk_index['GLUT']

        logging.info("GLUT Index is {0}".format(glut_index))

        output_sample_values = (ctypes.c_double * len(glut_list))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, glut_list.__len__()):
            output_sample_values[ind] = glut_list[ind]

        # for ind in range(0, glut_list.__len__()):
        #     output_sample_values[ind] = glut_list[ind]
        igcl_get_caps.pBlockConfigs[glut_index].Config.OneDLutConfig.pSampleValues = output_sample_values

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.OCSC.value:
        ocsc_matrix = color_blk_dict['oCSC']
        ocsc_index = color_blk_index['oCSC']
        for row in range(0, 3):
            for col in range(0, 3):
                igcl_get_caps.pBlockConfigs[ocsc_index].Config.MatrixConfig.Matrix[row][col] = ocsc_matrix[row][col]

    if user_block_type == color_igcl_wrapper.IgclColorBlocks.HW3DLUT.value:
        logging.info("For HW3DLUT")
        hw3dlut_data = color_blk_dict['3DLUT']
        hw3dlut_index = color_blk_index['3DLUT']
        output_sample_values = (ctypes.c_double * len(hw3dlut_data))()
        ctypes.cast(output_sample_values, ctypes.POINTER(ctypes.c_double))

        for ind in range(0, hw3dlut_data.__len__()):
            output_sample_values[ind] = hw3dlut_data[ind]

        for ind in range(0, hw3dlut_data.__len__()):
            output_sample_values[ind] = hw3dlut_data[ind]

        j = 0
        logging.info("HW3DLUT index is {0}".format(hw3dlut_index))
        input('Enter')
        for r_index in range(0, 17):
            for g_index in range(0, 17):
                for b_index in range(0, 17):
                    igcl_get_caps.pBlockConfigs[hw3dlut_index].Config.ThreeDLutConfig.pSampleValues[
                        j].Red = 0.0  # output_sample_values[r_index]
                    igcl_get_caps.pBlockConfigs[hw3dlut_index].Config.ThreeDLutConfig.pSampleValues[
                        j].Blue = 1.0  # output_sample_values[g_index]
                    igcl_get_caps.pBlockConfigs[hw3dlut_index].Config.ThreeDLutConfig.pSampleValues[
                        j].Green = 2.0  # output_sample_values[b_index]
                    j += 1

        for index in range(0, 3):
            logging.info(igcl_get_caps.pBlockConfigs[hw3dlut_index].Config.OneDLutConfig.pSampleValues[index].Red)
            logging.info(igcl_get_caps.pBlockConfigs[hw3dlut_index].Config.OneDLutConfig.pSampleValues[index].Blue)
            logging.info(igcl_get_caps.pBlockConfigs[hw3dlut_index].Config.OneDLutConfig.pSampleValues[index].Green)

    return igcl_esc_args