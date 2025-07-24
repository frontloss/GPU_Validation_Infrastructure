#######################################################################################################################
# @file                 manual_hdr_verification_utility.py
# @addtogroup           Test_Color
# @section              manual_hdr_verification_utility
# @remarks              @ref manual_hdr_verification_utility.py \n
#                       The test script aides in the verification of Metadata while running the Manual tests.
#                       The Manual test mandates to collect an ETL with the HDR Modeset captured in it.
#                       This script takes the ETL as an input and parses the same and with the exisiting APIs,
#                       gets the appropriate Default and FLip Metadata and creates the reference metadata.
#                       Then, based on the Display type, the programmed metadata is read from the registers and compared
#                       If the Display type is HDMI2.1 over PCON, then the test expects PCON path True as an input parameter
#                       Currently, the script is only capable of parsing the details for a single display,
#                       Will plan to extend to multiple displays and perform all other HDR related verification
#                       which could be leveraged in the Manual test.
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *


class HDRBasic(HDRTestBase):

    def setUp(self):
        self.custom_tags["-ETL"] = None
        self.custom_tags["-PCON"] = False
        super().setUp()
        self.pcon_path = str(self.context_args.test.cmd_params.test_custom_tags["-PCON"][0])

    def runTest(self):
        etl_name = str(self.context_args.test.cmd_params.test_custom_tags["-ETL"][0])
        interim_path = "bin\\EtlParser\\" + etl_name
        etl_path = os.path.join(self.context_args.test.path_info.root_path, interim_path)

        if os.path.exists(etl_path):
            logging.debug("The ETL {0} is available for parsing".format(etl_name))
        else:
            logging.error("The ETL {0} is NOT available for parsing".format(etl_name))
            gdhm.report_driver_bug_os("Failed to parse ETL as ETL not available in parse path: {0}"
                                        .format(etl_path))
            self.fail()

        if etl_parser.generate_report(etl_path) is False:
            logging.error("Failed to generate EtlParser report")
            self.fail()
        else:
            logging.info("Successfully generated EtlParser report")

            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    panel_props = color_properties.HDRProperties()
                    self.panel_props_dict[gfx_index, port] = panel_props

                    status, default_metadata = color_etl_utility.get_default_hdr_metadata_from_etl(panel.target_id)
                    if status is False:
                        logging.debug("No new Default Metadata issued by OS")
                        logging.debug("Considering the Default Metadata already available in the context")
                    else:
                        logging.info(
                            "OS has issued new Default Metadata, hence overriding the Default Metadata available in "
                            "context")
                        ##
                        # Take the latest Default Metadata from the list of metadata available
                        panel_props.default_metadata = default_metadata[-1]

                    ##
                    # Fetch the Flip Metadata from the ETL for the particular target-id
                    status, flip_metadata = color_etl_utility.get_flip_hdr_metadata_from_etl(panel.target_id)
                    if status is False:
                        logging.debug("No new Flip Metadata issued by OS")
                        logging.debug("Considering the Flip Metadata already available in the context")
                    else:
                        logging.info(
                            "OS has issued new Flip Metadata, hence overriding the Flip Metadata available in context")
                        panel_props.flip_metadata = flip_metadata

                    self.pipe_args.desired_max_cll = panel.HDRDisplayCaps.desired_max_cll
                    self.pipe_args.desired_max_fall = panel.HDRDisplayCaps.desired_max_fall
                    self.pipe_args.default_metadata = self.panel_props_dict[gfx_index, port].default_metadata
                    self.pipe_args.flip_metadata = self.panel_props_dict[gfx_index, port].flip_metadata
                    self.pipe_args.bpc = self.panel_props_dict[gfx_index, port].bpc
                    if hdr_utility.hdr_verification(self.pipe_args, gfx_index, adapter.platform, port, panel,
                                                    self.pipe_args.bpc, self.pcon_path) is False:
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
