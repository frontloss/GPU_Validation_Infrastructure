############################################################################################################
# @file
# @addtogroup PyLibs_Bspec_Transcoder
# @brief Python script that generates respective ctype structure to access the register. 
# @remarks
#       The input to the script will be folder path for BSPEC XML files. 
#       BSCPEC xml files can be checked out from SVN repo [https://fmsgfxauto.amr.corp.intel.com/svn/BSpec/branches/BSpecLiveBeta/BXml/Display/Display/]
#
# @attention Do not modify this wrapper without consent from the author.
# @author Beeresh
############################################################################################################


import os, sys, traceback
import collections
import xml.etree.ElementTree as ET
import logging
import argparse
import re

GEN_VERSION = "GEN9"
GEN_PATTERN = re.compile(r"GEN[0-9]{1,2}")
HAS_ADD_PATTERN = re.compile(r'GEN[0-9]{1,2}:HAS:[0-9]{1,10}')
HAS_REMOVE_PATTERN = re.compile(r'REMOVEDBY\(GEN[0-9]{1,2}:HAS:[0-9]{1,10}')


def cleanup_xml_constant_name(key):
    '''
    Perform cleanup on field constant names to be valid python literals
    '''
    key = key.replace("-", "_")
    key = key.replace(".", "_")
    key = key.replace("/", "_")
    key = key.replace(",", "_")

    invalid_char = ['-', '_', '*']
    for idx in range(0, 9):
        invalid_char.append(idx)

    for char in invalid_char:
        if key.startswith(str(char)):
            key = key[1:]

    if (key.endswith("_*")):
        key = key[:-2]

    if key[0].isdigit():
        key = "z%s" % (key)

    return key


##
# @brief Helper function to perform cleanup on field constant value to be a 
#        valid python number
# 
# @param[in] val - XML register field value
# @return processed field value
def cleanup_xml_constant_value(val):
    val = val.replace(" ", "")
    val = val.replace(",", "")

    suffix = "b"
    if (val.endswith(suffix)):
        val = val[:-1]

        if (val.isdigit()):
            val = "0b%s" % (val)

    if (val.endswith("h")):
        val = val[:-1]
        val = str(val)
        if val.isdigit():
            val = "0x%s" % (val)

    if (val.startswith("b")):
        val = "0%s" % (val)

    return val


##
# @brief Validation function to check the number of bits represented by fieldStore
# 
# @param[in] fieldStore - set of bit definition
# @return valdiation check and matching bits
def check_field_length(fieldStore):
    bits = 0
    for field in fieldStore.values():
        bits = bits + (field.endbit - field.startbit) + 1

    if (bits != 32):
        logging.error("Register width not equal to 32 bits.Something fishy!!")
        # raise Exception("Register width not equal to 32 bits.Something fishy!!")
        return False, bits
    return True, bits


# @brief Function to check whether project attribute matches GEN parameter
# 
# @param[in] project_attr - project name
# @return True or False
def valid_project(project_attr):
    if project_attr is None:
        return True

    results = re.findall(r"GEN\d+", project_attr)
    field_gen = int(re.findall(r"\d+", results[0])[0])
    configured_gen = int(re.findall(r"\d+", GEN_VERSION)[0])

    m = HAS_ADD_PATTERN.match(project_attr)
    if m is not None:
        # Add in the current or previous gen
        if (field_gen <= configured_gen):
            return True

    m = HAS_REMOVE_PATTERN.match(project_attr)
    if m is not None:
        # Removed in future version
        if (field_gen > configured_gen):
            return True

    return False


# @brief
class BSpecParser(ET.XMLTreeBuilder):
    def __init__(self):
        self.instances = None
        ET.XMLTreeBuilder.__init__(self)
        # assumes ElementTree 1.2.X        
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ET.Comment, {})
        self._target.data(data)
        self._target.end(ET.Comment)

        if ("Address Start" in data):
            self.instances = "<root>%s</root>" % (data)


# Register is a data store class
# @brief
class Register(object):
    def __init__(self):
        register_group = None
        instance_name = None
        description = None
        start_offset = None
        end_offset = None

    def __str__(self):
        return ("Register: %s - [%s]" % (self.instance_name, self.start_offset))


# RegisterField  is a data store class for register bit definition
# @brief
class RegisterField(object):
    def __init__(self):
        fieldname = None
        startbit = 0
        endbit = 0
        project = None

    def __str__(self):
        return ("%s [%d,%d]" % (self.fieldname, self.startbit, self.endbit))


