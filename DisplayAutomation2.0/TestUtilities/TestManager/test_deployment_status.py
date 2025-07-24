########################################################################################################################
# \file         test_deployment_status.py
# \addtogroup   PyTools_TestDeploymentStatus
# \brief        This Utility scans all the valid "<TestSet>.xml" files present in Automation 2.0 framework and converts
#               test details present in <TestSet>.xml to .csv file format (Which can be used for test management like
#               to get supported platform , OS , Test qualification status etc..).
# \remarks
#   Utility Reports :
#       PASS : If Test Details and Command line Parsing is Successful.
#       SKIP : If .xml files contains data other than test / command line details.
#               (Example : DELL_UP3216Q_HDMI.xml - which is test specific data)
#       FAIL : If Required Test Details and Command line parameter are missing.
#
#   Valid TestSet.xml Field are:
#       <Display_Automation_2.0>
#           <Feature Name="" Owner="">
#               <Test Name="" Owner="" Priority="" LastModifiedWW="2017.WW24" Version="1">
#                   <TestInstance Id="MDENM001" Grids="ETM;PreETM;CI">
#                       <CommandLine>python </CommandLine>
#                       <OS>WinTH2;WinRS1;WinRS2</OS>
#                       <Platform>ICL</Platform>
#                       <TestEnvironment>ICL_HP_SOC</TestEnvironment>
#                       <ExecutionTime_mm>00</ExecutionTime_mm>
#                       <AdditionalTag>NONE</AdditionalTag>
#                       <QualificationStatus>None</QualificationStatus>
#                   </TestInstance>
#               </Test>
#           </Feature>
#       </Display_Automation_2.0>
#
#   Valid Query.xml Field are:
#       <TestSetQuery>
#           <Query Platform="" OS="" Branch="" TestEnvironment=""/>
#       </TestSetQuery>
#
#  Usage:
#    python test_deployment_status.py -a (dump | update) -p (Binary path) [-x (filter xml) -c (csv file)]
#
#    Mandatory Parameters:
#       -a (or) --ACTION : Specify whether to Dump or Update Test Set xml files.
#    Optional Parameters:
#       -p (or) --PATH   : Specify Binary path or xml file path (Sub-dirs of given path is also included).
#       -x (or) --XML    : Required when user need to pass query xml file.
#       -c (or) --CSV    : Required when user need to convert csv file to xml file.
#
# \author
#   Name    : Gurusamy, BalajiX
#   Date    : WW 09.1'2018
#   Rev     : 2.0
########################################################################################################################
import os
import sys
import xml
import time
import ctypes
import logging
import argparse
from datetime import datetime
import xml.etree.ElementTree as Et


##
# Structure definition for Test Set XML fields.
class XmlDataStructure(ctypes.Structure):
    _fields_ = [
        ('folder_name',          ctypes.c_wchar_p),
        ('filename',             ctypes.c_wchar_p),
        ('feature_name',         ctypes.c_wchar_p),
        ('feature_owner',        ctypes.c_wchar_p),
        ('test_name',            ctypes.c_wchar_p),
        ('test_owner',           ctypes.c_wchar_p),
        ('priority',             ctypes.c_wchar_p),
        ('version',              ctypes.c_wchar_p),
        ('last_modified',        ctypes.c_wchar_p),
        ('grids',                ctypes.c_wchar_p),
        ('id',                   ctypes.c_wchar_p),
        ('command_line',         ctypes.c_wchar_p),
        ('os',                   ctypes.c_wchar_p),
        ('platform',             ctypes.c_wchar_p),
        ('test_environment',     ctypes.c_wchar_p),
        ('execution_time',       ctypes.c_wchar_p),
        ('additional_tag',       ctypes.c_wchar_p),
        ('qualification_status', ctypes.c_wchar_p)
    ]


