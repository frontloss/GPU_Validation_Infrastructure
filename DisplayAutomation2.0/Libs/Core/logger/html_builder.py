########################################################################################################################
# @file         html_builder.py
# @brief        Library for .log to .html conversion
# @author       Rohit Kumar, Kiran Kumar Lakshmanan
########################################################################################################################

import os
import re
import sys
import time

from xml.etree import ElementTree as Et

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STYLE_FILE_PATH = os.path.join(ROOT_FOLDER, "Libs", "Core", "logger", "style.css")
SCRIPT_FILE_PATH = os.path.join(ROOT_FOLDER, "Libs", "Core", "logger", "script.js")
STEP_START_PREFIX = "Step:"
STEP_START_PREFIX_HIGHLIGHT = "$Step$:"
STEP_START_PATTERN = r'Step[\-0-9]*:'
STEP_END_PREFIX = '-' * 64
SYSTEM_DETAILS_KEY_PLATFORM = "Platform"
TEST_RESULTS_START = "ANALYSE TEST RESULTS - START"
TEST_RESULTS_END = "ANALYSE TEST RESULTS - END"
TRACEBACK_PATTERN = "Traceback (most recent call last):"


##
# @brief        StepStatus Class
class StepStatus(object):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    UNKNOWN = "UNKNOWN"


##
# @brief        Step Class
class Step(object):

    ##
    # @brief        Constructor
    # @param[in]    index - Index of the Step
    # @param[in]    tr - Table row
    # @param[in]    status - Status of the Step
    # @param[in]    parent - Parent of the current HTML
    # @param[in]    highlight - True if Highlight is enable, False otherwise
    def __init__(self, index, tr, status, parent=None, highlight=False):
        self.index = int(index)
        self.last_sub_step_index = 0
        self.tr = tr
        self.status = status
        self.parent = parent
        self.result = StepStatus.PASSED
        self.highlight = highlight


