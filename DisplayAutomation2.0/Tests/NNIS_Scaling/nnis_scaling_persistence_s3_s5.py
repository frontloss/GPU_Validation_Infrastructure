##
# @file nnis_scaling_persistence_s3_s5.py
# @brief The script takes input and based on the input applies NN/IS Scaling, mode and verifies scaling.
#        Verify Scaling persistence on S3 and S5 power event.
# @author Nainesh Doriwala


from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.NNIS_Scaling.nnis_scaling_base import *


##
# @brief It contains methods to ensure driver is programing properly post for power event S3 and S5.
class NNISScalingPersistenceS3S5(ScalingBase):
    skip_plane_scaler = False

    ##
    # @brief test_step_1 add NNIS scaling registry and do system restart if request by OS
    # @return - None
    def test_step_1(self):
        status, reboot_required = self.check_and_add_nnis_scaling_registry()
        if status:
            logging.info("NNISScaling registry updated and successfully restarted driver.")
        elif status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_step_2') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief step-2 apply mode verify scaling before and after S3 power event.
    # @return - None
    def test_step_2(self):
        logging.debug("Entry: test_step_2()")

        # Apply NN/IS scaling based on input
        self.apply_nn_is_scaling(is_integer_scaling=self.is_integer_scaling)

        # Apply mode and verify scaling
        for scalarkey, scalarvalue in self.scalar_config_dict.items():
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
                        self.fail("Failed to enable plane scalar")
                else:
                    logging.warning("Integer scaling is not supported for this resolution")
                    return True
            # Verification started
            status = self.verify_nn_is_scaling(scalarvalue[0].targetId, [scalarvalue[0]])
            if status is False:
                logging.error("ERROR : Failed to verify scaling. Exiting..")
                self.fail("Failed to verify scaling. Exiting")

            self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60)

            # NN/IS scaling verification post S3 power event
            status = self.verify_nn_is_scaling(scalarvalue[0].targetId, [scalarvalue[0]])
            if status is False:
                logging.error("ERROR : Failed to verify scaling. Exiting..")
                self.fail("Failed to verify scaling. Exiting")

            # Power state S5 power event
            if reboot_helper.reboot(self, 'test_step_3') is False:
                self.fail("Failed to reboot the system")
            break

    ##
    # @brief step-2 verify scaling after S5 power event.
    # @return - None
    def test_step_3(self):
        self.is_teardown_required = True
        logging.info("post reboot - verifying Scaling value")
        scaling = 2 if self.is_integer_scaling is True else 1

        for scalarkey, scalarvalue in self.scalar_config_dict.items():

            if self.virtual_mode_set_aware:
                status = self.verify_Intergerscaling_support(scalarvalue[0].targetId, [scalarvalue[0]])
                if status is True:
                    status = self.check_plane_scalar_status(scalarvalue[0].targetId, [scalarvalue[0]], 20)
                    if status is False:
                        logging.error("ERROR: Plane scalar is not enabled")
                        self.fail("Failed to enable plane scalar")
                else:
                    logging.warning("Integer scaling is not supported for this resolution")
                    return True
            # Verification started
            status = self.verify_nn_is_scaling(scalarvalue[0].targetId, [scalarvalue[0]])

            if status is False:
                logging.error("ERROR : Failed to verify scaling. Exiting..")
                self.fail("Failed to verify scaling. Exiting")

            # applying different mode set
            status = self.display_config.set_display_mode([scalarvalue[len(scalarvalue) - 1]],
                                                          virtual_mode_set_aware=self.virtual_mode_set_aware,
                                                          enumerated_displays=None)
            break


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('NNISScalingPersistenceS3S5'))
    TestEnvironment.cleanup(outcome)