##
# Definition for Test Set XML Tags.
class TagNames(object):
    # Module Head Tags
    da_root = 'Display_Automation_2.0'
    feature = 'Feature'
    test = 'Test'
    test_instance = 'TestInstance'
    # Feature Module's attributes
    feature_name = 'Name'
    feature_owner = 'Owner'
    # Test Module's attributes
    test_name = 'Name'
    test_owner = 'Owner'
    test_priority = 'Priority'
    test_version = 'Version'
    test_last_modified = 'LastModifiedWW'
    # TestInstance Module's attributes
    ti_id = 'Id'
    ti_grids = 'Grids'
    # TestInstance Module's sub tags
    ti_command_line = 'CommandLine'
    ti_os = 'OS'
    ti_platform = 'Platform'
    ti_test_environment = 'TestEnvironment'
    ti_execution_time = 'ExecutionTime_mm'
    ti_additional_tag = 'AdditionalTag'
    ti_qualification_status = 'QualificationStatus'


##
# This class helps to Dump Test Set XML file to csv file.
class DumpTestDeploymentStatus(object):

    def __init__(self):
        self.filter_counter = {}
        self.filter_headers = []
        time_stamp = datetime.now().strftime('%H%M%S')
        self.csv_file_name = 'Test_Deployment_Status_{0}.csv'.format(time_stamp)
        self.counter_file = 'Test_Deployment_Status_{0}_FilterCount.csv'.format(time_stamp)
        self.column_headers = ['FolderName', 'FileName', 'Feature Name', 'Feature Owner', 'Test Name', 'Test Owner',
                               'Priority', 'LastModifiedWW', 'Version', 'Id', 'Grids', 'CommandLine', 'OS', 'Platform',
                               'TestEnvironment', 'ExecutionTime_mm', 'AdditionalTag', 'QualificationStatus']

    ##
    # @brief Retrieves Binary Version details from version.txt and Dump version and Heading details to the csv file.
    # @param[in] - String: Automation Binary path (auto_binary_path)
    # @param[in] - List: Supported configuration filter details (supp_config)
    # @param[in] - List: Qualification config filter details (qualification_config)
    # @return - Does not return anything
    def add_binary_version_and_csv_header(self, auto_binary_path, supp_config=None):
        if os.path.exists(self.csv_file_name):
            os.remove(self.csv_file_name)
        # Get DisplayAutomation2.0 Version details from version.txt
        ver_details = None
        try:
            version_file = os.path.join(auto_binary_path, "version.txt")
            with open(version_file, 'r') as file_handle:
                ver_details = file_handle.readline().strip()
        except Exception as ex:
            logging.debug("Exception : {}".format(ex))

        if ver_details is None:
            logging.error("Binary version not found")
        else:
            logging.info("Binary version : {}".format(ver_details))

        for supp_os_config in supp_config['OS']:
            self.column_headers.append("S.Status:{}".format(supp_os_config))
            self.filter_headers.append(supp_os_config)
        for supp_platform_config in supp_config['Platform']:
            self.column_headers.append("S.Status:{}".format(supp_platform_config))
            self.filter_headers.append(supp_platform_config)
        for supp_environment_config in supp_config['TestEnvironment']:
            self.column_headers.append("S.Status:{}".format(supp_environment_config))
            self.filter_headers.append(supp_environment_config)

        # Write Binary Version and Header details to CSV file.
        with open(self.csv_file_name, 'a') as csv_file_handle:
            csv_file_handle.write("DisplayAutomation: Version,{},Legend: S.Status=Supported Status".format(ver_details))
            csv_file_handle.write('\n')
            csv_file_handle.write(",".join(map(lambda x: '"{}"'.format(x), self.column_headers)))
            csv_file_handle.write('\n')
        # If len of filter_header is more than 0, then query is passed. Adding header for counter file.
        if len(self.filter_headers) > 0:
            with open(self.counter_file, 'w') as counter_file:
                counter_file.write("Filename,Folder Name,")
                counter_file.write(",".join(map(lambda x: '"{}"'.format(x), self.filter_headers)))
                counter_file.write('\n')

    ##
    # @brief Retrieves all Test details from given TestSet xml file and dump it to CSV file.
    # @param[in] - String: xml file absolute path (filename)
    # @param[in] - List: Supported configuration filter details (supp_config)
    # @param[in] - List: Qualification config filter details (qualification_config)
    # @return - Dict: Result as Key and Message as Value
    def read_xml(self, root_path, filename, supp_filter=None):

        l_field_data = [None] * len(self.column_headers)
        l_supported_os = []
        l_supported_platform = []
        l_supported_test_env = []

        self.filter_counter.clear()
        for key in supp_filter:
            for name in supp_filter[key]:
                self.filter_counter[name] = 0

        try:
            xml_root = Et.parse(os.path.join(root_path, filename)).getroot()

            # Verify TestSet XML has proper structure (Feature, Test and TestInstance tags).
            basic_feature = xml_root.find(TagNames.feature)
            if basic_feature is None:
                return {'SKIP': "Not a valid command line xml file"}
            if (basic_feature.find(TagNames.test) is None) or (
                        basic_feature.find(TagNames.test).find(TagNames.test_instance) is None):
                return {"FAIL": "Test details and command line **parsing error**"}

            # Index numbers are explicitly hard coded just to make sure appropriate values are assigned.
            l_field_data[0] = 'NA' if len(filename.split('\\')) < 2 else filename.split('\\')[1]
            l_field_data[1] = filename
            with open(self.csv_file_name, 'a') as csv_file:
                feature = xml_root.findall(TagNames.feature)
                for feature_item in feature:
                    l_field_data[2] = feature_item.attrib[TagNames.feature_name]
                    l_field_data[3] = feature_item.attrib[TagNames.feature_owner]
                    # Get "Test" details
                    test = feature_item.findall(TagNames.test)
                    for test_item in test:
                        l_field_data[4] = test_item.attrib[TagNames.test_name]
                        l_field_data[5] = test_item.attrib[TagNames.test_owner]
                        l_field_data[6] = test_item.attrib[TagNames.test_priority]
                        l_field_data[7] = test_item.attrib[TagNames.test_last_modified]
                        l_field_data[8] = test_item.attrib[TagNames.test_version]
                        # Get "Test Instance" details
                        test_instance = test_item.findall(TagNames.test_instance)
                        for test_instance_item in test_instance:
                            l_field_data[9] = test_instance_item.attrib[TagNames.ti_id]
                            l_field_data[10] = test_instance_item.attrib[TagNames.ti_grids]
                            for node in test_instance_item:
                                if node.tag == TagNames.ti_command_line:
                                    # Removing prefix to extract command line
                                    l_field_data[11] = "<{}>".format(node.text.replace('\n', '').strip())
                                if node.tag == TagNames.ti_os:
                                    node_content = node.text.replace('\n', '').strip()
                                    l_field_data[12] = node_content
                                    # Processing Supported OS filter query
                                    l_supported_os = self.get_supported_config(node_content, supp_filter['OS'])
                                if node.tag == TagNames.ti_platform:
                                    node_content = node.text.replace('\n', '').strip()
                                    l_field_data[13] = node_content
                                    # Processing Supported Platform filter query
                                    l_supported_platform = self.get_supported_config(node_content,
                                                                                     supp_filter['Platform'])
                                if node.tag == TagNames.ti_test_environment:
                                    node_content = node.text.replace('\n', '').strip()
                                    l_field_data[14] = node_content
                                    # Processing Supported TestEnvironment filter query
                                    l_supported_test_env = self.get_supported_config(node_content,
                                                                                     supp_filter['TestEnvironment'])
                                if node.tag == TagNames.ti_execution_time:
                                    l_field_data[15] = node.text.replace('\n', '').strip()
                                if node.tag == TagNames.ti_additional_tag:
                                    l_field_data[16] = node.text.replace('\n', '').strip()
                                if node.tag == TagNames.ti_qualification_status:
                                    node_content = node.text.replace('\n', '').strip()
                                    l_field_data[17] = node_content

                            # Write all details to CSV file
                            csv_file.write(",".join(map(lambda x: '"{}"'.format(x), l_field_data[0:18])))
                            csv_file.write(',')
                            if len(l_supported_os) > 0:
                                csv_file.write(",".join(map(lambda x: '{}'.format(x), l_supported_os)))
                                csv_file.write(',')
                            if len(l_supported_platform) > 0:
                                csv_file.write(",".join(map(lambda x: '{}'.format(x), l_supported_platform)))
                                csv_file.write(',')
                            if len(l_supported_test_env) > 0:
                                csv_file.write(",".join(map(lambda x: '{}'.format(x), l_supported_test_env)))
                                csv_file.write(',')
                            csv_file.write('\n')
                            # Clearing current "Test Instance" Data before moving to next "Test Instance"
                            for index in range(9, 18):
                                l_field_data[index] = None
                        # Clear current "Test" Data before moving to next "Test"
                        for index in range(4, 9):
                            l_field_data[index] = None

            if len(self.filter_headers) > 0:
                with open(self.counter_file, 'a') as counter_file:
                    counter_file.write("{},{}".format(file_name, filename.split('\\')[1]))
                    for filter_name in self.filter_headers:
                        counter_file.write(",")
                        counter_file.write(str(self.filter_counter[filter_name]))
                    counter_file.write('\n')

            return {"PASS": "Test Set XML parsing SUCCESS"}
        except xml.etree.ElementTree.ParseError:
            return {"SKIP": "Unable to read xml file"}
        except Exception as ex:
            logging.exception("Exception Filename: {} Line#: {} Message: {}".format(filename,
                                                                                    sys.exc_info()[-1].tb_lineno,
                                                                                    ex))
            return {"FAIL": "Test Set XML parsing FAILED"}

    ##
    # @brief Manipulates Supported OS/Platform content as per query [if requested].
    # @param[in] - String: Original content from TestSet XML file (node_string)
    # @param[in] - List: Supported config filter details (filter_list)
    # @return - List: Supported config as per filer list
    def get_supported_config(self, s_node_data, l_filter):
        if l_filter is not None:
            l_ret_config = ['Not Supported'] * len(l_filter)
        else:
            return []
        if ';' in s_node_data:
            l_config_to_check = s_node_data.split(';')
        else:
            l_config_to_check = [s_node_data]
        try:
            actual_data = [config.upper() for config in l_config_to_check]
            for index in range(0, len(l_filter)):
                for file_content in actual_data:
                    if l_filter[index] == file_content:
                        l_ret_config[index] = "Supported"
                        self.filter_counter[l_filter[index]] += 1
                        break
            return l_ret_config
        except Exception as ex:
            logging.exception("Exception found : {}".format(ex))
            return [None] * len(l_filter)

    ##
    # @brief Retrieves Platform/OS/Branch information provided in Query xml and converts it to Supported List and
    # Qualification list
    # @param[in] - String: Query xml file absolute path (filename)
    # @return - List, Dict: List of Qualification Config Filer and Dict of Supported config filter.
    @staticmethod
    def read_query_xml(filename):
        l_platform = []
        l_os = []
        l_test_env = []
        if not os.path.exists(filename):
            logging.error("Query file not found")
            return None
        try:
            query_file_root = Et.parse(filename).getroot()
            query_handle = query_file_root.findall("Query")
            for query in query_handle:
                platform = query.attrib['Platform'].upper()
                os_name = query.attrib['OS'].upper()
                test_env = query.attrib['TestEnvironment'].upper()
                if platform != 'NA':
                    if platform not in l_platform:
                        l_platform.append(platform.upper())
                if os_name != 'NA':
                    if os_name not in l_os:
                        l_os.append(os_name.upper())
                if test_env != 'NA':
                    l_test_env.append(test_env.upper())

            log_formatter = "Query       : {0:>15} : {1}"
            logging.info(log_formatter.format('Platform', ", ".join(map(lambda x: '{}'.format(x), l_platform))))
            logging.info(log_formatter.format('OS', ", ".join(map(lambda x: '{}'.format(x), l_os))))
            logging.info(log_formatter.format('TestEnvironment', ", ".join(map(lambda x: '{}'.format(x), l_test_env))))

            return {'OS': l_os, 'Platform': l_platform, 'TestEnvironment': l_test_env}
        except Exception as ex:
            logging.exception("Exception Caught while reading Query file : {} Line: {}".format(
                ex, sys.exc_info()[-1].tb_lineno))
            return {'OS': [], 'Platform': [], 'TestEnvironment': []}