# PystructureGenerator encapsulates functionalities to transocde BSPEC xml into .py files representing bit definition
# @brief
class PystructureGenerator(object):
    def __init__(self, inputfile, outputdir):
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
            filename = "__init__.py"
            filename = os.path.join(outputdir, filename)
            fd = open(filename, 'w')
            fd.close()

        self.bspecfile = inputfile
        self.outputdir = outputdir

    def write_register_instances(self, outputfile, regstore):
        outputfile.write("'''\n")
        outputfile.write("Register instance and offset \n")
        outputfile.write("'''\n")
        for key, val in sorted(regstore.items()):
            key = key.replace("_*", "")
            outputfile.write(("%s = %s \n") % (key, val.start_offset))
        outputfile.write('\n \n')

    def write_constants(self, outputfile, fieldvaluelist):
        outputfile.write("'''\n")
        outputfile.write("Register field expected values \n")
        outputfile.write("'''\n")
        for key, val in sorted(fieldvaluelist.items()):
            key = cleanup_xml_constant_name(key)
            val = cleanup_xml_constant_value(val)

            if ("reserve" in key.lower()):
                val = "0b0"

            outputfile.write(("%s = %s \n") % (key, val))

        outputfile.write('\n \n')

    def write_internal_class(self, outputfile, register_name, fieldStore):
        outputfile.write("'''\n")
        outputfile.write("Register bitfield defnition structure \n")
        outputfile.write("'''\n")
        outputfile.write(("class %s_REG( ctypes.LittleEndianStructure ):\n") % (register_name))
        outputfile.write("    _fields_ = [\n")

        # Sort based on the start bit
        fields = fieldStore.values()
        fields.sort(key=lambda x: x.startbit, reverse=False)

        # Generate the field bit details
        max_len = 1
        for val in fields:
            max_len = max(max_len, len(val.fieldname))

        for val in fields:
            bitlen = (int(val.endbit) - int(val.startbit)) + 1
            field_val = val.fieldname.strip()
            len_format = (max_len - len(field_val))
            padding = ' '.ljust(len_format)
            field_val = '''        ("%s"%s, ctypes.c_uint32, %s), # %s to %s \n''' % (
            field_val, padding, bitlen, val.startbit, val.endbit)
            outputfile.write(field_val)

        outputfile.write("    ]\n")

        outputfile.write('\n \n')

    def write_register_class(self, outputfile, register_name):
        outputfile.write(("class %s_REGISTER( ctypes.Union ):\n") % (register_name))
        outputfile.write('    _anonymous_ = ("u",)\n')
        outputfile.write("    _fields_ = [\n")
        outputfile.write('        ("u",      %s_REG ),\n' % (register_name))
        outputfile.write('        ("asUint", ctypes.c_uint32 ) ]')
        outputfile.write('\n \n')

    def generate(self):
        bParser = BSpecParser()
        tree = ET.parse(self.bspecfile, parser=bParser)
        root = tree.getroot()

        register = root.find('Register')
        if (register is None or register.get('Name') is None):
            return

        register_name = register.get('Name').upper().replace(' ', '_').replace(':', '')

        regstore = {}
        if (bParser.instances is not None):
            try:
                comment_root = ET.fromstring(bParser.instances)

                for address in comment_root.findall('Address'):
                    obj = Register()
                    obj.register_group = register_name
                    obj.instance_name = address.get('Symbol')
                    obj.description = address.get('Name')
                    obj.start_offset = address.get('Start')
                    obj.end_offset = address.get('End')
                    regstore[obj.instance_name] = obj
            except Exception as e:
                logging.error(e)

        for address in root.findall('Register/Address'):
            obj = Register()
            obj.register_group = register_name
            obj.instance_name = address.get('Symbol')
            obj.description = address.get('Name')
            obj.start_offset = address.get('Start')
            obj.end_offset = address.get('End')
            regstore[obj.instance_name] = obj

        fieldStore = {}
        fieldvaluelist = {}

        interested_dwords = []

        interested_project = None
        for dword in root.findall('Register/DWord'):
            project_attr = dword.get('Project')
            result = valid_project(project_attr)
            if result is True:
                interested_dwords.append(dword)

        if len(interested_dwords) != 1:
            logging.error("Something fishy more than one instance of register selected")

        for bitfield in interested_dwords[0].findall('BitField'):
            field = RegisterField()
            if (bitfield.get('Name') is None):
                continue

            field.fieldname = bitfield.get('Name').replace(' ', '_').lower().replace(':', '').replace("(", "").replace(
                ")", "")
            field.startbit = int(bitfield.get('LowBit'))
            field.endbit = int(bitfield.get('HighBit'))
            field.project = bitfield.get('Project')

            if field.project is None:
                field.project = interested_project

            if (str(field.fieldname).strip() == "reserved"):
                field.fieldname = "%s_%s" % (field.fieldname, field.startbit)

            symbol_name = bitfield.get('Symbol')

            '''
            Category: Exception
            BSPEC XML has element with same name, but different symbol name, below statement
            uses symbol name instead of field name
            '''
            if (symbol_name is not None and len(symbol_name) > 0 and symbol_name != ""):
                field.fieldname = symbol_name

            fieldStore[field.fieldname] = field

            for validvalues in bitfield.findall('ValidValue'):
                value_name = validvalues.get('Name')

                if (value_name is None):
                    value_name = "default"

                value_name = value_name.upper().replace(' ', '_').replace(':', '').replace("(", "").replace(")", "")
                fiedlvaluename = ("%s_%s") % (field.fieldname, value_name)
                fieldvaluelist[fiedlvaluename] = validvalues.get('Value')

        contruded_field_store = {}
        for key, current_field in fieldStore.items():
            project_attr = current_field.project
            result = valid_project(project_attr)
            if result is True:
                contruded_field_store[key] = current_field

        result, bit_length = check_field_length(contruded_field_store)
        if (result is False):
            raise Exception("Register width not equal to 32 bits.Something fishy!!")

        filename = "%s_REGISTER.py" % (register_name)
        if self.outputdir is not None:
            filename = os.path.join(self.outputdir, filename)

        f = open(filename, 'w')

        f.write("import ctypes")
        f.write('\n \n')

        self.write_register_instances(f, regstore)
        self.write_constants(f, fieldvaluelist)
        self.write_internal_class(f, register_name, contruded_field_store)
        self.write_register_class(f, register_name)

        f.close()


