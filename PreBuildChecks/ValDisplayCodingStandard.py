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
# @file  ValDisplayCodingStandard.py
# @brief This file contains checkers of clang-format.
#
# --------------------------------------------------------------------------*/

import sys
import os
import argparse
import subprocess

# Globals
Edit = 0
ErrCount = 0
LLVM_BINARY_DIR = ""

IgnoreDirList = ["GfxValSimTestApp", "SystemUtilityApp"]
IgnoreFileList = ["IgfxExt_i.c", "IgfxExt_i.h", "IgfxExt.h", "IgfxExt.c", "DeckLinkAPI_i.c", "VbtArgs.h"]


def IgnoreThisDirFromScanning(DirName):
    return DirName.split("\\")[-1] in IgnoreDirList


def IgnoreThisFileFromScanning(FileName):
    return FileName.split("\\")[-1] in IgnoreFileList


def usage():
    print(" Usage: ValDisplayCodingStandard.py -p Bin Path [-s Source Path] [--edit]")
    print("")
    print(" -p BinPath - Binary path where the artifactory tools exist")
    print(" -s SourcePath - Optional. Default is ..\\DisplayAutomation2.0\\ Can provide directory or file name as path")
    print(
        " --edit = If mentioned Indicates to detection and correction of clang-format,else just detects clang-format errors")
    sys.exit(1)


def ClangScanFile(BasePath, FilePath):
    global Edit
    global ErrCount
    global LLVM_BINARY_DIR

    if IgnoreThisFileFromScanning(FilePath):  # skip old files.
        return

    CLANG_EXE_PATH = LLVM_BINARY_DIR + "clang-format.exe" + "\""
    FileName = os.path.splitext(os.path.split(FilePath)[1])[0] + ".txt"
    TEMP_FILE = os.path.join(BasePath, r"ValDisplay\PreBuildChecks", FileName)

    if FilePath.lower().endswith(('.cpp', '.hpp', '.h', '.c')) is False:
        return

    # verify this link to know more about subprocess: https://docs.python.org/2/library/subprocess.html
    if Edit == 1:
        # If ran with no arguments, then edit the files to fix the coding style
        # Cmd to run to determine if coding style is violated
        CmdString = CLANG_EXE_PATH + " -output-replacements-xml -style=file \"" + FilePath + "\""
        with open(TEMP_FILE, "w") as FileOutput:
            subprocess.call(CmdString, stdout=FileOutput)
        FileOutput.close()

        with open(TEMP_FILE, "r") as FileInput:
            lines = len((FileInput.read()).splitlines())
            # Store the number of lines in the xml file
            # for /f "tokens=*" %%c in ('!cmdline!') do set LINES=%%c
            # If more than 3 lines in xml file, then code violation was found
            if lines > 3:
                print("Editing: ", FilePath)
                CmdString = CLANG_EXE_PATH + " -i -style=file \"" + FilePath + "\""
                subprocess.call(CmdString)
            else:
                print("No Errors found for file: ", FilePath)
        FileInput.close()
    else:
        # Only check if we violate any coding style. Do not edit.
        # Cmd to run to determine if coding style is violated
        CmdString = CLANG_EXE_PATH + " -output-replacements-xml -style=file \"" + FilePath + "\""
        with open(TEMP_FILE, "w") as FileOutput:
            subprocess.call(CmdString, stdout=FileOutput)
        FileOutput.close()

        if os.path.exists(TEMP_FILE):
            with open(TEMP_FILE, "r") as FileInput:
                lines = len((FileInput.read()).splitlines())
                # Store the number of lines in the xml file
                # If more than 3 lines in xml file, then code violation was found
                if lines > 3:
                    print("Coding Style Violation:", FilePath)
                    ErrCount += lines - 3
            FileInput.close()
    try:
        os.remove(TEMP_FILE)
    except OSError:
        pass


def ClangScanFolder(BasePath, FolderPath):
    # Parse all source files in this directory
    for subdir, dirs, files in os.walk(FolderPath):
        if IgnoreThisDirFromScanning(subdir):  # skip old files.
            continue

        for file in files:
            ClangScanFile(BasePath, os.path.join(subdir, file))


def main():
    global LLVM_BINARY_DIR
    global Edit
    try:
        parser = argparse.ArgumentParser(description='Process common args.')
        parser.add_argument('-p', help='Base folder path where tools are present (FolderPath where ValDisplay folder exists)', default="")
        parser.add_argument('-s', help="Source directory/file path to run clang-format.exe",
                            default='../DisplayAutomation2.0')
        parser.add_argument('--edit', action="store_true", dest="editFile", help="Indicate clang whether to edit the file or not")
        args = parser.parse_args()

        if args.p == "":
            print("base binary directory path not specified")
            usage()

        LLVM_BINARY_DIR = "\"" + args.p + "\\ValDisplay\\LLVM\\"

        if (os.path.exists(LLVM_BINARY_DIR)):
            print("LLVM BINARY directory ", LLVM_BINARY_DIR, " not found")
            usage()

        if args.editFile:
            Edit = 1
        else:
            Edit = 0

        if (os.path.isdir(args.s)):
            ClangScanFolder(args.p, os.path.join(args.s))
        else:
            ClangScanFile(args.p, args.s)

    except Error:
        print(" Error during Parsing Folder/File")

    finally:
        global ErrCount

        if ErrCount > 0:
            print("\n Found ", ErrCount, " error(s) in clang format: Correct it before proceeding with commit" + "\n")
            print("\n Usage: CheckCodingStandard.bat /p [Base Repo Path] [/s Source Path] [Edit]")
            print("\n\t Repo Path - Binary path where the artifactory tools exists (FolderPath of Repo)")
            print("\n\t Source Path - Optional. Default ..\DisplayAutomation2.0\ (Can provide directory or file name as path)")
            print("\n\t Edit - Corrects the clang-format errors and formats the file(s) in Source Path file")
            print("\n Example: (Assuming cwd=ValDisplay\)")
            print("\n\tPreBuildChecks\CheckCodingStandard.bat /p ..\ /s DisplayAutomation2.0\Src\Logger\log.c Edit\n")
        if (ErrCount > 0):
            sys.exit(ErrCount)
        else:
            sys.exit(0)


main()
