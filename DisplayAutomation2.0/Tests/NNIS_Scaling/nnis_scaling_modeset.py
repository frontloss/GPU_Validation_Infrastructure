##
# @file nnis_scaling_modeset.py
# @brief This test ensures Driver is programing properly when we enable NN/ IS scaling.
# @details  the script takes NN or IS scaling and Plane or Pipe scalar as input.
#           First take list of mode from xml and apply mode set with scaling option provided on command line.
#           Apply all mode set one after other and Verify NN/IS scaling enable and apply properly or not.
# @author Nainesh Doriwala

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.NNIS_Scaling.nnis_scaling_base import *


##
# @brief It contains methods to ensure driver is programing properly when we apply modeset with different scaling
class ModeSetNNISScaling(ScalingBase):
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
    # @brief Unit-test runTest function. Check scaling after applying different custom mode set.
    # @return - void
    def test_run(self):
        self.is_teardown_required = True
        # Apply NN/IS scaling based on input
        self.apply_nn_is_scaling(is_integer_scaling=self.is_integer_scaling)

        # Apply mode and verify scaling
        self.apply_mode_and_verify_scaling(config_dict=self.scalar_config_dict,
                                           virtual_mode_set_aware=self.virtual_mode_set_aware)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ModeSetNNISScaling'))
    TestEnvironment.cleanup(outcome)
