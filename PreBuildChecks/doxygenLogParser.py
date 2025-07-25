########################################################################################################################
# @file doxygenLogParser.py
# @addtogroup Tools_Doxygen
# @brief Checks for mandatory documentation tags at file level
# @author Supriya Krishnamurthi
# 1]Command for Log parser that needs html generation :
# python C:/Users/supriyak/source/repos/ValDisplay/PreBuildChecks/doxygenLogParser.py -i
# C:/Users/supriyak/source/repos/ValDisplay/DisplayAutomation2.0/Tests/VRR/ -html
# 2]Command for Log parser that doesnt need html generation :
# python C:/Users/supriyak/source/repos/ValDisplay/PreBuildChecks/doxygenLogParser.py -i
# C:/Users/supriyak/source/repos/ValDisplay/DisplayAutomation2.0/Tests/VRR/
# @note This checker script is developed for python2, since git repo tools use python2 to run this script
# during 'git commit'
########################################################################################################################
import os
import re
import sys
import argparse
import subprocess

VAL_DISPLAY_PATH = "\\".join(os.path.abspath(__file__).split("\\")[:-2])
DISPLAY_AUTOMATION_PATH = os.path.join(VAL_DISPLAY_PATH, "DisplayAutomation2.0")
LOG_FOLDER_PATH = os.path.join(DISPLAY_AUTOMATION_PATH, "Logs\\")
SKIP_WARNING_TYPES = ["variable", "multiple use of section label", "No output formats selected"]
EXCLUDE_FILES_FOLDERS = ["DisplayAutomation2.0/Tests/Color/", "DisplayAutomation2.0/Tests/ULT/"]
DOXYFILE_TAGS_TO_EDIT = {}


##
# @brief It parses the arguments and calls all other functions
# @return is_log_clean returns boolean value, True if  no errors and False otherwise
def main():
    # Parse cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", "-i", help="set Input file path", required=True)
    parser.add_argument("--html", "-html", action="store_true", dest="generate_html", help="doxygen_generate_html")
    parser.add_argument("--output", "-o", help="set output file path")
    args = parser.parse_args()

    doxygen_src_path = args.input_path
    doxygen_generate_html = args.generate_html

    # create log folder if not exists
    if not os.path.isdir(LOG_FOLDER_PATH):
        try:
            os.makedirs(LOG_FOLDER_PATH)
        except OSError as e:
            print(e)

    # creating a relative path for doxygen.exe
    doxygen_exe_path = os.path.join(DISPLAY_AUTOMATION_PATH, "TestStore\\CommonBin\\doxygen_1.8.20.exe")
    existing_config_file = os.path.join(DISPLAY_AUTOMATION_PATH, "TestStore\\CommonBin\\PyGfxAutomation_Doxyfile")

    # editDoxyFile
    tags_to_edit = update_doxyfile_tags_to_edit(doxygen_src_path, doxygen_generate_html, EXCLUDE_FILES_FOLDERS)
    new_doxyfile_path = edit_doxygen_config_file(tags_to_edit, existing_config_file)

    # running Doxygen with Edited doxyfile
    doxygen_command = doxygen_exe_path + " " + new_doxyfile_path
    doxygen_log_path = os.path.join(LOG_FOLDER_PATH, "doxygen_log.txt")
    run_doxygen(doxygen_command, doxygen_log_path)

    # prepare to parse the logfile generated by Doxygen
    if doxygen_log_path:
        input_log_file_path = doxygen_log_path
        if args.output:
            output_txt_file_path = args.output
        else:
            output_txt_file_path = os.path.join(LOG_FOLDER_PATH, "doxygen_parser_output.txt")

    # Run Log Parser
    is_log_clean = True
    result = parse_log_file(input_log_file_path, output_txt_file_path)
    if result is False:
        is_log_clean = False
    else:
        warning_output_file = open(output_txt_file_path, "a+")
        warning_output_file.write("No documentation issues found")
        warning_output_file.close()

    return is_log_clean


