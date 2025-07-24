#######################################################################################################################
# @file                 elp_persistence_with_hdr.py
# @brief                This test script is a basic script where optimization levels are applied
#                       and persistence with HDR is verified. ELP is expected to persist across HDR and SDR Mode.
#                       Also, set a new optimization level while in HDR Mode and verify if it persists in SDR Mode
#                       This test is intended to be a semi-auto test;
#                       Currently, the optimization for 'Image Quality' option in DC mode to enable HDR capability
#                       needs to be done manually
# Sample CommandLines:  python elp_persistence_with_hdr.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ELP.elp_test_base import *
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase


class elpPersistenceWithHdrBasic(ELPTestBase):
    ##
    # @brief - ELP Stress test
    def test_01_with_hdr(self):
        # ##
        # # Enable ELP on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2 : Enable HDR on all supported panels and verify persistence of ELP***")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()

        logging.info("Performing verification of ELP Persistence after enabling HDR")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                        self.fail()

        logging.info("*** Step 3 : Set a different Optimization Strength***")
        while True:
            new_level = random.randint(1, 3)
            if self.user_opt_level != new_level:
                break
        self.user_opt_level = new_level
        logging.info("Trying to update the Optimization Level to {0} in HDR Mode".format(self.user_opt_level))
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 4 : Disable HDR on all the supported panels and verify persistence of ELP***")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()

        logging.info("Performing verification of ELP Persistence after disabling HDR")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                        self.fail()

    def tearDown(self):
        ##
        # Disable HDR if there was an exception raised and HDR could not be disabled
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()

        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels and verifying the persistence with HDR Mode")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