##
# @brief        HtmlBuilder Class
class HtmlBuilder(object):

    ##
    # @brief        Constructor
    # @param[in]    log_file - Log Files
    # @param[in]    title - Title of the Log File
    def __init__(self, log_file, title="DisplayAutomation2.0 Logs"):
        self.path = log_file
        self.html = Et.Element('html', attrib={'lang': 'en'})
        self.head = self.__build_head(title)
        self.html.append(self.head)
        self.body = self.__build_body(title)
        self.html.append(self.body)

        table, t_body = HtmlBuilder.__build_system_details()
        self.body.append(table)
        self.system_details = t_body

        table, t_body = HtmlBuilder.__build_driver_details()
        self.body.append(table)
        self.driver_details = t_body

        table, t_body = HtmlBuilder.__build_test_logs(" ".join(sys.argv))
        self.body.append(table)
        self.test_logs = t_body

        table, th, t_body = HtmlBuilder.__build_test_result()
        self.body.append(table)
        self.test_result_title = th
        self.test_result = t_body

        table, t_body = HtmlBuilder.__build_traceback()
        self.body.append(table)
        self.traceback = t_body

        self.active_step = None
        self.root_step_index = 1
        self.test_logging_finished = False
        self.test_started = False
        self.test_end_reached = False
        self.traceback_started = False

    ##
    # @brief        load caller
    # @return       None
    def __load(self):
        if os.path.exists(self.path) is False:
            return

        self.system_details = self.driver_details = self.test_logs = self.test_result = None

        ##
        # @brief        Get Body API
        # @param[in]    child_element - Inner element in the Document
        # @param[in]    element_id - HTML id in the Document
        # @return       c - HTML element when tag='tbody'
        def get_tbody(child_element, element_id):
            if 'id' in child_element.attrib and child_element.attrib['id'] == element_id:
                for c in child_element:
                    if c.tag == 'tbody':
                        return c

        self.html = Et.parse(self.path).getroot()
        for child in self.html:
            if child.tag == 'head':
                self.head = child
            if child.tag == 'body':
                self.body = child

        for child in self.body:
            if child.tag == 'table':
                if self.system_details is None:
                    self.system_details = get_tbody(child, 'sys_d_table')
                if self.driver_details is None:
                    self.driver_details = get_tbody(child, 'driver_d_table')
                if self.test_logs is None:
                    self.test_logs = get_tbody(child, 'test_logs_table')
                if self.test_result is None:
                    self.test_result = get_tbody(child, 'test_r_table')
                    # for tr in self.test_result:
                    #     pass

    ##
    # @brief        New Caller
    # @param[in]    title - Title of the HTML Document
    # @param[in]    attrib - HTML element Attribute
    # @param[in]    text - Text to be added in the Document
    # @param[in]    file_path - HTML Document file path
    # @return       body - Body Attribute
    @staticmethod
    def __new(title, attrib, text=None, file_path=None):
        tag = Et.Element(title, attrib=attrib)
        if file_path is not None:
            with open(file_path) as f:
                tag.text = f.read()
        else:
            if text is not None and '\t' in str(text):
                margin = len([i for i in range(len(text)) if text.startswith('\t', i)])
                tab = Et.Element('span', attrib={'style': 'margin-left:{0}px;'.format(margin * 50)})
                pos = text.index('\t')
                tab.text = text[pos:]
                tag.append(tab)
            else:
                tag.text = str(text)
        return tag

    ##
    # @brief        API to build Head
    # @param[in]    title - Title of the Head Element
    # @return       head - Head Attribute
    @staticmethod
    def __build_head(title):
        head = Et.Element('head')
        head.append(Et.Element('meta', attrib={'charset': 'utf-8'}))
        head.append(HtmlBuilder.__new('title', {}, title))
        head.append(HtmlBuilder.__new('style', {'media': 'screen'}, file_path=STYLE_FILE_PATH))
        head.append(HtmlBuilder.__new('script', {'type': 'text/javascript'}, file_path=SCRIPT_FILE_PATH))
        return head

    ##
    # @brief        API to build body
    # @param[in]    title - Title of the Body Element
    # @return       body - Body Attribute
    @staticmethod
    def __build_body(title):
        body = Et.Element('body')
        body.append(HtmlBuilder.__build_nav_bar(title))
        return body

    ##
    # @brief        API to build Navigation Bar
    # @param[in]    title - Title of the Navigation Bar
    # @return       nav_bar - Navigation Bar Attribute
    @staticmethod
    def __build_nav_bar(title):
        nav_bar = Et.Element('nav', attrib={'class': 'navbar navbar-expand-lg navbar-light bg-light'})
        nav_bar.append(HtmlBuilder.__new('strong', {'class': 'navbar-brand'}, title))
        nav_bar.append(
            HtmlBuilder.__new(
                'button', {'class': 'btn bg-danger text-white', 'id': 'debugBtn', 'onclick': 'toggleDebugLogs()'},
                "Turn ON Debug Mode"))
        # nav_bar.append(
        #     HtmlBuilder.__new(
        #         'button',
        #         {'class': 'btn btn-outline-info', 'id': 'expandBtn', 'onclick': 'toggleCollapsibles()',
        #          'style': 'margin-left: 15px;'}, "Expand All"))

        return nav_bar

    ##
    # @brief        API to build System Details
    # @return       (String,String) - (Attributes for Table,Attribute for Table Body)
    @staticmethod
    def __build_system_details():
        table = Et.Element('table', attrib={'class': 'table table-striped table-sm', 'id': 'sys_d_table'})
        t_head = Et.Element('thead', attrib={'class': 'thead-dark', 'style': 'cursor:pointer;'})
        tr = Et.Element('tr', attrib={'class': 'trs h'})
        tr.append(
            HtmlBuilder.__new('th',
                              {'colspan': '2', 'class': 'table-head', 'onclick': 'toggleVisibility(\'sd\', \'table\')'},
                              "System Details"))
        t_head.append(tr)
        table.append(t_head)

        t_body = Et.Element('tbody', attrib={'class': 'tbody', 'id': 'sd', 'style': 'display: none;'})
        table.append(t_body)
        return table, t_body

    ##
    # @brief        API to build Driver Details
    # @return       (String,String) - (Attributes for Table,Attribute for Table Body)
    @staticmethod
    def __build_driver_details():
        table = Et.Element('table', attrib={'class': 'table table-striped table-sm', 'id': 'driver_d_table'})
        t_head = Et.Element('thead', attrib={'class': 'thead-dark', 'style': 'cursor:pointer;'})
        tr = Et.Element('tr')
        tr.append(HtmlBuilder.__new('th', {'colspan': '5'}, "Driver Details"))
        t_head.append(tr)
        tr = Et.Element('tr')
        tr.append(HtmlBuilder.__new('th', {}, "Service"))
        tr.append(HtmlBuilder.__new('th', {}, "Version"))
        tr.append(HtmlBuilder.__new('th', {}, "State"))
        tr.append(HtmlBuilder.__new('th', {}, "Hardware ID"))
        tr.append(HtmlBuilder.__new('th', {}, "Driver"))
        t_head.append(tr)
        table.append(t_head)

        t_body = Et.Element('tbody')
        table.append(t_body)

        return table, t_body

    ##
    # @brief        API to build test logs
    # @param[in]    cmdline - Command Line Argument
    # @return       (String,String) - (Attributes for Table,Attribute for Table Body)
    @staticmethod
    def __build_test_logs(cmdline):
        # table = Et.Element('table', attrib={'class': 'table table-sm', 'id': 'test_logs_table'})
        table = Et.Element('table', attrib={'class': 'table table-sm', 'id': 'test_logs_table'})
        t_head = Et.Element('thead', attrib={'class': 'thead-dark', 'style': 'cursor:pointer;'})
        tr = Et.Element('tr', attrib={'onclick': ''})
        tr.append(HtmlBuilder.__new('th', {'colspan': '10', 'class': 'text-left'}, "%s" % cmdline))
        t_head.append(tr)

        tr = Et.Element('tr')
        tr.append(HtmlBuilder.__new('th', {'style': 'width:100px;'}, "Time"))
        tr.append(HtmlBuilder.__new('th', {'style': 'width:100px;'}, "Step"))
        tr.append(HtmlBuilder.__new('th', {'style': 'width:150px;display:none;'}, "Result"))
        tr.append(HtmlBuilder.__new('th', {'class': 'dc', 'style': 'width:100px;'}, "File"))
        tr.append(HtmlBuilder.__new('th', {'class': 'dc', 'style': 'width:100px;'}, "Line"))
        tr.append(HtmlBuilder.__new('th', {'class': 'dc', 'style': 'width:100px;'}, "Function"))
        tr.append(HtmlBuilder.__new('th', {'class': 'text-left'}, "Message"))
        t_head.append(tr)
        table.append(t_head)

        t_body = Et.Element('tbody')
        table.append(t_body)

        return table, t_body

    ##
    # @brief        API to build test Result
    # @return       (String,String,String) - (Attributes for Table, Attribute for Table Head, Attribute for Table Body)
    @staticmethod
    def __build_test_result():
        table = Et.Element('table', attrib={'class': 'table table-sm', 'id': 'test_r_table'})
        t_head = Et.Element('thead', attrib={'class': 'thead-dark', 'style': 'cursor:pointer;'})
        tr = Et.Element('tr', attrib={'class': 'trs h'})
        th = HtmlBuilder.__new('th', {'colspan': '10', 'class': 'table-head'}, "TEST RESULT : RUNNING")
        tr.append(th)
        t_head.append(tr)
        table.append(t_head)

        t_body = Et.Element('tbody', attrib={'class': 'tbody'})
        table.append(t_body)
        return table, th, t_body

    ##
    # @brief        API to build Traceback
    # @return       (String,String) - (Attributes for Table,Attribute for Table Body)
    @staticmethod
    def __build_traceback():
        table = Et.Element('table', attrib={'class': 'table table-striped table-sm', 'id': 'traceback_table'})
        t_head = Et.Element('thead', attrib={'class': 'thead-dark', 'style': 'cursor:pointer;'})
        tr = Et.Element('tr', attrib={'class': 'trs h'})
        tr.append(
            HtmlBuilder.__new('th',
                              {'colspan': '2', 'class': 'table-head', 'onclick': 'toggleVisibility(\'tt\', \'table\')'},
                              "Traceback"))
        t_head.append(tr)
        table.append(t_head)

        t_body = Et.Element('tbody', attrib={'class': 'tbody', 'id': 'tt', 'style': 'display: none;'})
        table.append(t_body)
        return table, t_body

    ##
    # @brief        API to add System Detail
    # @param[in]    key - System Detail Key
    # @param[in]    value - Value to the corresponding key
    # @return       None
    def __add_system_detail(self, key, value):
        tr = Et.Element('tr')
        tr.append(HtmlBuilder.__new('td', {}, key))
        tr.append(HtmlBuilder.__new('td', {}, value))
        self.system_details.append(tr)

    ##
    # @brief        API to add Driver
    # @param[in]    service - Running Service for which Driver is to be added
    # @param[in]    version - Service Version
    # @param[in]    state - state of the Service
    # @param[in]    hardware_id - ID of the Hardware Involved
    # @param[in]    driver - Driver details of the Hardware
    # @return       None
    def __add_driver(self, service, version, state, hardware_id, driver):
        if 'Running'.lower() not in state.lower():
            tr = Et.Element('tr', attrib={'class': 'bg-warning'})
        else:
            tr = Et.Element('tr')
        tr.append(HtmlBuilder.__new('td', {}, service))
        tr.append(HtmlBuilder.__new('td', {}, version))
        tr.append(HtmlBuilder.__new('td', {}, state))
        tr.append(HtmlBuilder.__new('td', {}, hardware_id))
        tr.append(HtmlBuilder.__new('td', {}, driver))
        self.driver_details.append(tr)

    ##
    # @brief        Internal API to find the TextTestRunner frame.
    # @details      TextTestRunner frame is used to add errors and failures to unittest result in case of setUp()
    #               and test() failure. todo : handle the failing case
    # @param[in]    f_back - current frame
    # @return       f_back - TextTestRunner frame    -
    def __find_runner_frame(self, f_back):
        ##
        # Check for orig_result and result properties to identify the frame instance.
        # These properties are part of TextTestRunner object.
        if ('orig_result' not in f_back.f_locals.keys()) or ('result' not in f_back.f_locals.keys()):
            return self.__find_runner_frame(f_back.f_back)
        return f_back

    ##
    # @brief        Add step
    # @param[in]    timestamp - Result log timestamp
    # @param[in]    filename - Filename of which log is generated
    # @param[in]    line - string of which warning is to be generated
    # @param[in]    function - method to be tested
    # @param[in]    message - Message to be logged
    # @param[in]    highlight - True, if message has to be highlighted, False otherwise
    # @return       None
    def __add_step(self, timestamp, filename, line, function, message, highlight=False):
        parent = None
        index = str(self.root_step_index)
        if self.active_step is None:
            self.root_step_index += 1
        else:
            if self.active_step.status.text == StepStatus.RUNNING:
                self._close_step(self.active_step.result)
                return self.__add_step(timestamp, filename, line, function, message)
                # index = str(self.active_step.index) + '.' + str(self.active_step.last_sub_step_index)
                # parent = self.active_step

        if self.active_step is not None and self.active_step.status is None:
            # last step didn't close properly
            self.active_step.status.text = StepStatus.UNKNOWN
            self.active_step.tr.set('class', 'bg-warning')

        tr = Et.Element('tr', attrib={'class': 'bg-primary text-white'})
        tr.set('onclick', 'toggleStepView(\'%s\')' % index)

        tr.append(HtmlBuilder.__new('td', {}, timestamp))
        tr.append(HtmlBuilder.__new('td', {}, "STEP " + str(index)))
        active_step_status = HtmlBuilder.__new('td', {'style': 'display: none;'}, StepStatus.RUNNING)
        tr.append(active_step_status)
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, filename))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, line))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, function))
        tr.append(HtmlBuilder.__new('td', {'class': 'step msg'}, message))

        self.active_step = Step(index, tr, active_step_status, parent, highlight)

        if self.active_step.last_sub_step_index is not None and self.active_step.last_sub_step_index != 0:
            self.active_step.last_sub_step_index += 1
        else:
            self.active_step.last_sub_step_index = 1

        self.test_logs.append(tr)

    index = 0

    ##
    # @brief        API for Close Step
    # @param[in]    step_result - True if Result status is Passed, False otherwise
    # @return       None
    def _close_step(self, step_result):
        if self.active_step:
            if step_result == StepStatus.FAILED:
                # Failed
                self.active_step.status.text = StepStatus.FAILED
                self.active_step.tr.set('class', 'bg-danger text-white')
            elif step_result == StepStatus.PASSED:
                # Passed
                self.active_step.status.text = StepStatus.PASSED
                if self.active_step.highlight:
                    self.active_step.tr.set('class', 'bg-primary text-white')
                else:
                    self.active_step.tr.set('class', 'bg-success text-white')
            elif step_result == StepStatus.WARNING:
                # Passed but generated warning
                self.active_step.status.text = StepStatus.PASSED
                self.active_step.tr.set('class', 'bg-warning')

            self.active_step = self.active_step.parent

            # if parent is still active, increase the last sub step index
            if self.active_step is not None:
                self.active_step.last_sub_step_index += 1

    ##
    # @brief        Add log Caller
    # @param[in]    level - level of Exception
    # @param[in]    timestamp - Result log timestamp
    # @param[in]    filename - Filename of which log is generated
    # @param[in]    line - string of which warning is to be generated
    # @param[in]    function - method to be tested
    # @param[in]    message - Message to be logged
    # @param[in]    *args - Arguments
    # @param[in]    **kwargs - Arguments
    # @return       None
    def __add_log(self, level, timestamp, filename, line, function, message, *args, **kwargs):
        parent = None
        if 'parent' in kwargs:
            parent = kwargs['parent']
        index = self.active_step.index if self.active_step is not None else 0
        display = 'none' if index > 0 else 'table-row'
        level = level.lower()

        bg_color = ''
        if level == 'warning':
            bg_color = 'bg-warning'
            if self.active_step is not None:
                self.active_step.result = StepStatus.WARNING
        elif level in ['error', 'exception', 'critical']:
            bg_color = 'bg-danger text-white'
            if self.active_step is not None:
                self.active_step.result = StepStatus.FAILED

        if parent is not None:
            tr = Et.Element('tr', attrib={'class': '{0}'.format(bg_color)})
        elif level in ['debug', 'adv_debug']:
            tr = Et.Element('tr', attrib={'class': 'dr sl{0} {1}'.format(index, bg_color)})
        else:
            tr = Et.Element(
                'tr', attrib={'class': 'sl{0} {1}'.format(index, bg_color), 'style': 'display:{0};'.format(display)})

        tr.append(HtmlBuilder.__new('td', {}, timestamp))
        tr.append(HtmlBuilder.__new('td', {}, ""))
        tr.append(HtmlBuilder.__new('td', {'style': 'display: none;'}, ""))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, filename))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, line))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, function))
        tr.append(HtmlBuilder.__new('td', {}, message))
        if parent is None:
            self.test_logs.append(tr)
        else:
            parent.append(tr)

    ##
    # @brief        Add test result Caller
    # @param[in]    is_passed - True if test result is Passed, False otherwise
    def _add_test_result(self, is_passed):
        self.test_result_title.text = "TEST RESULT : PASSED" if is_passed else "TEST RESULT : FAILED"

    ##
    # @brief        Add test result log Caller
    # @param[in]    level - level of Exception
    # @param[in]    timestamp - Result log timestamp
    # @param[in]    filename - Filename of which log is generated
    # @param[in]    line - string of which warning is to be generated
    # @param[in]    function - method to be tested
    # @param[in]    message - Message to be logged
    # @param[in]    *args - Arguments
    # @param[in]    **kwargs - Arguments
    def __add_test_result_log(self, level, timestamp, filename, line, function, message, *args, **kwargs):
        display = 'table-row'
        level = level.lower()

        bg_color = ''
        if level == 'warning':
            bg_color = 'bg-warning'
        elif level in ['error', 'exception', 'critical']:
            bg_color = 'bg-danger text-white'
        index = -1
        tr = Et.Element(
            'tr', attrib={'class': 'sl{0} {1}'.format(index, bg_color), 'style': 'display:{0};'.format(display)})

        tr.append(HtmlBuilder.__new('td', {}, timestamp))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, filename))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, line))
        tr.append(HtmlBuilder.__new('td', {'class': 'dc'}, function))
        tr.append(HtmlBuilder.__new('td', {}, message))

        self.test_result.append(tr)

    ##
    # @brief        Add Traceback Caller
    # @param[in]    line - string to be traced back
    def __add_traceback(self, line):
        tr = Et.Element('tr')
        tr.append(HtmlBuilder.__new('td', {}, ''))
        tr.append(HtmlBuilder.__new('td', {}, line))
        self.traceback.append(tr)

    ##
    # @brief        Write Caller
    # @return       None
    def _write(self):
        try:
            with open(self.path, 'wb') as f:
                Et.ElementTree(self.html).write(f, encoding='utf-8', method='html')
        except IOError:
            try:
                time.sleep(1)
                with open(self.path, 'wb') as f:
                    Et.ElementTree(self.html).write(f, encoding='utf-8', method='html')
            except IOError:
                return

    ##
    # @brief        Helper API to parse a single line from .log file
    # @param[in]    line - string to be parsed
    # @return       None
    def _parse_line(self, line):
        # Skip empty lines
        line = line.strip()
        if len(line) == 0 or line == '':
            return

        # Skip decoration lines
        if re.match(r'^[_\W]+$', line):
            self.traceback_started = False
            return

        if self.test_logging_finished:
            return

        # System Details
        # [Start with '|'] [string with chars or space][optional -gfx_index] : [Any String] [end with '|']
        # Example: "| Environment : Post-Si |"
        if re.match(r'[|][ \w]+[-gfx_0-9 ]*[:].*[|]', line) and self.test_started is False:
            line = line[1:-1].strip()
            self.__add_system_detail(line.split(':', 1)[0], line.split(':', 1)[1])
            return

        # Driver Details
        if re.match(r'[|].+[\[][\w]+[]].*[|]', line) and SYSTEM_DETAILS_KEY_PLATFORM not in line:
            line = line[1:-1].strip()
            try:
                service = re.search(r'.+[\[]', line).group(0)[0:-1].strip().split(' ')[0]
            except AttributeError:
                service = 'None'
            try:
                version = re.search(r'.+[\[]', line).group(0)[1:-1].strip().split(' ')[-1]
            except AttributeError:
                version = 'None'
            try:
                state = re.search(r'[\[].+[]]', line).group(0)
            except AttributeError:
                state = 'None'
            try:
                hardware_id = re.search(r'[]].+[:]', line).group(0)[1:-1].strip()
            except AttributeError:
                hardware_id = 'None'
            try:
                driver = line.split(':')[-1].strip()
            except AttributeError:
                driver = 'None'
            self.__add_driver(service, version, state, hardware_id, driver)
            return

        # Test result analysis section
        if TEST_RESULTS_START.lower() in line.lower() or self.test_end_reached:
            if TEST_RESULTS_START.lower() in line.lower():
                self.test_end_reached = True
                return
            if TEST_RESULTS_END.lower() in line.lower():
                return

            # Traceback
            if TRACEBACK_PATTERN in line or self.traceback_started:
                self.traceback_started = True
                self.__add_traceback(line)
            else:
                if 'Passed = ' in line and 'Failed = ' in line:
                    self.test_logging_finished = True
                    return
                if '.py' not in line and 'runTest' not in line:
                    self.__add_test_result_log('ERROR', '', '', '', '', line)
            return

        # Logs
        if re.match(r'[\[].+', line):
            self.test_started = True
            meta_data = line.split(']', 1)[0] + ']'
            level = re.search(r'[:][ ][A-Z_]+[ ]+[]]', meta_data).group(0)[1:-1].strip()
            timestamp = re.search(r'[\[][ ][0-9]+[:][0-9]+[:][0-9]+[ ]', meta_data).group(0)[1:-1].strip()
            filename = re.search(r'[ ][\w]+.py', meta_data).group(0)[1:].strip()
            line_no = re.search(r'[:][0-9]+[ ]+[-]', meta_data).group(0)[1:-1].strip()
            function = re.search(r'[-][ ]+.+[ ][:]', meta_data).group(0)[1:-1].strip()
            message = line.split(']', 1)[1]

            if level in ['CRITICAL', 'ERROR']:
                self.__add_test_result_log(level, timestamp, filename, line_no, function, message)

            # Check for highlighted step start
            step = re.match(STEP_START_PATTERN, message.strip(), flags=re.IGNORECASE)
            if STEP_START_PREFIX_HIGHLIGHT in message.strip():
                message = message.strip()
                self.__add_step(timestamp, filename, line_no, function, message.replace(STEP_START_PREFIX_HIGHLIGHT, ''),
                              True)
            elif step:
                message = message.strip()[step.span()[1]:]
                # html.close_step()
                self.__add_step(timestamp, filename, line_no, function, message.replace(STEP_START_PREFIX, ''))
            elif STEP_END_PREFIX in message:
                if self.active_step is not None:
                    self._close_step(self.active_step.result)
            else:
                self.__add_log(level, timestamp, filename, line_no, function, message)

        # Empty logs
        if re.match(r'[a-zA-Z]+', line):
            if self.traceback_started:
                print(line)
                self.__add_traceback(line)
            else:
                self.__add_log('INFO', '', '', '', '', line)
