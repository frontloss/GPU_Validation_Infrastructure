##
# @file dd_base.py \n
# @brief This script contains helper functions along with setUp and tearDown methods of unittest framework.
#        that will be used by Display Diagnostic test scripts
#
# @author  Nainesh Doriwala


import codecs
import os
import re

from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Tests.TDR.tdr_base import *


##
# @brief It contains setUp and tearDown methods of Unittest framework
class DisplayDiagnosticBase(TDRBase):
    DD_test_store = os.path.join(test_context.TEST_STORE_FOLDER, "TestSpecificBin", "Start_Stop")

    ##
    # @brief parse_CDI_log_file - parse Collect Diagnostic Information log file
    # @return String - log details [Failed] or [Passed]
    def parse_CDI_log_file(self):
        log_file = codecs.open('%s\\Display_Diagnostic.log' % test_context.TestContext.logs_folder(), 'r',
                               encoding='utf-16')
        for input_line in log_file:
            if input_line.startswith('Error'):
                logging.info(input_line)
            if input_line.startswith('EndGroup: CollectDiagnosticInfo::CallCollectDiagnosticInfo'):
                return re.search('\[.*\]', input_line).group(0)

    ##
    # @brief parse_DDI_log_file - parse Display Diagnostic information log file
    # @return String - log details [Failed] or [Passed]
    def parse_DDI_log_file(self):
        status = '[Passed]'
        test_1, test_2 = None, None

        log_file = codecs.open('%s\\Display_Diagnostic.log' % test_context.TestContext.logs_folder(), 'r',
                               encoding='utf-16')

        for input_line in log_file:
            if input_line.startswith('Error'):
                logging.debug(input_line)

            if input_line.startswith(
                    'EndGroup: OSG::GRFX::DisplayKernel::DisplayDiagnostics::VerifyDisplayDiagnosticsSupported'):
                test_1 = re.search('\[.*\]', input_line).group(0)
                logging.info("DisplayKernel::DisplayDiagnostics::VerifyDisplayDiagnosticsSupported : %s" % test_1)
            elif input_line.startswith(
                    'EndGroup: OSG::GRFX::DisplayKernel::DisplayDiagnostics::VerifyDisplayDiagnosticsBlackContent'):
                test_2 = re.search('\[.*\]', input_line).group(0)
                logging.info("DisplayKernel::DisplayDiagnostics::VerifyDisplayDiagnosticsBlackContent : %s" % test_2)

        if test_1 == '[Failed]' or test_2 == '[Failed]':
            status = '[Failed]'
            return status
        elif test_1 == '[Passed]' and test_2 == '[Passed]':
            status = '[Passed]'
            return status

    ##
    # @brief run_CDI_test_tool - API to run CDI test tool
    # @return None
    def run_CDI_test_tool(self):
        os.system("%s\\DxgkTests\\te.exe %s\\DxgkTests\\CollectDiagnosticInfo.HLK.dll > %s\\Display_Diagnostic.log" % (
            self.DD_test_store, self.DD_test_store, test_context.TestContext.logs_folder()))

    ##
    # @brief run_DDI_test_tool - API to run DDI test tool
    # @return None
    def run_DDI_test_tool(self):
        os.system("%s\\DxgkTests\\te.exe %s\\DxgkTests\\DisplayDiagnostics.HLK.dll > %s\\Display_Diagnostic.log" % (
            self.DD_test_store, self.DD_test_store, test_context.TestContext.logs_folder()))

    ##
    # @brief verify_Display_Diagnostics - verify Display Diagnostics logs and information
    # @return Boolean - True if pass else False
    def verify_Display_Diagnostics(self):
        # OS Build Info
        machine_info = SystemInfo()
        self.os_info = machine_info.get_os_info()
        result = '[Failed]'
        if self.os_info.BuildNumber >= '18960':
            logging.debug("Display Diagnostics is supported from OS build 18960+")
            result = self.parse_DDI_log_file()
        else:
            logging.debug("Display Diagnostics is not supported for OS build %s" % self.os_info.BuildNumber)
        if result == '[Passed]':
            return True
        else:
            return False

    ##
    # @brief verify_Collect_Diagnostics - verify Collect Diagnostics logs and information
    # @return Boolean - True if pass else False
    def verify_Collect_Diagnostics(self):
        result = self.parse_CDI_log_file()
        if result == '[Passed]':
            return True
        else:
            return False


if __name__ == '__main__':
    unittest.main()
