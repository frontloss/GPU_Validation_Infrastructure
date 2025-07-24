# ===========================================================================
#
#   Copyright (c) Intel Corporation (2000 - 2018)
#
#   INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
#   ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
#   INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
#   ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
#   MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
#   OTHER WARRANTY.  Intel disclaims all liability, including liability for
#   infringement of any proprietary rights, relating to use of the code. No license,
#   express or implied, by estoppel or otherwise, to any intellectual property
#   rights is granted herein.
#
# --------------------------------------------------------------------------*/

# **------------------------------------------------------------------------*
#
# @file  ValDisplayCommitMsgChcker.py
# @brief This file contains checkers of Val display commit message 
#
# --------------------------------------------------------------------------*/

import logging
import os
import shutil
import sys

logging.basicConfig(level=logging.ERROR)

# Globals
error_count = 0

commit_msg_path = sys.argv[1]

commit_msg_dict = {"Component": False, "Type": False, "Description": False, "Platforms": False, 
                   "Related/Resolves": False}

component = ["[Display_Interfaces]", "[OS_Features]", "[Powercons]", "[Audio]", "[GOP_VBIOS]",
             "[Display_Tools]", "[IGCL]", "[VQ]", "[Compliance]", "[Val_Infra]"]

type_list = ["New_Content", "Pre_Enable", "BugFix", "Refactor", "Workaround", "Tools", "BUN", "DUN",
             "Revert", "Maintenance", "Docs", "Chore"]


def parse_message(file_path):
    global error_count
    # Parse every line in the file and applies the
    fp = open(file_path, 'rU')
    shutil.copy(file_path, os.path.dirname(os.path.realpath(__file__)))

    line_count = 0
    for line in fp:
        if line_count == 0:
            line_array = line.replace("\n", '', 1).split(' ', 3)

            if (line_array[0] in component) is False:
                print("\n Val display check-ins should have valid component name currently it is " + line_array[0])
                error_count += 1
            else:
                commit_msg_dict['Component'] = True

            if (line_array[1] in type_list) is False:
                print("\n Val display check-ins should have valid type, currently it is \"" + line_array[1])
                error_count += 1
            else:
                commit_msg_dict['Type'] = True

            if line_array[2] != ':':
                print("\n ':' missing in title message, currently it is " + line_array[2])
                error_count += 1
            if len(line_array[3]) > 65:
                print("\n Title description should be brief, within 65 characters, currently it is ",
                      len(line_array[3]))
                error_count += 1
            if line_array[3][0].isupper() is False:
                print("\n Title's first letter should be in capital")
                error_count += 1
            if line_array[3].strip().endswith("."):
                print("\n Do not end the title line with a period")
                error_count += 1

        if (line_count == 1) and (line != '\n'):
            print("\n Leave a blank line after Title line")
            error_count += 1

        if line.startswith("Description:"):
            line_array = line.replace("\n", '', 1).split(':', 2)
            if len(line_array[1]) > 100:
                print("\n Max column width limit of 100 chars exceeded on line no:{}".format(line_count))
                print(" Refer: https://wiki.openstack.org/wiki/GitCommitMessages for guidelines.\n")
                error_count += 1
            else:
                commit_msg_dict['Description'] = True

        if line.startswith("Platforms:"):
            line_array = line.replace("\n", '', 1).split(':', 1)
            if line_array[1] == '':
                print("\n Val display check-ins should have platform Name, currently it is " + line_array[1])
                error_count += 1
            else:
                commit_msg_dict['Platforms'] = True

        if line.startswith("Related-to:") or line.startswith("Resolves:"):
            line = line.replace(" ", '', 1)  # Replace 1st space encountered
            line_array = line.replace("\n", '', 1).split(':', 2)
            jira_id_found = hsd_id_found = False
            if line_array[1].startswith("http") is True:
                print("\n Do not put full URLs as they violate Intel legal policies " + line_array[1])
                error_count += 1
            elif line.startswith("Related-to:") and line_array[1].startswith("VSDI"):
                jira_id_found = True
            elif line.startswith("Related-to:") and line_array[1].startswith("HSD"):
                hsd_id_found = True
            elif line.startswith("Resolves:") and line_array[1].startswith("VSDI"):
                jira_id_found = True
            elif line.startswith("Resolves:") and line_array[1].startswith("HSD"):
                hsd_id_found = True

            if jira_id_found is False and hsd_id_found is False:
                print("\n Val display check-ins should have at least one JIRA/HSD ID, currently it is empty")
                error_count += 1
            else:
                commit_msg_dict['Related/Resolves'] = True

        line_count += 1


if __name__ == '__main__':
    try:
        if os.path.exists(commit_msg_path):
            parse_message(commit_msg_path)
        else:
            print('Given Path' + commit_msg_path + 'dose not exist' + '\n')
    except:
        print(",")
        logging.exception("ERROR: Exception caught in main(): ")

    finally:
        for key in commit_msg_dict:
            if commit_msg_dict[key] is False:
                print("FAIL - " + key + " entity violate commit message formats")
                error_count += 1
            else:
                print("SUCCESS - " + key + " entity has valid commit message formats")
        if error_count > 0:
            print("\n Found ", error_count,
                  " error(s) in commit message: Correct it before proceeding with commit" + "\n")
            print("Temporary commit message is copied at " + os.path.dirname(os.path.realpath(__file__)))
        if error_count > 0:
            sys.exit(error_count)
        else:
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.basename(commit_msg_path)))
            sys.exit(0)