##
# This class helps to Update (Convert) output csv file to Test Set XML file.
class UpdateTestDeploymentStatus(object):

    def __init__(self):
        pass

    ##
    # @brief This class method helps to get line from csv file and convert it XML Structure.
    # @param[in] - String: A single line from CSV file.
    # @return    - Bool : True or False and XmlDataStructure : Returns XML file structure.
    @staticmethod
    def process_csv_data(s_csv_line):
        try:
            csv_info = s_csv_line.split(',')
            xml_struct = XmlDataStructure()

            cmd_start = [csv_info.index(i) for i in csv_info if i.startswith('<')][0]
            cmd_index = [csv_info.index(i) for i in csv_info if i.endswith('>')][0]
            cmd_line = ",".join(map(lambda x: '{}'.format(x), csv_info[cmd_start:cmd_index + 1]))

            xml_struct.filename = csv_info[1]
            xml_struct.feature_name = csv_info[2]
            xml_struct.feature_owner = csv_info[3]
            xml_struct.test_name = csv_info[4]
            xml_struct.test_owner = csv_info[5]
            xml_struct.priority = csv_info[6]
            xml_struct.version = csv_info[8]
            xml_struct.last_modified = csv_info[7]
            xml_struct.id = csv_info[9]
            xml_struct.grids = csv_info[10]
            xml_struct.command_line = cmd_line.replace('<', '').replace('>', '')
            xml_struct.os = csv_info[cmd_index + 1]
            xml_struct.platform = csv_info[cmd_index + 2]
            xml_struct.test_environment = csv_info[cmd_index + 3]
            xml_struct.execution_time = csv_info[cmd_index + 4]
            xml_struct.additional_tag = csv_info[cmd_index + 5]
            xml_struct.qualification_status = csv_info[cmd_index + 6]
        except IndexError as ex:
            logging.exception("Invalid Command line data in csv file Message: {}".format(ex))
            return False, None

        return True, xml_struct

    ##
    # @brief This class method helps to convert csv file to xml file.
    # @param[in] - String: CSV file path.
    # @param[in] - String: Binary path where XML files needs to saved.
    # @return    - None.
    def convert_csv_to_xml(self, csv_file, binary_path):
        try:
            csv_content = self.read_csv_file(csv_file)
            for line in csv_content:
                status, parsed_data = self.process_csv_data(line)
                # This checks for empty lines created while deleting a line from Excel
                if status is False:
                    logging.error("CSV content error. Line#: {}".format(csv_content.index(line)+1))
                    continue
                filename = os.path.join(binary_path, parsed_data.filename)
                xml_root = Et.Element(TagNames.da_root)
                if os.path.exists(filename):
                    xml_root = Et.parse(filename).getroot()
                    feature = xml_root.findall(TagNames.feature)
                    avail_feature = [feature_item.attrib[TagNames.feature_name] for feature_item in feature]
                    if (len(avail_feature) == 0) or (parsed_data.feature_name not in avail_feature):
                        feature_ele = Et.SubElement(xml_root, TagNames.feature_name, {
                            TagNames.feature_name: parsed_data.feature_name,
                            TagNames.feature_owner: parsed_data.feature_owner})
                        feature.append(feature_ele)
                    for feature_item in feature:
                        test = []
                        if feature_item.attrib[TagNames.feature_name] == parsed_data.feature_name:
                            feature_item.attrib[TagNames.feature_owner] = parsed_data.feature_owner
                            test = feature_item.findall(TagNames.test)
                            avail_test = [item.attrib[TagNames.test_name] for item in test]
                            if (len(avail_test) == 0) or (parsed_data.test_name not in avail_test):
                                test_ele = Et.SubElement(feature_item, TagNames.test,
                                                         {TagNames.test_name: parsed_data.test_name,
                                                          TagNames.test_owner: parsed_data.test_owner,
                                                          TagNames.test_priority: parsed_data.priority,
                                                          TagNames.test_version: parsed_data.version,
                                                          TagNames.test_last_modified: parsed_data.last_modified})
                                test.append(test_ele)
                        for test_item in test:
                            if test_item.attrib[TagNames.test_name] == parsed_data.test_name:
                                test_item.attrib[TagNames.test_owner] = parsed_data.test_owner
                                test_item.attrib[TagNames.test_priority] = parsed_data.priority
                                test_item.attrib[TagNames.test_version] = parsed_data.version
                                test_item.attrib[TagNames.test_last_modified] = parsed_data.last_modified
                                test_instance = test_item.findall(TagNames.test_instance)
                                avail_test_instance = [item.attrib[TagNames.ti_id] for item in test_instance]
                                if (len(avail_test_instance) == 0) or (parsed_data.id not in avail_test_instance):
                                    test_instance.append(self.add_test_instance_node(xml_tag=test_item,
                                                                                     xml_structure=parsed_data))
                                for test_instance_item in test_instance:
                                    if test_instance_item.attrib[TagNames.ti_id] == parsed_data.id:
                                        test_instance_item.attrib[TagNames.ti_grids] = parsed_data.grids
                                        for node in test_instance_item:
                                            if node.tag == TagNames.ti_command_line:
                                                node.text = parsed_data.command_line
                                            if node.tag == TagNames.ti_os:
                                                node.text = parsed_data.os
                                            if node.tag == TagNames.ti_platform:
                                                node.text = parsed_data.platform
                                            if node.tag == TagNames.ti_test_environment:
                                                node.text = parsed_data.test_environment
                                            if node.tag == TagNames.ti_execution_time:
                                                node.text = parsed_data.execution_time
                                            if node.tag == TagNames.ti_additional_tag:
                                                node.text = parsed_data.additional_tag
                                            if node.tag == TagNames.ti_qualification_status:
                                                node.text = parsed_data.qualification_status
                else:
                    feature = Et.SubElement(xml_root, TagNames.feature, {
                        TagNames.feature_name: parsed_data.feature_name,
                        TagNames.feature_owner: parsed_data.feature_owner})
                    test = Et.SubElement(feature, TagNames.test,
                                         {TagNames.test_name: parsed_data.test_name,
                                          TagNames.test_owner: parsed_data.test_owner,
                                          TagNames.test_priority: parsed_data.priority,
                                          TagNames.test_version: parsed_data.version,
                                          TagNames.test_last_modified: parsed_data.last_modified})
                    self.add_test_instance_node(xml_tag=test, xml_structure=parsed_data)
                tree = Et.ElementTree(self.format_xml_file(xml_root))
                tree.write(file_or_filename=filename, xml_declaration=True, encoding="UTF-8", method='xml')
                logging.info("PASS : Filename: {0} ID:{1} updated successfully".format(parsed_data.filename,
                                                                                       parsed_data.id))
        except Exception as convert_csv_exception:
            message = "Exception Found = Line#: {} Message: {}".format(sys.exc_info()[-1].tb_lineno,
                                                                       convert_csv_exception)
            logging.exception(message)

    ##
    # @brief This class method helps to add test instance module to xml file handle.
    # @param[in] - XML tag handle: Master XML tag's handle where test instance need to be added.
    # @param[in] - XmlDataStructure: XML structure to pick test instance details.
    # @return    - XML tag handle. Returns TestInstance Tag handle.
    @staticmethod
    def add_test_instance_node(xml_tag, xml_structure):
        test_instance = Et.SubElement(xml_tag, TagNames.test_instance, {TagNames.ti_id: xml_structure.id,
                                                                        TagNames.ti_grids: xml_structure.grids})
        Et.SubElement(test_instance, TagNames.ti_command_line).text = xml_structure.command_line
        Et.SubElement(test_instance, TagNames.ti_os).text = xml_structure.os
        Et.SubElement(test_instance, TagNames.ti_platform).text = xml_structure.platform
        Et.SubElement(test_instance, TagNames.ti_test_environment).text = xml_structure.test_environment
        Et.SubElement(test_instance, TagNames.ti_execution_time).text = xml_structure.execution_time
        Et.SubElement(test_instance, TagNames.ti_additional_tag).text = xml_structure.additional_tag
        Et.SubElement(test_instance, TagNames.ti_qualification_status).text = xml_structure.qualification_status
        return test_instance

    ##
    # @brief This class method helps to read csv file and convert it list.
    # @param[in] - String: CSV file with path.
    # @return    - List: Returns csv content as list.
    @staticmethod
    def read_csv_file(input_csv_file):
        try:
            csv_out_data = []
            with open(input_csv_file, 'r') as input_handle:
                csv_content = input_handle.readlines()
                # Delete Binary Version and Tile bar from CSV file
                del csv_content[:2]
            for lin in csv_content:
                csv_out_data.append(lin.replace('\n', '').replace('"', ''))
            return csv_out_data
        except Exception as ex:
            logging.exception("Exception Found = Line#: {} Message: {}".format(sys.exc_info()[-1].tb_lineno,
                                                                               ex))
            return []

    ##
    # @brief This class method helps to format xml file to readable format on Text editors.
    # @param[in] - XML root handle: XML file root handle.
    # @return    - XML root handle: Returns Formatted XML as XML root handle.
    @staticmethod
    def format_xml_file(xml_root):
        new_line = '\n'
        tab_space = ' ' * 4
        xml_root.text = new_line + tab_space
        xml_root.tail = new_line
        feature = xml_root.findall(TagNames.feature)
        for feature_item in feature:
            feature_item.text = new_line + (tab_space * 2)
            feature_item.tail = new_line
            test = feature_item.findall(TagNames.test)
            for test_item in test:
                test_item.text = new_line + (tab_space * 3)
                value = 2 if test_item != test[-1] else 1
                test_item.tail = new_line + (tab_space * value)
                test_instance = test_item.findall(TagNames.test_instance)
                for test_instance_item in test_instance:
                    test_instance_item.text = new_line + (tab_space * 4)
                    value = 2 if test_instance_item == test_instance[-1] else 3
                    test_instance_item.tail = new_line + (tab_space * value)
                    for node in test_instance_item:
                        value = 3 if node.tag == TagNames.ti_qualification_status else 4
                        node.tail = new_line + (tab_space * value)
        return xml_root


