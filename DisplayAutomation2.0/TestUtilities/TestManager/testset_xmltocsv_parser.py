########################################################################################################################
# \file         testset_xmltocsv_parser.py
# \addtogroup   PyTools_TestSetXmlToCsv
# \brief        This Utility scans all the valid "<TestSet>.xml" files present in Automation 2.0 framework and converts
#               test details or command line tags present in <TestSet>.xml to .csv file format (Which can be used
#               for test management).
# \remarks
#   Utility Reports :
#       PASS : If Test Details and Command line Parsing is Successful.
#       SKIP : If .xml files contains data other than test / command line details.
#               (Example : DELL_UP3216Q_HDMI.xml - which is test specific data)
#       FAIL : If Required Test Details and Command line parameter are missing.
#
#   Valid TestSet.xml Field are:
#   <Display_Automation_2.0>
#       <Feature Name="" Owner="">
#           <Test Name="" Owner="" Priority="" LastModifiedWW="2017.WW24" Version="1">
#               <TestInstance InstanceUniqueId="1" Grids="ETM;PreETM;CI" >
#                   <CommandLine>python </CommandLine>
#                   <OS>WinTH2;WinRS1;WinRS2</OS>
#                   <Platform>ICL</Platform>
#                   <QualificationStatus>ICL_WinRS2_15.40</QualificationStatus>
#               </TestInstance>
#           </Test>
#       </Feature>
#   </Display_Automation_2.0>
#
# \author       Balaji Gurusamy
#   Date    : WW30.2
#   Rev     : 1
########################################################################################################################
import os
import logging
import xml
import xml.etree.ElementTree as Et


class TestSetXmlToCsv:

    def __init__(self):
        self.csv_file_name = 'TestSet_XMLtoCSV_Parser_Output.csv'
        self.column_headers = ['Feature Name', 'Feature Owner', 'Test Name', 'Test Owner', 'Priority', 'LastModifiedWW',
                               'Version', 'Id', 'Grids', 'CommandLine', 'OS', 'Platform',
                               'QualificationStatus']

    def add_autobinary_version_and_csvheader(self, auto_binary_path):
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
            logging.info("Get automation binary version success")

        # Write Binary Version and Header details to CSV file
        with open(self.csv_file_name, 'a') as csvfile_handle:
            csvfile_handle.write("DisplayAutomation Version,{}".format(ver_details))
            csvfile_handle.write('\n')
            csvfile_handle.write(",".join(map(lambda x: '"{}"'.format(x), self.column_headers)))
            csvfile_handle.write('\n')

    def read_xml(self, filename):

        field_data = [None] * len(self.column_headers)
        try:
            xml_root = Et.parse(filename).getroot()

            # Verify TestSet XML has proper structure (Feature, Test and TestInstance tags).
            basic_feature = xml_root.find('Feature')
            if basic_feature is None:
                logging.warning("%(type)-5s : %(keymsg)-50s : %(value)s" %
                                {'type': "SKIP", 'keymsg': "Not a valid command line xml file", 'value': filename})
                return
            if (basic_feature.find('Test') is None) or (basic_feature.find('Test').find('TestInstance') is None):
                logging.error("%(type)-5s : %(keymsg)-50s : %(value)s" %
                              {'type': "FAIL", 'keymsg': "Test details and command line **parsing error**",
                               'value': filename})
                return

            # Index numbers are explicitly hard coded just to make sure appropriate values are assigned.
            with open(self.csv_file_name, 'a') as csv_file:
                feature = xml_root.findall('Feature')
                for feature_item in feature:
                    field_data[0] = feature_item.attrib['Name']
                    field_data[1] = feature_item.attrib['Owner']
                    # Get "Test" details
                    test = feature_item.findall('Test')
                    for test_item in test:
                        field_data[2] = test_item.attrib['Name']
                        field_data[3] = test_item.attrib['Owner']
                        field_data[4] = test_item.attrib['Priority']
                        field_data[5] = test_item.attrib['LastModifiedWW']
                        field_data[6] = test_item.attrib['Version']
                        # Get "Test Instance" details
                        test_instance = test_item.findall('TestInstance')
                        for test_instance_item in test_instance:
                            field_data[7] = test_instance_item.attrib['Id']
                            field_data[8] = test_instance_item.attrib['Grids']
                            for node in test_instance_item:
                                if node.tag == 'CommandLine':
                                    # Removing prefix to extract command line
                                    field_data[9] = node.text.strip('python ')
                                if node.tag == 'OS':
                                    field_data[10] = node.text
                                if node.tag == 'Platform':
                                    field_data[11] = node.text
                                if node.tag == 'QualificationStatus':
                                    field_data[12] = node.text
                            # Write all details to CSV file
                            csv_file.write(",".join(map(lambda x: '"{}"'.format(x), field_data)))
                            csv_file.write('\n')
                            # Clearing current "Test Instance" Data before moving to next "Test Instance"
                            for index in range(7, 13):
                                field_data[index] = None
                        # Clear current "Test" Data before moving to next "Test"
                        for index in range(2, 7):
                            field_data[index] = None
            logging.info("%(type)-5s : %(keymsg)-50s : %(value)s" %
                         {'type': "PASS", 'keymsg': "Test details and command line parsing success",
                          'value': filename})
        except xml.etree.ElementTree.ParseError:
            logging.warning("%(type)-5s : %(keymsg)-50s : %(value)s" %
                            {'type': "SKIP", 'keymsg': "Unable to read xml file",
                             'value': filename})
        except Exception as ex:
            logging.error("%(type)-5s : %(keymsg)-50s : %(value)s" %
                          {'type': "FAIL", 'keymsg': "Test details and command line **parsing error**",
                           'value': file_name})
            print("Exception Caught : ", filename)
            print(ex)

if __name__ == '__main__':
    # Logging File Handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)-s:%(msecs)-03d - %(levelname)-09s : %(message)s', "%d-%m-%Y %H:%M:%S")
    file_handler = logging.FileHandler('testset_xmltocsv_parser.log', mode='w')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Get Automation Framework Binary path from user
    binary_path = input("Please enter DisplayAutomation binary Path: ")

    class_obj = TestSetXmlToCsv()

    if os.path.exists(binary_path):
        # Create CSV file with Header details
        class_obj.add_autobinary_version_and_csvheader(binary_path)
        for root, dirs, files in os.walk(binary_path):
            for file_name in files:
                if file_name.startswith('TestSet_') and file_name.endswith('.xml'):
                    xml_file = os.path.join(root, file_name)
                    class_obj.read_xml(filename=xml_file)
    else:
        logging.error("Invalid binary path specified")