##
# @brief     Update the dictionary(DOXYFILE_TAGS_TO_EDIT) of regex to be matched to find the tag in config file and its
#            corresponding edited value
# @param[in] doxygen_src_path Source file path from the input argument
# @param[in] doxygen_generate_html This boolean value is true if --HTML argument is passed by the user, False otherwise
# @param[in] doxygen_excludes List of all the source paths to be excluded from input tag in doxyfile
# @return DOXYFILE_TAGS_TO_EDIT Returns the dictionary with tags to be edited in doxyfile and their corresponding values
def update_doxyfile_tags_to_edit(doxygen_src_path, doxygen_generate_html, doxygen_excludes):
    # edit the input tag with source path mentioned
    DOXYFILE_TAGS_TO_EDIT["^INPUT[ ]+[=]"] = doxygen_src_path

    # edit generate html tag based on user input
    if doxygen_generate_html:
        DOXYFILE_TAGS_TO_EDIT["^GENERATE_HTML[ ]+[=]"] = "YES"

    # edit the exclude tag to ignore the unwanted files/folders mentioned in EXCULDE_FILES_FOLDERS from doxygen parsing
    doxygen_exclude_path = ''
    for exclude_file_folder in doxygen_excludes:
        doxygen_exclude_path += " " + os.path.join(VAL_DISPLAY_PATH, exclude_file_folder).replace("\\", "/")
    DOXYFILE_TAGS_TO_EDIT["^EXCLUDE[ ]+[=]"] = doxygen_exclude_path

    return DOXYFILE_TAGS_TO_EDIT


##
# @brief     To edit the input source path of the existing Doxyfile and storing the edited Config file to a new one
# @param[in] tags_to_edit dictionary having tags to edit and the value to be replaced with
# @param[in] existing_config_file Existing config file
# @return    new_config_file_path the path of new edited config file
def edit_doxygen_config_file(tags_to_edit, existing_config_file):
    current_config_file = open(existing_config_file, "r")
    new_config_file_path = os.path.join(LOG_FOLDER_PATH, "new_configfile")
    new_config_file = open(new_config_file_path, "w+")
    for line in current_config_file.readlines():
        for regexp, edit_val in tags_to_edit.items():
            if re.search(regexp, line):
                # If tag to be edited is found then frame the line using the existing tag name format and new value
                line = "= ".join([line.split("=")[0], edit_val]) + "\n"
        new_config_file.write(line)
    current_config_file.close()
    new_config_file.close()

    return new_config_file_path


##
# @brief     It runs the doxygen application and stores console error output to log file
# @param[in] command Command to run Doxygen with Edited Doxyfile(config file)
# @param[in] log_output_path is the path where Output errors/warnings thrown by the Doxygen are stored
# @return    None
def run_doxygen(command, log_output_path):
    file_output = open(os.path.join(LOG_FOLDER_PATH, "file_output.txt"), "w+")
    with open(log_output_path, "w") as file_err:
        subprocess.call(command, stderr=file_err, stdout=file_output)
        file_err.close()
    file_output.close()
    # removing file_output.txt(stdout) after saving stderr in file_err(log_output_path)
    os.remove(os.path.join(LOG_FOLDER_PATH, "file_output.txt"))


##
# @brief     It parses the log file produced by Doxygen and stores warnings in Output file
# @param[in] input_log_file_path Doxygen log file path
# @param[in] output_txt_file_path is the path where parsed warnings are stored
# @return    Returns True if no warnings are present in o/p file else false
def parse_log_file(input_log_file_path, output_txt_file_path):
    warning_output_file = open(output_txt_file_path, "a+")
    ret = True
    with open(input_log_file_path, "r") as log_file:
        for line in log_file:
            # line should have warning but should not contain any SKIP_WARNING_TYPES
            if "warning" in line and len([skip_type for skip_type in SKIP_WARNING_TYPES if (skip_type in line)]) == 0:
                line = "WARNING: " + line.replace("warning: ", "")
                print(line)
                warning_output_file.write(line + "\n")
                ret = False
        log_file.close()
        warning_output_file.close()
    # delete the input doxygen log file after parsing
    os.remove(input_log_file_path)
    return ret


if __name__ == "__main__":
    status = main()
    if status:
        sys.exit(0)
    else:
        sys.exit(1)