if __name__ == '__main__':

    # Initiate and Declare logging file handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)-s:%(msecs)-03d - %(levelname)-09s : %(message)s', "%d-%m-%Y %H:%M:%S")

    # Handler for logging information to log file
    file_handler = logging.FileHandler('test_deployment_status.log', mode='w')
    file_handler.setFormatter(formatter)

    # Handler for logging information to command console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    root_logger.addHandler(consoleHandler)
    root_logger.addHandler(file_handler)

    # Log file format definition
    log_msg_formatter = "{type:^8}:{keymsg:<35}:{slno:^6}:{timestamp:^25}: {value}"
    log_title_formatter = "{type:^8}|{keymsg:^35}|{slno:^6}|{timestamp:^25}| {value}"

    # Configure Commandline parameters
    parser = argparse.ArgumentParser(description="Test Manager helps to manipulate TestSet files between XML and CSV.")
    parser.add_argument("--ACTION", "-a", choices=('DUMP', 'UPDATE'), required=True, type=str.upper,
                        help="Provide action to DUMP | UPDATE", dest='action')
    parser.add_argument("--PATH", "-p", help="Provide binary/xml file path", dest='path', type=str.upper, default=None)
    parser.add_argument("--XML", "-x", help="Provide filter xml file", dest='xml', type=str.upper, default=None)
    parser.add_argument("--CSV", "-c", help="Provide output csv file", dest='csv', type=str.upper, default=None)
    user_arguments = parser.parse_args()

    # Set one level above cwd as default path. If PATH argument is not parsed through command line.
    if user_arguments.path is None:
        current_dir = os.getcwd()
        user_arguments.path = os.path.dirname(current_dir) if current_dir.endswith("TestManager") else current_dir

    supp_config_filter = {'OS': [], 'Platform': [], 'TestEnvironment': []}

    logging.info("Command Line: {0}".format(" ".join(map(lambda x: '{}'.format(x), sys.argv))))
    logging.info("Binary Path : {0}".format(user_arguments.path))

    if user_arguments.action == "UPDATE":
        update_testset = UpdateTestDeploymentStatus()
        update_testset.convert_csv_to_xml(user_arguments.csv, user_arguments.path)
    else:
        status_counter = {'PASS': 0, 'FAIL': 0, 'SKIP': 0}
        get_status = DumpTestDeploymentStatus()
        if user_arguments.xml is not None:
            supp_config_filter = get_status.read_query_xml(user_arguments.xml)

        # Create CSV file with Header details
        get_status.add_binary_version_and_csv_header(user_arguments.path, supp_config_filter)
        counter = 0
        logging.info("{0}".format('*' * 160))
        logging.info(log_title_formatter.format(type="Status", keymsg="Result Message", value="XML File Name",
                                                slno="S.No", timestamp="XML TimeStamp"))
        logging.info("{0}".format('*' * 160))

        # Scan for all TestSet xml files and manipulated to csv
        for root, dirs, files in os.walk(user_arguments.path):
            for file_name in files:
                if file_name.startswith('TestSet_') and file_name.endswith('.xml'):
                    counter += 1
                    xml_file = os.path.join(root, file_name)
                    trimmed_filename = xml_file.replace(user_arguments.path + '\\', '')
                    mod_time = time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(os.path.getmtime(xml_file)))
                    d_result = get_status.read_xml(root_path=user_arguments.path, filename=trimmed_filename,
                                                   supp_filter=supp_config_filter)

                    if list(d_result)[0] == "PASS":
                        status_counter['PASS'] += 1
                        logging.info(log_msg_formatter.format(type="PASS", keymsg=d_result['PASS'],
                                                              slno="{:02}".format(counter),
                                                              value=trimmed_filename, timestamp=mod_time))
                    elif list(d_result)[0] == "FAIL":
                        status_counter['FAIL'] += 1
                        logging.error(log_msg_formatter.format(type="FAIL", keymsg=d_result['FAIL'],
                                                               slno="{:02}".format(counter),
                                                               value=trimmed_filename, timestamp=mod_time))
                    elif list(d_result)[0] == "SKIP":
                        status_counter['SKIP'] += 1
                        logging.warning(log_msg_formatter.format(type="SKIP", keymsg=d_result['SKIP'],
                                                                 slno="{:02}".format(counter),
                                                                 value=trimmed_filename, timestamp=mod_time))

        logging.info("{0}Test Summary{0}".format(('*' * 22)))
        logging.info("Total Pass : {:02}".format(status_counter['PASS']))
        logging.info("Total Fail : {:02}".format(status_counter['FAIL']))
        logging.info("Total Skip : {:02}".format(status_counter['SKIP']))
        logging.info("==================")
        logging.info("Total      : {:02}".format(counter))
        logging.info("==================")
        logging.info("{0}END{0}".format(('*' * 26)))
