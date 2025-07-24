###################################################################################################################
# @file         parser.py
# @addtogroup   NorthGate
# @brief        Contains APIs to get data from TestSet XML files
# @description  @ref parser.py file contains the basic functions required to get data from TestSet XML files. Below
#               APIs are exposed in this file:
#               1. get_gta_platforms()      Returns a list of platforms present in XML files
#               2. get_gta_os()             Returns a list of OS
#               3. get_gta_grids()          Returns a list of grids
#               4. get_gta_tests()          Returns a list of tests based on inputs
#               5. get_features()           Returns a list of features
#               6. get_sub_features()       Returns a list of sub features
#               7. get_tests()              Returns a list of tests
#
# @author       Rohit Kumar
###################################################################################################################

import os
import xml.etree.ElementTree as elementTree

__MANUAL_TESTS_ROOT = "Tests"  # Root folder to search XML files
__MANUAL_TESTS_XML_PREFIX = "ManualTestSet"  # XML file name prefix

__manual_test_set_xml_files = []
__dev_test_set = {}
__gta_test_set = {}

##
# Get all ManualTestSet XML files
for path, sub_dirs, files in os.walk(__MANUAL_TESTS_ROOT):
    for name in files:
        if __MANUAL_TESTS_XML_PREFIX in name and ".xml" in name:
            __manual_test_set_xml_files.append(os.path.join(path, name))

counter = 0
for manual_test_set_xml in __manual_test_set_xml_files:
    try:
        tree = elementTree.parse(manual_test_set_xml)
    except Exception as e:
        print(e)
        continue

    root = tree.getroot()
    for feature in root:
        __dev_test_set[feature.attrib['Name']] = feature.attrib
        __dev_test_set[feature.attrib['Name']]['sub_features'] = {}
        for sub_feature in feature:
            sub_feature.attrib['tests'] = {}
            for test in sub_feature:
                temp = {'Owner': sub_feature.attrib['Owner']}
                for info in test:
                    temp[info.tag] = info.text
                temp.update(test.attrib)
                sub_feature.attrib['tests'][str(counter) + temp['Id']] = temp
                counter += 1
                if 'Platform' in temp.keys():
                    platforms = temp['Platform'].split(';')
                    for p in platforms:
                        if p not in __gta_test_set.keys():
                            __gta_test_set[p] = {'tests': {}, 'os': {}, 'grids': {}}
                        __gta_test_set[p]['tests'][str(counter) + test.attrib['Id']] = temp
                        counter += 1
                        if 'OS' in temp.keys():
                            os_list = temp['OS'].split(';')
                            for _os in os_list:
                                if _os not in __gta_test_set[p]['os'].keys():
                                    __gta_test_set[p]['os'][_os] = {'tests': {}, 'grids': {}}
                                __gta_test_set[p]['os'][_os]['tests'][str(counter) + test.attrib['Id']] = temp
                                counter += 1
                                if 'Grids' in test.attrib.keys():
                                    grids = test.attrib['Grids'].split(';')
                                    for grid in grids:
                                        if grid not in __gta_test_set[p]['os'][_os]['grids'].keys():
                                            __gta_test_set[p]['os'][_os]['grids'][grid] = {}
                                        __gta_test_set[p]['os'][_os]['grids'][grid][str(counter) + test.attrib['Id']] \
                                            = temp
                                        counter += 1
                        if 'Grids' in test.attrib.keys():
                            grids = test.attrib['Grids'].split(';')
                            for grid in grids:
                                if grid not in __gta_test_set[p]['grids'].keys():
                                    __gta_test_set[p]['grids'][grid] = {}
                                __gta_test_set[p]['grids'][grid][str(counter) + test.attrib['Id']] = temp
                                counter += 1
            __dev_test_set[feature.attrib['Name']]['sub_features'][sub_feature.attrib['Name']] = sub_feature.attrib


##
# @brief        Exposed API to get a list of platforms present in XML
def get_gta_platforms():
    return list(__gta_test_set.keys())


##
# @brief        Exposed API to get a list of os based on target platform
# @param[in]    target_platform
def get_gta_os(target_platform):
    if target_platform in __gta_test_set.keys():
        return list(__gta_test_set[target_platform]['os'].keys())
    return []


##
# @brief        Exposed API to get a list of grids based on target platform and target os
# @param[in]    target_platform
# @param[in]    target_os
def get_gta_grids(target_platform, target_os):
    if target_platform in __gta_test_set.keys():
        if target_os in __gta_test_set[target_platform]['os'].keys():
            return list(__gta_test_set[target_platform]['os'][target_os]['grids'].keys())
    return []


##
# @brief        Exposed API to get a list of os based on target platform, os and grid
# @param[in]    target_platform
# @param[in]    target_os
# @param[in]    target_grid
def get_gta_tests(target_platform, target_os=None, target_grid=None):
    if target_platform in __gta_test_set.keys():
        if target_os is not None:
            if target_os in __gta_test_set[target_platform]['os'].keys():
                if target_grid is not None:
                    if target_grid in __gta_test_set[target_platform]['os'][target_os]['grids'].keys():
                        return __gta_test_set[target_platform]['os'][target_os]['grids'][target_grid]
                else:
                    return __gta_test_set[target_platform]['os'][target_os]['tests']
        else:
            return __gta_test_set[target_platform]['tests']
    return {}


##
# @brief        Exposed API to get a list of features
def get_features():
    return list(__dev_test_set.keys())


##
# @brief        Exposed API to get a list of sub features based on target feature
# @param[in]    target_feature
def get_sub_features(target_feature):
    if target_feature in __dev_test_set.keys():
        return list(__gta_test_set[target_feature]['sub_features'].keys())
    return []


##
# @brief        Exposed API to get a list of test cases based on feature and sub feature
# @param[in]    target_feature
# @param[in]    target_sub_feature
# @todo         Implement this API for features view
def get_tests(target_feature, target_sub_feature):
    pass