'''
Stitch multiple bspec XML into single XML.
The output XML is used in flicker test sutie for
register verification.
'''


def stitchfiles(input_dir):
    first = None
    files = [inputfile for inputfile in os.listdir(input_dir) if os.path.isfile(inputfile)]

    for filename in files:
        if (filename.endswith("bspec.xml")):
            root = ET.parse(filename).getroot()

            unwanted_nodes = ['Description', 'ProgrammingNotes', 'ProgrammingNote']
            # Remove unwanted nodes
            for i in range(0, 10):
                for unwanted_node in unwanted_nodes:
                    parents = root.findall('.//%s/..' % unwanted_node)

                    for parent in parents:
                        child = parent.find('%s' % unwanted_node)
                        parent.remove(child)

            # Remove old fields
            registerParent = root.find("Register")
            fieldParent = registerParent.find("DWord")
            fields = fieldParent.findall("BitField")
            for item in fields:
                if "Project" in item.attrib and "REMOVEDBY" in item.attrib["Project"]:
                    fieldParent.remove(item)
                else:
                    item.attrib["Name"] = item.attrib["Name"].lower().replace(' ', '_').replace(':', '').replace("(",
                                                                                                                 "").replace(
                        ")", "")

                    valid_values = item.findall("ValidValue")
                    for validvalue in valid_values:
                        validvalue.attrib["Name"] = validvalue.attrib["Name"].lower().replace(' ', '_').replace(':',
                                                                                                                '').replace(
                            "(", "").replace(")", "")

            unwanted_attributes = ["_Custom_DisplayPartition", "_Custom_DisplayFUB", "Unit", "Reset", "Power",
                                   "Project"]
            # Remove unwanted attributes
            addressList = root.findall('Register/Address')
            for addr in addressList:
                for attr in unwanted_attributes:
                    if attr in addr.attrib:
                        del addr.attrib[attr]

            if first is None:
                first = root
            else:
                first.extend(root)

    if first is not None:
        filename = "register.xml"
        f = open(filename, 'w')
        f.write(ET.tostring(first))
        f.close()


'''
Generate Pythonized C structure based on Bspec XML
'''
if (__name__ == "__main__"):
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
    logging.basicConfig(filename="bspec_transcoder.log", stream=sys.stderr, level="DEBUG", format=FORMAT, filemode='w')

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--perform', help='Perform stitch/generate')
    parser.add_argument('-i', '--input', help='Input folder path')
    parser.add_argument('-o', '--output', help='Output folder path')
    args = parser.parse_args()

    if (args.perform.lower() == "generate"):
        input_dir = args.input
        output_dir = args.output

        files = []
        for root, directories, filenames in os.walk(input_dir):
            for filename in filenames:
                files.append(os.path.join(root, filename))

        for bspecfile in files:
            if (bspecfile.endswith("bspec.xml")):
                if ("HAS" in bspecfile):
                    continue
                try:
                    obj = PystructureGenerator(bspecfile, output_dir)
                    logging.info("Generating python equivalent file for %s" % (bspecfile))
                    obj.generate()
                except Exception as e:
                    logging.info("Processing %s" % bspecfile)
                    traceback.print_exc(file=sys.stdout)
                    logging.error(str(e))
    elif args.perform.lower() == "stich":
        stitchfiles(args.input)
    else:
        logging.info("Invalid commandline options")
