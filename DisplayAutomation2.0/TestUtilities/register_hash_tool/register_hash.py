#####################################################################################################################################
# \file        register_hahs.py
# \addtogroup  PyLibs_Utils
# \brief       Interface for capturing and comparing registers' state
# \author      Gopal Beeresh, agolwala
#####################################################################################################################################

import hashlib
import json
from win32api import *
import logging
import re
import xml.etree.ElementTree as ET

from Libs.Core.system_utility import *
from Libs.Core.display_config.display_config import *
from Libs.Core.winkb_helper import *

HW_REGISTER_XML_FILE = r'Libs\utils\DisplaySequence.xml'
HW_REGISTER_BUCKET_CSV_FILE = r'Libs\utils\DisplaySequence_Buckets.csv'
HW_REGISETR_DEFINITION_JSON_FILE = r'Libs\utils\DisplaySequence.json'


##
# Class to store meta data of registers
class HWRegister(object):
    def __init__(self):
        self.key = None
        self.offset = None
        self.offset_name = None
        self.value = 0
        self.hash = None

    def __str__(self):
        ret_val = ("%s  %s  [%s] : %s" % (self.key, self.offset_name, self.offset, self.value))
        return ret_val

    def to_csv(self):
        ret_val = ("%s,%s,%s,%s" % (self.key, self.offset_name, self.offset, self.value))
        return ret_val

    ##
    # @brief Helper function read value of offset
    #
    # @param[in] offset to be read
    # @return offset value
    @staticmethod
    def read(offset):
        offset = int(offset, 16)
        reg_val = driver_interface.DriverInterface().mmio_read(offset, 'gfx_0')
        if reg_val is not None:
            return reg_val
        else:
            logging.error("offset %s value is None", offset)
            return 0


class HwRegisterBucket(object):
    key = None
    key_hash = None
    exclude = None  ## if value is "Y", then only that bucket will be considered for comparison.
    register_offset_list = None
    register_value_hash = None
    register_offset_name_hash = None
    register_value = 0

    ## 
    # helper function to get offsets' hash of all registers in given list
    def get_offsets_hash(self):
        reg_offset = ''
        for reg in self.register_offset_list:
            reg_offset = reg_offset + reg.offset_name + "|"

        reg_offset = reg_offset[:-1]
        hash_key = hashlib.md5(reg_offset)
        self.register_offset_name_hash = hash_key.hexdigest()

    ##
    # helper function to get redisters' value hash for registers in given list
    def read(self):
        reg_values = ''

        reg_offset_names = ''
        for reg in self.register_offset_list:
            offset = reg.offset
            reg_values = reg_values + hex(HWRegister.read(offset)) + "|"
            reg_offset_names = reg_offset_names + reg.offset_name + "|"

        hash_key = hashlib.md5(reg_values)
        self.register_value_hash = hash_key.hexdigest()
        self.register_value = reg_values
        self.get_offsets_hash()
        return self.register_value, self.register_value_hash


