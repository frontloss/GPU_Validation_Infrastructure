########################################################################################################################
# @file doxygenTemplateChecker.py
# @addtogroup Tools_Doxygen
# @brief Checks for mandatory documentation tags at file level
# @author Supriya Krishnamurthi
# 1]Command for Template Checker for Directory :
# python C:/Users/supriyak/source/repos/ValDisplay/PreBuildChecks/doxygenTemplateChecker.py -i
# C:/Users/supriyak/source/repos/ValDisplay/DisplayAutomation2.0/Tests/VRR/
# 2]Command for Template Checker for File :
# python C:/Users/supriyak/source/repos/ValDisplay/PreBuildChecks/doxygenTemplateChecker.py -i
# C:/Users/supriyak/source/repos/ValDisplay/DisplayAutomation2.0/Tests/VRR/vrr_base.py
# @note This checker script is developed for python2, since git repo tools use python2 to run this script
# during 'git commit'
########################################################################################################################
import os
import re
import sys
import logging
import argparse

MESSAGE = ""
VAL_DISPLAY_PATH = "\\".join(os.path.abspath(__file__).split("\\")[:-2])
DISPLAY_AUTOMATION_PATH = os.path.join(VAL_DISPLAY_PATH, "DisplayAutomation2.0")
LOG_FOLDER_PATH = os.path.join(DISPLAY_AUTOMATION_PATH, "Logs\\")
EXCLUDE_FILES_FOLDERS = ["DisplayAutomation2.0/Tests/Color/", "DisplayAutomation2.0/Tests/ULT/"]


##
# @brief Parses the arguments and calls other functions
# @return is_template_clean Returns boolean value, True if template is clean and False otherwise
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", "-i", help="set Input file or directory path", required=True)
    args = parser.parse_args()

    if not os.path.isdir(LOG_FOLDER_PATH):
        try:
            os.makedirs(LOG_FOLDER_PATH)
        except OSError as e:
            print(e)

    is_template_clean = True
    output_txt_file_path = os.path.join(LOG_FOLDER_PATH, "doxygen_template_checker_output.txt")
    checker_output = open(output_txt_file_path, "a+")

    for input_path in args.input_path.strip().split(" "):
        # If input is directory and then perform template checking only over Python files present in all subdirectories
        if os.path.isdir(input_path):
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file).replace("\\", "/")

                    # proceed further only if its a python file and not part of exclude_file list
                    if file_path.endswith(".py") and not any(exclude_file_folder in file_path
                                                        for exclude_file_folder in EXCLUDE_FILES_FOLDERS):
                        result = template_checker(file_path)
                        if result:
                            is_template_clean = is_template_clean and False
                            MESSAGE = "\nWARNING: " + file_path + ": Mandatory tags not documented in the preamble for"\
                                                                  " File " + str(result)
                            checker_output.write(MESSAGE)
                            print(MESSAGE)
                        else:
                            MESSAGE = "\nPASS: " + file_path
                            checker_output.write(MESSAGE)

        # else it will be a file and not part of exclude_file list
        elif input_path.endswith(".py"):
            input_path = input_path.replace("\\", "/")
            if any(exclude_file_folder in input_path for exclude_file_folder in EXCLUDE_FILES_FOLDERS):
                continue

            result = template_checker(input_path)
            if result:
                is_template_clean = False
                MESSAGE = "\nWARNING: " + input_path + ": Mandatory tags not documented in the preamble for File " + str(
                    result)
                checker_output.write(MESSAGE)
                print(MESSAGE)
            else:
                MESSAGE = "\nPASS: " + input_path
                checker_output.write(MESSAGE)
        else:
            input_path = input_path.replace("\\", "/")
            MESSAGE = "\nINFO: " + input_path + ": Its neither a directory nor a .py file or it is part of Exclude" \
                                                " File list"
            checker_output.write(MESSAGE)
            print(MESSAGE)

    checker_output.close()
    return is_template_clean


##
# @brief It parses the python files and checks for the file level templates ex: @ file, @ author, @ brief, @ addtogroup
# @param[in] input_file_path Path of the file to be checked
# @return unDocumented Returns list of missing templates
def template_checker(input_file_path):
    if os.path.exists(input_file_path) is False:
        print("File does not exists")
        sys.exit(1)
    input_file = open(input_file_path, "r")
    declaration = []
    unDocumented = []
    tags = ['file', 'brief', 'author']

    for line in input_file.readlines():
        # decode string to remove UTF-8 characters that are sometimes present. Note: this str.decode works only in
        # python2. git repo tools use python 2; so this file will be run with python 2 during 'git commit'.
        line = line.decode('ascii', 'ignore')
        # Read only the preamble part from file i.e, the initial lines that start with '#'. Stop parsing after that.
        if line.lstrip() != '' and line.lstrip()[0] == '#':
            # Preprocessing to remove unwanted spaces in the template declaration lines
            declaration.append(re.sub('#[ ]*@',"@",line.lower()))
        else:
            break
    input_file.close()

    for tag in tags:
        tag_found = 0
        tag_regexp = "^@"+tag+".*\\n$"
        for text in declaration:
            if re.search(tag_regexp,text):
                tag_found = 1
        if tag_found == 0:
            unDocumented.append("@"+tag)

    return unDocumented


if __name__ == "__main__":
    status = main()
    if status:
        sys.exit(0)
    else:
        sys.exit(1)

