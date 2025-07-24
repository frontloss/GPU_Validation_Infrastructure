######################################################################################
# @file
# @brief This test fetches the EDID, DPCD and Scalar mode that has to be applied from the XML file passed as input.
# @details Apply scalar mode specified, verify if Pipe scalar is enabled and scalar plane size and position programmed correctly based on scaling option (CI,FS,MAR),
#          Verify Clock, Plane, Pipe, Transcoder, DDI programming
# Command line : python Tests\Scalar\scalar_verication.py -[hdmi_*/dp_*] -dispconfig [single/dual] -xml [XML file]
# @author  Aafiya Kaleem
######################################################################################
import logging
import sys
import unittest
from xml.etree import ElementTree as ET

from Libs.Core import display_utility
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine.de_base.display_scalar import DisplayScalar, VerifyScalarProgramming
from Libs.Feature.display_engine.de_base.display_pipe import DisplayPipe
from Libs.Feature.display_engine.de_base.display_plane import DisplayPlane
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.vdsc import dsc_verifier
from Libs.Core.logger import gdhm
from Tests.Scalar.scalar_base import ScalarBase


##
# @brief This class has the test implementation for Upscale verification of Pipe Scalar Feature
class Scalar(ScalarBase):

    ##
    # @brief        Scalar verification runTest function. Apply each scalar mode from input xml and verify DE
    # @details      verify if Pipe scalar is enabled along with scalar plane size and scalar position,
    #               verify Clock, Plane, Pipe, Transcoder, DDI programming
    # @return       None
    def scalar_mode_and_verify(self):
        fail_flag = False
        enumerated_displays = self.display_config.get_enumerated_display_info()

        for scalarkey, scalarvalue in self.scalar_config_dict.items():
            for scalar in range(0, len(scalarvalue)):
                supported_mode_list = self.display_config.get_all_supported_modes([scalarvalue[scalar].targetId],
                                                                                  False)
                for supported_key, supported_value in supported_mode_list.items():
                    for sup in range(0, len(supported_value)):
                        logging.debug(
                            "OS Supported Modes - TargetID : %s - " % (supported_value[sup].targetId) +
                            supported_value[
                                sup].to_string(enumerated_displays))
                        if (self.compare_modes(scalarvalue[scalar], supported_value[sup])):
                            logging.info("PASS : Scalar Mode is Supported - TargetID : %s - "
                                         % (scalarvalue[scalar].targetId) + scalarvalue[scalar].to_string(
                                enumerated_displays))
                            # apply the user requested mode
                            # To Force PLANE Scalar set "virtual_mode_set_aware" parameter as True (Default).
                            # To Force PIPE Scalar set "virtual_mode_set_aware" parameter as False.
                            status = self.display_config.set_display_mode(mode_list=[scalarvalue[scalar]],
                                                                          virtual_mode_set_aware=False,
                                                                          enumerated_displays=None)
                            if status is False:
                                logging.error("ERROR : Failed to apply display mode. Exiting ...")
                                fail_flag = True
                            else:
                                logging.info("INFO : Requested Mode is successfully applied")
                                # Verify scalar programming
                                scaling = self.rscale_dict[scalarvalue[scalar].scaling]
                                gfx_index = supported_value[sup].displayAndAdapterInfo.adapterInfo.gfxIndex

                                plane_list, pipe_list, scalar_list = self.get_pipe_plane_scalar_lists(scalarkey, scaling, gfx_index)
                                                                                                                                   
                                test_pass = VerifyScalarProgramming(scalar_list)
                                if (test_pass is False):
                                    fail_flag = True

                                # Test whether clock, plane, pipe, transcoder, DDI are programmed correctly in case of DSC and non DSC Panel
                                ports = []
                                ports.append(scalarkey)
                                display = DisplayEngine()
                                test_pass = display.verify_display_engine(ports, plane_list, pipe_list)
                                if test_pass is False:
                                    fail_flag = True
                                if 'TRUE' in self.cmd_line_param['DSC']:
                                    test_pass = dsc_verifier.verify_dsc_programming(gfx_index, port=scalarkey)
                                    self.assertTrue(test_pass,
                                        "FAIL : scalar_mode_and_verify - Incorrect DSC Programming for dsc display plugged at %s" % str(scalarkey))
                                    if test_pass is False:
                                        fail_flag = True
                            break
                        else:
                            if (sup == len(supported_value) - 1):
                                logging.error("FAIL : Scalar Mode is not supported - TargetID : %s - "
                                              % (scalarvalue[scalar].targetId) + scalarvalue[scalar].to_string(
                                    enumerated_displays))
                                gdhm.report_bug(
                                    title="[Display_Interfaces][Scalar] Unsupported Scalar Mode-[{}:{}:{}:{}] for the Target {}".
                                        format(scalarvalue[scalar].HzRes, scalarvalue[scalar].VtRes,
                                               scalarvalue[scalar].refreshRate,
                                               scalarvalue[scalar].scaling, scalarvalue[scalar].targetId),
                                    problem_classification=gdhm.ProblemClassification.OTHER,
                                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                fail_flag = True

        if fail_flag is True:
            self.fail("FAIL : scalar_mode_and_verify")


    ##
    # @brief Creates Display objects lists to pass to DE Veirification
    # @param[in] display_port
    # @param[in] scaling_type Scaling mode MAR/CI/FS
    # @param[in] gfx_index
    # @return planeList pipeListscalarList
    def get_pipe_plane_scalar_lists(self, display_port, scaling_type, gfx_index):
        scalar_obj_list = []
        pipe_obj_list = []
        plane_obj_list = []
        scalar_obj_list.append(DisplayScalar(display_port, scaling_type, gfx_index=gfx_index))
        pipe_obj_list.append(DisplayPipe(display_port, gfx_index=gfx_index))
        plane_obj_list.append(DisplayPlane(display_port, gfx_index=gfx_index))
        is_pipe_joiner_req, num_pipes = DisplayClock.is_pipe_joiner_required(gfx_index, display_port)
        for i in range(1, num_pipes):                                    
            pipe_obj = DisplayPipe(display_port, gfx_index=gfx_index)
            adj_pipe = chr(ord(pipe_obj.pipe[-1]) + i)
            pipe_obj.pipe = "PIPE_" + adj_pipe
            pipe_obj.pipe_suffix = adj_pipe
            pipe_obj_list.append(pipe_obj)

            plane_obj = DisplayPlane(display_port, gfx_index=gfx_index)
            plane_obj.pipe = pipe_obj.pipe
            plane_obj.pipe_suffix = adj_pipe
            plane_obj_list.append(plane_obj)

            scalar_obj = DisplayScalar(display_port, scaling_type, gfx_index=gfx_index)
            scalar_obj.pipe = pipe_obj.pipe
            scalar_obj.pipe_suffix = adj_pipe
            scalar_obj_list.append(scalar_obj)     

        return plane_obj_list, pipe_obj_list, scalar_obj_list


    ##
    # @brief Unit-test runTest function. Apply scalar mode and verify scalar parameters
    # @return None
    def runTest(self):
        self.scalar_mode_and_verify()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