class HwRegisterBucketCollection(object):
    bucket_file = None
    active_bucket_list = list()
    inactive_bucket_list = list()

    def __init__(self, registers_bucket_csv, register_json_file):
        json_manager = HwRegisterJsonManager(HW_REGISTER_XML_FILE)
        register_list = json_manager.load_from_json_file(register_json_file, HWRegister)

        with open(registers_bucket_csv, 'r') as input_file:
            self.bucket_file = registers_bucket_csv
            for line in input_file:
                words = line.split(",")

                reg_bucket = HwRegisterBucket()
                reg_bucket.key = words[0]
                reg_bucket.key_hash = words[1]
                reg_bucket.exclude = words[2]
                register_offset_list = words[3].split("|")
                reg_bucket.register_offset_list = list()

                for offset_name in register_offset_list:
                    offset_name = offset_name.replace("\n", "")
                    found = False
                    for reg in register_list:
                        if offset_name == reg.offset_name:
                            reg_bucket.register_offset_list.append(reg)
                            found = True

                    if not found:
                        logging.error("OOPs register details not found", offset_name)

                if reg_bucket.exclude == "N":
                    self.active_bucket_list.append(reg_bucket)
                else:
                    self.inactive_bucket_list.append(reg_bucket)

    ##
    # @brief Helper function to capture register's state
    #
    # @param[in] csv file to store registers' state
    def capture(self, filename):
        bucket_hash = ''
        with open(filename, 'w') as csv_write:
            for reg_bucket in self.active_bucket_list:
                reg_offset_val, active_bucket_hash = reg_bucket.read()
                bucket_hash = bucket_hash + active_bucket_hash + "|"
                reg_offset_names = '|'.join([reg.offset_name for reg in reg_bucket.register_offset_list])
                line = ("%s, %s, %s, %s, %s" % (
                    reg_bucket.key, reg_offset_names, reg_offset_val, reg_bucket.register_offset_name_hash,
                    reg_bucket.register_value_hash))
                csv_write.write(line)
                csv_write.write("\n")

        hash_key = hashlib.md5(bucket_hash)
        return hash_key.hexdigest()

    ##
    # @brief Helper function to create buckets of registers based on key
    #
    # @param[in] json_file - contains registers' json objects
    # @param[in] bucket_file - to store registers' bucket
    @staticmethod
    def bucketize(json_file, bucket_file):
        obj = HwRegisterJsonManager(HW_REGISTER_XML_FILE)
        register_list = obj.load_from_json_file(json_file, HWRegister)

        bucket_dict = dict()

        if len(register_list) == 0:
            return bucket_dict

        key = register_list[0].key
        bucket_dict[key] = list()

        if len(register_list) == 1:
            bucket_dict[key] = register_list[0]
            return bucket_dict

        previous_key = key
        for idx in range(1, len(register_list)):
            current_obj = register_list[idx - 1]
            current_key = current_obj.key
            if current_key != previous_key:
                previous_key = current_key
                bucket_dict[current_key] = list()
            bucket_dict[current_key].append(current_obj)

        fd = open(bucket_file, "w")
        for key, reg_list in sorted(bucket_dict.items(), key=lambda k, v: (v, k)):
            offset_names = ""
            for reg_obj in reg_list:
                offset_names += reg_obj.offset_name + "|"

            offset_names = offset_names[:-1]
            hash_key = hashlib.md5(offset_names)
            fd.write(key)
            fd.write(",")

            fd.write(hash_key.hexdigest())
            fd.write(",")
            fd.write("N")
            fd.write(",")
            fd.write(offset_names)
            fd.write("\n")
        fd.close()


class HwRegisterJsonManager(object):
    def __init__(self, display_sequence_xml):
        self.input_xml_file = display_sequence_xml

    ##
    # Creates object of type HWRegister for all registers stored in xml file and returns list of registers of type HWRegister
    def deserialize_from_xml(self):
        with open(self.input_xml_file, 'r') as xml_file:
            registers = list()
            xml = xml_file.read()
            tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
            root = tree.findall("BspecSequence")

        for root_element in root:
            seq_reg = root_element.findall("SeqRegisters")
            for seq_reg_element in seq_reg:
                reg = seq_reg_element.findall("register")
                for reg_element in reg:
                    reg_name = reg_element.get('name')
                    address_list = reg_element.findall("AddressList")
                    for address_list_element in address_list:
                        address = address_list_element.findall("Address")
                        for address_element in address:
                            hw_reg = HWRegister()
                            hw_reg.key = reg_name
                            hw_reg.offset = address_element.get('Offset')
                            hw_reg.offset_name = address_element.get('Symbol')
                            registers.append(hw_reg)
        return registers

    ##
    # Encodes objects to json objects
    def encode_to_json(self, object_list, output_file):
        json_string = json.dumps([obj.__dict__ for obj in object_list])
        with open(output_file, "w") as json_file:
            json_file.write(json_string)

    ##
    # Creates DisplaySequence.json file from xml file
    def convert_to_json(self, json_output_file):
        self.register_list = self.deserialize_from_xml()
        self.encode_to_json(self.register_list, json_output_file)

    ##
    # Using given json file, it will create list of dictionary of type class_type
    def load_from_json_file(self, json_input_file, class_type):
        json_file = open(json_input_file, "r")
        json_object_list = json.load(json_file)
        hw_register_list = list()

        for json_dict in json_object_list:
            # dynamically instantiate the object from class type
            instance = class_type()
            for key, value in json_dict.items():
                instance.__setattr__(key, value)
            hw_register_list.append(instance)

        json_file.close()

        return hw_register_list

    ##
    # Writes all registers to register_list.csv file
    def export_to_csv(self, output_file=None):
        ##
        # Sorting registers by key
        register_list = self.deserialize_from_xml()
        output = register_list.sort(key=lambda c: c.key)

        if output_file is None:
            output_file = r'register_list.csv'

        with open(output_file, 'w') as register_file:
            for reg in register_list:
                register_file.write(reg.to_csv())
                register_file.write("\n")


