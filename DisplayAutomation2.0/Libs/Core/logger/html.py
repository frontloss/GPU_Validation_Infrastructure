########################################################################################################################
# @file         html.py
# @brief        Library for HTML logging
# @author       Rohit Kumar
########################################################################################################################
import logging
from functools import wraps

from Libs.Core.logger.html_builder import *


##
# @brief        Callable
def __(decorator):
    ##
    # @brief        caller_layer
    def caller_layer(*args, **kwargs):
        ##
        # @brief        Callee_layer
        def callee_layer(f):
            return decorator(f, *args, **kwargs)

        return callee_layer

    return caller_layer


@__
##
# @brief        Step function
# @param[in]    func - Function
# @param[in]    message - step function message
# @return       wrapper -
def step(func, message: str = None):
    wraps(func)

    ##
    # @brief        wrapper
    # @param[in]    *ars -
    # @param[in]    **kwargs -
    # @return       result -
    def wrapper(*args, **kwargs):
        logging.info(f"{STEP_START_PREFIX} {message}")
        result = func(*args, **kwargs)
        logging.info(f"{STEP_END_PREFIX}")
        return result

    return wrapper


##
# @brief        Exposed API to start HTML step
# @param[in]    message - str, step title
# @param[in]    highlight - highlighted steps will be colored in blue if passed
# @return       None
def step_start(message: str, highlight: bool = False):
    prefix = STEP_START_PREFIX
    if highlight:
        prefix = STEP_START_PREFIX_HIGHLIGHT
    logging.info(f"{prefix} {message}")


##
# @brief        Exposed API to end HTML step
# @return       None
def step_end():
    logging.info(f"{STEP_END_PREFIX}")


##
# @brief        Exposed API to convert .log file into .html
# @param[in]    log_file_path - .log file path
# @param[in]    test_result - test result
# @return       html_file_path - string, if successful, None otherwise
def process_logs(log_file_path, test_result):
    assert log_file_path
    assert os.path.exists(log_file_path)

    html_file_path = log_file_path + '.html'
    html = HtmlBuilder(html_file_path)
    with open(log_file_path) as fp:
        for cnt, line in enumerate(fp):
            html._parse_line(line)
    if html.active_step is not None:
        html._close_step(html.active_step.result)
    else:
        html._close_step(StepStatus.PASSED)
    html._add_test_result(test_result)
    html._write()


if __name__ == '__main__':
    process_logs('display_config_switching.txt', False)
