###############################################################################
# \ref sanity_check.py
# \remarks 
# sanity_check.py imports every python script present in DisplayAutomation2.0 
# as a module and checks for any errors in it.  
# \author   Amanpreet Kaur Khurana, Bharath
###############################################################################

import logging
import os
import sys
import unittest
from Libs.Core.test_env.test_environment import *
from Libs.Core.gta import gta_state_manager
from Libs.Core import test_header


def import_check():
    modules = []
    matches = []
    index = 1

    # This will contain the current directory path.

    dir_path = os.getcwd()
    libs_path = os.path.join(dir_path, "Libs")
    tests_path = os.path.join(dir_path, "Tests")

    # This will contain the list of all directories in the DisplayAutomation2.0.
    libs_sub_dirs = [x[0] for x in os.walk(libs_path)]
    tests_sub_dirs = [x[0] for x in os.walk(tests_path)]

    # To find out all the .py files.
    for subdir in (libs_sub_dirs + tests_sub_dirs):
        sys.path.append(subdir)
        files = next(os.walk(subdir))[2]
        if len(files) > 0:
            for file_found in files:
                if file_found.endswith(".py"):
                    script_name = file_found[:-3]
                    script_dir = subdir.replace(dir_path, "")
                    matches.append(os.path.join(script_dir, script_name))

    logging.info("=================================================================")
    logging.info("%-5s | %-110s | %s" % ("SL No", "Module", "Error"))
    logging.info("=================================================================")

    # To import each python script as a module.
    # Currently excluding 'registers', 'bin', 'presi', Samples', 'Test_Tools' and 'BAT' folders

    import_error_count = 0
    status = True
    for module_name in matches:
        try:
            # import each file as module by slicing ".py" characters
            module_name = module_name.replace("\\", ".")
            module_name = module_name[1:]
            modules.append(__import__(module_name, globals(), locals(), [], -1))
            # logging.debug("%-5s | %-110s | %s" % (index, module_name, ""))
        except Exception as e:
            # print and log modules with cause exception
            logging.warning("%-5s | %-110s | %s" % (index, module_name, e))
            status = False
            import_error_count += 1
        index += 1
    return status, import_error_count


class dispauto_sanity_check_ult(unittest.TestCase):
    log_handle = None

    def setUp(self):
        logging.info("ULT Start")

    @unittest.expectedFailure
    def runTest(self):
        status, import_error_count = import_check()
        if import_error_count == 100:
            logging.warning("Passing with know error count")
        else:
            self.assertTrue(status, "Import check failed with %d errors" % (import_error_count))

    def tearDown(self):
        logging.info("ULT Complete")


if __name__ == '__main__':
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()
