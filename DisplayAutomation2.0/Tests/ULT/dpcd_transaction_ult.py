import unittest
from Libs.Core import enum
from Libs.Core import cmd_parser
from Libs.Core import display_power as disp_pwr
from Libs.Core.display_config import display_config
from Libs.Core.sw_sim import gfxvalsim
from Libs.Core.sw_sim import dpcd_model_data_struct as model_data
from Libs.Core.test_env.test_environment import *
from Libs.Core.display_utility import *


class DpcdTransactionULT(unittest.TestCase):

    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        self.dp_displays_in_cmdline = []
        self.display_power = disp_pwr.DisplayPower()
        self.config = display_config.DisplayConfiguration()
        self.valsim = gfxvalsim.GfxValSim()


        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if (value['connector_port'] is not None) and ('DP' in value['connector_port']):
                    self.dp_displays_in_cmdline.append(value['connector_port'] + "_" + value['connector_port_type'])

    def tearDown(self):
        for display in self.dp_displays_in_cmdline:
            connector_port = display.split('_')[0] + '_' + display.split('_')[1]
            connector_type = display.split('_')[2]
            unplug(connector_port, False, connector_type)

    def test_1(self):
        # plug displays with is_low_power=False
        for display in self.dp_displays_in_cmdline:
            connector_port = display.split('_')[0] + '_' + display.split('_')[1]
            connector_type = display.split('_')[2]

            # fill DP link training model data
            dp_dpcd_model_data = model_data.DPDPCDModelData()
            logging.info('Filling link training transactions in DPCD model data')
            self.valsim._fill_default_dpcd_model_data(dp_dpcd_model_data, connector_port)

            logging.info("Plugging display {0} by passing LT model data to plug".format(display))
            plug(connector_port, edid="Acer_H277HK_DP.bin", dpcd="Acer_H277HK_nonVRR_DPCD.txt", is_low_power=False,
                 port_type=connector_type, dp_dpcd_model_data=dp_dpcd_model_data)

        for display in self.dp_displays_in_cmdline:
            connector_port = display.split('_')[0] + '_' + display.split('_')[1]
            if self.config.set_display_configuration_ex(enum.SINGLE, [connector_port]) == False:
                self.fail("SetDisplayConfigurationEX returned false")
            else:
                logging.info('Applying single {0} configuration successful'.format(display))

    def test_2(self):
        # plug displays with is_low_power=True
        for display in self.dp_displays_in_cmdline:
            connector_port = display.split('_')[0] + '_' + display.split('_')[1]
            connector_type = display.split('_')[2]

            # fill DP link training model data
            dp_dpcd_model_data = model_data.DPDPCDModelData()
            logging.info('Filling link training transactions in DPCD model data')
            self.valsim._fill_default_dpcd_model_data(dp_dpcd_model_data, connector_port)

            logging.info("Plugging display {0} with low_power by passing LT model data to plug".format(display))
            plug(connector_port, edid="Acer_H277HK_DP.bin", dpcd="Acer_H277HK_nonVRR_DPCD.txt", is_low_power=True,
                 port_type=connector_type, dp_dpcd_model_data=dp_dpcd_model_data)

        # Invoke S3 state
        if self.display_power.invoke_power_event(disp_pwr.PowerEvent.S3, 30):
            logging.info("Invoking S3 Power Event: Success")
            time.sleep(5)
        else:
            logging.info("Invoking S3 Power Event: Failed")
            return False
        time.sleep(10)

        for display in self.dp_displays_in_cmdline:
            connector_port = display.split('_')[0] + '_' + display.split('_')[1]
            if self.config.set_display_configuration_ex(enum.SINGLE, [connector_port]) == False:
                self.fail("SetDisplayConfigurationEX returned false")
            else:
                logging.info('Applying single {0} configuration successful'.format(display))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