##
# @brief Helper function to generate json and bucket file from xml file
#
# @param[in] xml_file_path - Reference xml which contains registers' defination
# @param[in] register_json_file - to store registers' json objects
# @param[in] xml_file_path - of csv type to store registers' bucket
def generate_meta_files(xml_file_path, register_json_file, bucket_definition_file):
    hw_reg_json_manager = HwRegisterJsonManager(xml_file_path)
    hw_reg_json_manager.convert_to_json(register_json_file)

    # Use can modify this file to filter unwanted registers
    HwRegisterBucketCollection.bucketize(register_json_file, HW_REGISTER_BUCKET_CSV_FILE)


##
# @brief Helper function to capture hash value for each bucket
#
# @param[in] output_file - is of type csv provided by user. Registers' state will be written in this file.
def capure_reg_hash(output_file):
    bucket_collection = HwRegisterBucketCollection(HW_REGISTER_BUCKET_CSV_FILE, HW_REGISETR_DEFINITION_JSON_FILE)

    display_state_reg_hash = bucket_collection.capture(output_file)
    logging.info("Hash of all registers %s", display_state_reg_hash)


##
# @brief Helper function to compare two csv files having registers' state
#
# @param[in] file1, file2 - of type csv
# @return true if difference is found
def reg_hash_comparison(file1, file2):
    ret_val = False
    file1_path, file1_name = os.path.split(file1)
    file2_path, file2_name = os.path.split(file2)

    result_file_name = 'comparison_result.json'
    bucketcollection = HwRegisterBucketCollection(HW_REGISTER_BUCKET_CSV_FILE, HW_REGISETR_DEFINITION_JSON_FILE)

    obj = HwRegisterJsonManager(HW_REGISTER_XML_FILE)
    register_data = obj.load_from_json_file(HW_REGISETR_DEFINITION_JSON_FILE, HWRegister)

    with open(result_file_name, "w") as json_file:
        with open(file1, 'r') as reg_hash1, open(file2, 'r') as reg_hash2:
            reg_hash1_line = reg_hash1.readlines()
            reg_hash2_line = reg_hash2.readlines()

        for line_in_file1 in reg_hash1_line:
            words_in_file1 = line_in_file1.split(",")
            key_in_file1 = words_in_file1[0]
            reg_value_hash_in_file1 = words_in_file1[4]
            found = False

            for line_in_file2 in reg_hash2_line:
                if not found:
                    words_in_file2 = line_in_file2.split(",")
                    key_in_file2 = words_in_file2[0]

                    if key_in_file2 == key_in_file1:
                        found = True
                        reg_value_hash_in_file2 = words_in_file2[4]

                        if reg_value_hash_in_file1 != reg_value_hash_in_file2:
                            words_in_file1[1] = words_in_file1[1].strip()
                            offset_names_in_file1 = words_in_file1[1].split("|")
                            offset_values_in_file1 = words_in_file1[2].split("|")
                            offset_values_in_file2 = words_in_file2[2].split("|")

                            for index in range(len(offset_values_in_file1)):
                                if offset_values_in_file1[index] != offset_values_in_file2[index]:
                                    ret_val = True
                                    data = dict()
                                    data['key'] = key_in_file1
                                    data['offset_name'] = offset_names_in_file1[index]
                                    data['offset'] = 0x0
                                    for json_obj in register_data:
                                        if json_obj.offset_name == data['offset_name']:
                                            data['offset'] = json_obj.offset
                                            break
                                            # logging.error("Register instance not found for %s" % (data['offset_name']))

                                    data[file1_name] = offset_values_in_file1[index]
                                    data[file2_name] = offset_values_in_file2[index]

                                    json_data = json.dumps(data)
                                    json_file.write(json_data)
                                    json_file.write("\n")

    return ret_val


if __name__ == "__main__":
    logging.basicConfig(filename='register_hash.log', level=logging.DEBUG, filemode='w')

    '''
    Generate JSON and RegisterBucket CSV file.
    This is one time call only when registers' defination is changed in xml.
    '''

    # generate_meta_files(HW_REGISTER_XML_FILE, HW_REGISETR_DEFINITION_JSON_FILE, HW_REGISTER_BUCKET_CSV_FILE)

    '''ULT to capture register hash'''
    reg_hash_file_before_test = r'reg_hash_output_before_test.csv'
    capure_reg_hash(reg_hash_file_before_test)

    reg_hash_file_after_test = r'reg_hash_output_after_test.csv'
    capure_reg_hash(reg_hash_file_after_test)

    '''ULT to compare register hash'''
    ret_val = reg_hash_comparison(reg_hash_file_before_test, reg_hash_file_after_test)
    if ret_val:
        logging.info(
            "Registers' state is not same before and after mode set. Please check 'comparison_result.json' to get list of registers differ in both files")
