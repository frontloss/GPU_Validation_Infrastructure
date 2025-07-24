##
# @file nnis_scaling_disable_enable.py
# @brief The script verify NN/IS scaling register programming verification in case of disable/enable NN/IS scaling
# @details The script takes NN or IS scaling and Plane or Pipe scalar as input.
#          First take list of mode from xml and apply mode set with scaling option provided on command line.
#          Verify NN/IS scaling enable and apply properly or not.
#          Disable NN/IS Scaling and verified whether it is disabled or not, again
#          Apply a different mode set for next test case to work properly.
# @author Nainesh Doriwala

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.NNIS_Scaling.nnis_scaling_base import *


##
# @brief It contains methods to ensure driver is programing properly when we disable NN/ IS scaling
class NNISScalingDisableEnable(ScalingBase):
    edp = False
    skip_plane_scaler = False

    ##
    # @brief test_start add NNIS scaling registry and do system restart if request by OS
    # @return - None
    def test_setup(self):
        status, reboot_required = self.check_and_add_nnis_scaling_registry()
        if status:
            logging.info("NNISScaling registry updated and successfully restarted driver.")
        elif status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_run') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief Unit-test runTest function. Check scaling before and after disable
    # @return - None
    def test_run(self):
        self.is_teardown_required = True
        PLATFORM_NAME = SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName

        # Apply NN/IS scaling based on input
        self.apply_nn_is_scaling(is_integer_scaling=self.is_integer_scaling)

        # Apply mode and verify scaling
        for scalarkey, scalarvalue in self.scalar_config_dict.items():
            # apply the user requested mode
            # To Force PLANE Scalar set "virtual_mode_set_aware" parameter as True (Default).
            # To Force PIPE Scalar set "virtual_mode_set_aware" parameter as False.
            status = self.display_config.set_display_mode([scalarvalue[0]],
                                                          virtual_mode_set_aware=self.virtual_mode_set_aware,
                                                          enumerated_displays=None)
            if status is False:
                self.fail("Failed to apply display mode. Exiting ...")

            if self.virtual_mode_set_aware:
                status = self.verify_Intergerscaling_support(scalarvalue[0].targetId, [scalarvalue[0]])
                if status is True:
                    status = self.check_plane_scalar_status(scalarvalue[0].targetId, [scalarvalue[0]], 20)
                    if status is False:
                        logging.error("ERROR: Plane scalar is not enabled")
                        self.fail("Failed to enable Plane Scalar")
                else:
                    logging.warning("Integer scaling is not supported for this resolution")
                    return True
            # Verification started
            status = self.verify_nn_is_scaling(scalarvalue[0].targetId, [scalarvalue[0]])
            if status is False:
                logging.error("ERROR : Failed to verify scaling. Exiting..")
                self.fail("Failed to verify scaling. Exiting")

            self.nn_args.opCode = ScalingOperation.SET_NN_SCALING_STATE.value
            self.nn_args.NNScalingState = NNScalingState.NN_SCALING_DISABLE.value
            # disable NN/IS scaling options
            status, self.nn_args = driver_escape.get_set_nn_scaling(scalarvalue[0].targetId,
                                                                    self.nn_args)  # Disabling scaling
            if status is False:
                logging.error(f"Escape call failed : get_set_nn_scaling() for {scalarvalue[0].targetId}")
                gdhm.report_bug(
                    title="[NN/IS] Escape call failed : get_set_nn_scaling()",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
            else:
                if self.nn_args.NNScalingState == NNScalingState.NN_SCALING_DISABLE.value:
                    logging.info("NN/IS scaling Disabled")
                else:
                    gdhm.report_bug(
                        title="[NN/IS] Failed to Disable NN/IS scaling ",
                        problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Disable NN/IS scaling Failed")

            # applying different mode set
            status = self.display_config.set_display_mode([scalarvalue[len(scalarvalue) - 1]],
                                                          virtual_mode_set_aware=self.virtual_mode_set_aware,
                                                          enumerated_displays=None)

            # verification post disable NN/IS scaling
            status = self.VerifyFilterSelection('A', PLATFORM_NAME, is_prgm_mode_enable=False)
            if status is False:
                self.fail("Program mode is still enable")
            status = self.verify_nnscalingstate_registry(0)
            if status is False:
                gdhm.report_bug(
                    title="[NN/IS] Scaling not disable in registry NNScalingState",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("NN/IS scaling not Disabled in registry")
            break


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2). \
        run(reboot_helper.get_test_suite('NNISScalingDisableEnable'))
    TestEnvironment.cleanup(outcome)
