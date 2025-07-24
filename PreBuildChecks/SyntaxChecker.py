# ===========================================================================
#
#   Copyright (c) Intel Corporation (2000 - 2019)
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
# @file  SyntaxChecker.py
# @brief This file contains syntax checker script to validate the syntax 
#        followed by different driver codes and generate errors if some 
#        syntax is incorrect in any of the driver codings done.
#
# --------------------------------------------------------------------------*/

import sys
import re
import os
import logging

logging.basicConfig(level=logging.ERROR)

# Globals
ErrCount = 0
FilePath = ''
LineNumber = 0
InCfile = False
MAX_LINE_COUNT = 120
MAX_NESTING_LEVEL = 6
FunctionHeaderFound = False
Path = sys.argv[1]
switchdefault = 0
IgnoreDirList = ["GfxValSimTestApp", "SystemUtilityApp"]
IgnoreFileList = ["IgfxExt_i.c", "IgfxExt_i.h", "IgfxExt.h", "IgfxExt.c", "DeckLinkAPI_i.c", "VbtArgs.h"]


# Auto Generated ETW Crimson headers


# Function to search if local variable declared is in allowed list of Global pointers
def IgnoreThisDirFromScanning(DirName):
    return DirName.split("\\")[-1] in IgnoreDirList


def IgnoreThisFileFromScanning(FileName):
    return FileName.split("\\")[-1] in IgnoreFileList


def printUsage():
    print('Recheck the command line Args')


# Prints an error message in a VisualStudio-friendly format
def report_error(msg):
    global LineNumber
    global ErrCount

    print(os.path.abspath(FilePath) + ' (', LineNumber, ') : error- : ' + msg)
    ErrCount += 1
    if ErrCount > 200:
        print(" Too many errors... exiting... ")
        sys.exit(ErrCount)


# Function to check and print errors if Local variables are not followinng the coding syntax
# Used for both code and header variables
def CheckAndPrintErrorForLocals(Variable):
    # If match found, pick the corresponding string from array
    Ch = list("123")
    for i in range(0, min(3, len(str(Variable)))):
        Ch[i] = Variable[i]

    # Global variable start with "g_<Caps Letter name>". Hence ignore them
    # if variable starts with _ also, ignore them
    if ((Ch[0] == 'g') and (Ch[1] == '_') and (Ch[2] == Ch[2].upper())) or (Ch[0] == '_'):
        return

    elif (Ch[0] == 'p') or (Ch[0] == 'h'):
        # There can be a numeric character after 'p', e.g. p420VideoBlock; Hence ignoring this
        if (Ch[1] >= '0') and (Ch[1] <= '9'):
            return

    # If variable starts with a number or special character (then its not a variable), don't report error
    # TBD: This needs more correction as we might be ignoring some valid failures here
    elif re.search('([^\\w]|[0-9])', Ch[0]):
        return
    # If its a just a local non pointer variable, it should start in caps
    elif Ch[0] == Ch[0].lower():
        if Ch[0] == 'p':
            report_error(
                "First letter of variable should be in CAPS; if its a pointer, * should be assosiated with the variable")


# Object for Data type validation
class DATATYPE:
    # -------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------
    in_user_defined_type = False  # tracks outer-most type
    in_enum_data_type = False  # tracks outer-most type
    nesting_level = 0

    # -------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------

    def __init__(self, in_user_defined_type, nesting_level):
        self.in_user_defined_type = in_user_defined_type
        self.nesting_level = nesting_level
        self.in_enum_data_type = False

    # validate typedefs and user defined data types
    def Validate(self, Line, CodePart):
        global FunctionHeaderFound
        # check if typedef declared without type in same line
        if re.match('typedef\s*$', Line):
            report_error("Please put type on the same line as typedef")
            return

        # check if it is start of struct/enum of union
        # tracks outer-most type
        if self.in_user_defined_type == False or self.in_user_defined_type == None:
            if re.search('^\s*(typedef)?\s*(enum|struct|union)[ \t\w]*', Line):
                # start of the data type
                self.in_user_defined_type = True
                self.nesting_level = 0
                FunctionHeaderFound = False
                # Checks if its enum data type
                if re.search('^\s*(typedef)?\s*(enum)[ \t\w]*', Line):
                    self.in_enum_data_type = True

        if self.in_user_defined_type:
            # nesting
            NumMatches = len(re.findall("\{", Line))

            if NumMatches:
                self.nesting_level += NumMatches

            NumMatches = len(re.findall("\}", Line))
            if NumMatches:
                self.nesting_level -= NumMatches

            # check closing
            if self.nesting_level == 0:
                if re.search('(^|\})[ \t\,\w\*]*\;', Line):
                    self.in_user_defined_type = False
                    self.in_enum_data_type = False
            else:
                Array = CodePart.split(" ")
                try:
                    Array.remove('const')
                except ValueError:
                    pass
                try:
                    Array.remove('DD_IN')
                except ValueError:
                    pass
                try:
                    Array.remove('DD_OUT')
                except ValueError:
                    pass
                try:
                    Array.remove('DD_IN_OUT')
                except ValueError:
                    pass
                try:
                    Array.remove('struct')
                except ValueError:
                    pass
                try:
                    Array.remove('union')
                except ValueError:
                    pass

                # Go through the array and find the matching string starting with ASCII or '*' (for pointers)
                for i in range(1, len(Array)):
                    Variable = re.sub('[^\w]', '', Array[i])  # Strip off all special characters
                    if (Variable is not None) and (Variable != "") and (Variable != 'void'):
                        CheckAndPrintErrorForLocals(Array[i])


# Object for Function related processing
class FUNCTION:
    # -------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------
    max_code_lines = 0
    inside_function = False
    nesting_level = 0
    func_brace_count = 0
    func_decl_done = False
    func_start_line_num = 0
    max_lines_exceeded = False
    max_nesting_level_exceeded = False
    max_nesting_level = 0
    in_control_block = False

    funcStart = False

    def __init__(self, max_code_lines, nesting_level, inside_function):
        self.max_code_lines = max_code_lines
        self.nesting_level = nesting_level
        self.inside_function = inside_function

    # -------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------
    def Validate(self, CodePart, Line):
        self.declaration_check(CodePart)
        self.FunctionBody(CodePart, Line)
        self.ValidateLocalVariables(CodePart)

    def declaration_check(self, CodePart):
        if InCfile is False:
            return

        if self.nesting_level != 0:
            return

        IsMacro = re.match('^#define|^#if', CodePart)  # Check if the line begins with #define
        if not IsMacro:
            # Find for occurances for "(", to know if its a function declaration/function body start
            NumMatches = len(re.findall("\w+\(", CodePart))

            if NumMatches:
                self.func_brace_count += NumMatches
                self.funcStart = True
            # Function declaration had started if func_brace_count > 0
            # TBD: add type checks for non-static function to be having PVOID/PVOID signature
            # Find for occurrences for ")",
            NumMatches = len(re.findall("\)", CodePart))
            if NumMatches:
                self.func_brace_count -= NumMatches
                if self.func_brace_count == 0:
                    # declaration ended
                    self.func_decl_done = True
                    # Since all braces are now closed, we can assume function declaration done

        if self.func_decl_done:
            # Function declaration/definition has been done. Find which one:
            # Find occurrences for ");" or ';' to check function declaration & '[', to avoid detection of static table
            NumMatches = len(re.findall("\);|\;|\[", CodePart))
            if NumMatches:
                self.func_decl_done = False  # This is function declaration only
            else:
                self.func_decl_done = True  # Assume function body has started, until we either find '{' or ';'

    def FunctionBody(self, CodePart, Line):
        global FunctionHeaderFound
        if InCfile is False:
            return

        # Increment code line counter as we are inside function
        if self.inside_function is True:
            if not (('{' == CodePart) or ('}' == CodePart)):
                self.max_code_lines += 1

        # Find # of occurences for "{", increment nesting level
        NumMatches = len(re.findall('\{', CodePart))
        if NumMatches:
            self.nesting_level += NumMatches

        # Find # of occurences for "}", increment nesting level
        NumMatches = len(re.findall('\}', CodePart))
        if NumMatches:
            self.nesting_level -= NumMatches

        # Set flag if # of code lines exclusing comments > MAX_LINE_COUNT
        if self.max_code_lines > MAX_LINE_COUNT:
            self.max_lines_exceeded = True

        # Set flag if # of nesting levels > 5
        if (self.max_nesting_level_exceeded is False) and (self.nesting_level > MAX_NESTING_LEVEL):
            self.max_nesting_level_exceeded = True
            self.max_nesting_level = self.nesting_level

        if self.max_nesting_level_exceeded and (self.nesting_level > self.max_nesting_level):
            self.max_nesting_level = self.nesting_level  # update nesting level
        # indicate start of function
        if (self.inside_function is False) and (self.nesting_level >= 1) and self.func_decl_done is True \
                and self.funcStart is True:
            self.max_code_lines += 1
            global LineNumber
            self.func_start_line_num = LineNumber
            self.max_lines_exceeded = False
            self.max_nesting_level_exceeded = False
            self.inside_function = True
            self.func_decl_done = False
            # clear off declaration variable until we start finding another in next function
            self.in_control_block = False
            FunctionHeaderFound = False
            self.funcStart = False

        # indicates end of function
        if (self.inside_function is True) and (self.nesting_level == 0):
            self.inside_function = False
            self.max_code_lines = 0

        if self.inside_function is True and self.nesting_level >= 1:
            # Check data type inside for loop
            # Conditions should not contain = (assignment operator)
            self.Check_Conditions_not_Contain_Assignment(CodePart)
            #  Do not use !Condition for any checks. Always use Condition == FALSE
            self.Check_if_NOT_SYMBOL_USED(CodePart)

    def ValidateLocalVariables(self, CodePart):
        """
        # We have to be inside C file and nesting level 1 for local variable.
        # Assumption: Defining local variables inside control statements not allowed/checked as allowed fn. size is small.
        # TBD: Need to add checks for those??
        """
        global InCfile
        if (self.nesting_level != 1) or (InCfile is False):
            return

        """
        # Check if this is local variable declaration
        # Assumption: Local variable data typedef will be all caps. Non-caps ones will be ignored
        # TBD: seperate checks for datatypes to be done in .h file
        """
        Array = re.findall('(\w*)', CodePart)
        if (Array is None) or (Array[0] == ""):
            return

        # Still some code used UCHAR instead of DDU8. Below check is to catch those
        Variable = Array[0]

        # Check if 1st string is all caps, Same assumption as above
        if str(Variable) != str(Variable).upper():
            return

        Variable = re.search('(\w\,\w)', CodePart)
        if Variable is not None:
            report_error("Correct variable name spacing before or after Comma")

        # Split the local variable declarations in array.
        Array = CodePart.split(" ")

        # Check if variable was found and if variable doesn't have '(' character as it can be like DD_ZERO_MEM(...) etc.
        if None is not re.search('\(', Array[0]):
            return

        # Go through the array and find the matching string starting with ASCII or '*' (for pointers)
        for i in range(1, len(Array)):
            Variable = re.sub('[^\w]', '', Array[i])  # Strip off all special characters
            if (Variable is not None) and (Variable != "") and (Variable != 'void'):
                CheckAndPrintErrorForLocals(Array[i])

    # Conditions should not contain assignment inside them .. they must use comparison
    def Check_Conditions_not_Contain_Assignment(self, CodePart):
        Brace_Match = re.search('((if|while) *\(.*\))$', CodePart)
        if Brace_Match:
            m = Brace_Match.group(0)  # Contains entire if or while
            str1 = re.search('\((.*)\)', m).group(1)  # Contains various conditions inside if or while
            str2 = re.split("(&&|\|\|)", str1)  # Splits the conditions based on && or || and store that list into str2
            for i in range(len(str2)):  # Check every condition to see if any one of them contains assignment
                assignment_in_condition = re.search('(\w+ ?= ?\w+)', str2[i])  # If assignment is present raise error
                if assignment_in_condition:
                    report_error("Conditional Statements cannot use the assignment operator like if(x=y)!!! "
                                 "It must use comparison operator like if(x==y) ")
        return

    # Macros should not contain function call
    def Macro_not_Containing_Function_Call(self, Line):
        return
        Words = re.findall('\w+', Line)
        for i in range(len(Words)):
            if (True == Words[i].isupper()) and (False == IgnoreThisMacroFromScanning(Words[i])) \
                    and (None != re.search('.*' + re.escape(Words[i]) + '\(\w+\(', Line)):
                # if the Macro name is followed by '('again'('
                ignore_list_temp = re.findall('.*\((\w+)\(.*', Line)
                # there can be multiple matches for '(' followed by '('
                # Example :- pCeModeList = (CE_MODE_LIST *)(DD_ALLOC_MEM(sizeof(CE_MODE_LIST) * MAX_VIC_DEFINED));
                # ignoring sizeof() as a function as its called within DD_ALLOC_MEM.
                # Also ignoring MIPI_REG_OFFSET for now, need to remove later after GLK MIPI code cleanup.
                for j in range(len(ignore_list_temp)):
                    if ignore_list_temp[j] != 'sizeof' and ignore_list_temp[j] != 'MIPI_REG_OFFSET':
                        report_error('Dont call functions within a macro!!!')

    # FUNCTION TO ENSURE THAT NOT SYMBOL IS NOT USED .. INSTEAD USE == FALSE CONDITION
    def Check_if_NOT_SYMBOL_USED(self, CodePart):
        Condition_Inside_Quotes = re.search('(\".*![^=].*\")', CodePart)
        # Example: DISP_DBG_MSG(GFXDBG_CRITICAL,"LaceInitPhaseInSupport(): LACE PhaseIn Context allocation failed!!\r\n")
        Check_if_inside_preprocessor = re.search(r"^(#if|#ifndef|#ifdef|#error|#define)", CodePart)
        # Example :- #if !( _RELEASE_INTERNAL || _DEBUG)
        #           EventWriteMMIO_Read_Dword(NULL, Offset, *pData, *pData);
        #           #endif
        if Condition_Inside_Quotes or Check_if_inside_preprocessor:
            # If Conditions similar to examples given above then return ; no need to correct '!' here
            return
        Condition_Check = re.search('(![^=].*)',
                                    CodePart)  # If only '!' is found which is not followed by '=' then report error
        if Condition_Check:
            report_error("Do not use '!' symbol in code as it is not readable. Use explicit condition '=='or '!=' ")
        return


# Object for File related processing
class FILE:
    # -------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------
    FuncObj = FUNCTION(0, 0, False)
    VarObj = DATATYPE(0, 0)
    in_block_comment = False

    def __init__(self):
        LineNumber = 0

    # -------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------

    def ParseFile(self, FPath):
        try:
            global FilePath
            global fp
            global FunctionHeaderFound
            global switchdefault
            switchdefault = 0
            FilePath = FPath

            if IgnoreThisFileFromScanning(FPath):  # skip old files.
                return

            FunctionHeaderFound = False
            self.in_block_comment = False
            if FilePath.lower().endswith(('cpp', 'c')):
                global InCfile
                InCfile = True
                self.FuncObj = FUNCTION(0, 0, False)
                self.VarObj = DATATYPE(0, 0)
            else:
                InCfile = False

            # Parse every line in the file and applies the
            fp = open(FilePath, 'r')

            global LineNumber
            LineNumber = 0
            # Skip until file header comments are closed and code starts
            for Line in fp:
                if re.search('(\*\/)$', Line):
                    LineNumber += 1
                    break
                else:
                    LineNumber += 1
                    continue

            for Line in fp:
                LineNumber += 1
                self.ParseLine(Line)

            # check line endings
            if '\r' == fp.newlines:
                report_error("Found Non-Windows Line ending. Check your IDE settings and ensure 'CR-LF' line ending.")
            elif type(fp.newlines) is tuple:
                for item in fp.newlines:
                    if item == '\r':
                        report_error(
                            "Found Non-Windows Line ending. Check your IDE settings and ensure 'CR-LF' line ending.")

            # If at the end of the file switch and default are not equal then we will report error.
            if switchdefault != 0:
                report_error("Default Case is not found for Switch")
            fp.close()
        except:
            report_error("")
            logging.exception("ERROR: Exception caught in ParseFile():")

    def ParseLine(self, Line):
        global InCfile
        global FunctionHeaderFound

        if (self.FuncObj.inside_function == False) and (FunctionHeaderFound == False):
            if re.match('^\/\*\*', Line):
                FunctionHeaderFound = True

        # Trim non-relevant chars
        CodePart = re.sub('^[ \t\v\xEF\xBB\xBF]+|[ \t\v\r\n\f]+$', '', Line)
        if (CodePart == ""):
            return

        # process comment lines
        InBlockCommentSavedValue = self.in_block_comment
        CodePart = self.ProcessAndTrimComments(CodePart)

        if ((CodePart == "") or self.in_block_comment or InBlockCommentSavedValue):
            return

        # Check if Macro Name is in CAPS
        self.Check_if_Macro_Declaration_in_Caps(Line)

        # Check for Default Case in Switch
        self.CheckforDefaultcaseinSwitch(Line)
        # process header include
        # include directive should not use relative paths ..\ or .\; it should use forward slash only for subdirectories
        # This helps resolving inclusion search path issues across multiple projects
        IncludeMatch = re.search(r"^#include *[\"<](?P<Path>[^\"]+)[\">]", CodePart)
        if IncludeMatch is not None:
            Path = IncludeMatch.group('Path')
            return  # no further processing needed

        # replace strings
        CodePart = re.sub('\"[^\"]*?\"', '', CodePart)
        if CodePart == "":
            return

        # Validate Functions
        self.FuncObj.Validate(CodePart, Line)

        # Validate DataType defs
        self.VarObj.Validate(Line, CodePart)

    # Macros should be always declared in CAPS
    def Check_if_Macro_Declaration_in_Caps(self, Line):
        return
        MACRO_Name = re.search('^(#define (\w+).*)', Line)  # Check if the line begins with #define
        if MACRO_Name:
            if False == MACRO_Name.group(2).isupper():  # retrieve the macro name and check if its in upper case
                report_error('Macros should always be declared in FULL CAPITAL WORDS')

    # Check for default case in code
    def CheckforDefaultcaseinSwitch(self, Line):
        global switchdefault
        NumMatches1 = len(re.findall('switch\s*\(', Line))
        # if switch found we will  increase count for switchdefault variable 
        if NumMatches1:
            switchdefault += NumMatches1
        # if default is found we will decrease count for switchdefault variable at the end of file we will
        # check for it's value which should be zero incase of default is present for all switch cases in file.
        NumMatches1 = len(re.findall('default:', Line))
        if NumMatches1:
            switchdefault -= NumMatches1

    # process comment lines and check for syntax error
    # return active code part after trimming comments
    def ProcessAndTrimComments(self, Line):
        # if inside a comment block
        if self.in_block_comment:
            # check if the line has  */ but is not followed by /*
            if re.search('\*\/(?!.*\/\*)', Line):
                self.in_block_comment = False

            # if /* */ block comment end in active code line
            if re.search('\*\/.*\S+$', Line):
                report_error("'  */' block comment should not end in active code line or inserted inside active code.")
            return ""
        else:
            # remove single line block comment
            CodePart = re.sub('\/\*.*?\*\/', '', Line)
            # remove inline comment
            CodePart = re.sub('\/\/.*$', '', CodePart)

            if (CodePart != ""):
                # '/* */' block comment should not start in active code line
                if re.search('^\S+.*?\/\*', CodePart):
                    report_error(
                        "'/* ' block comment should not start in active code line or inserted inside active code.")
                    self.in_block_comment = True
                elif re.search('\/\*', CodePart):  # check if the line has  /*
                    self.in_block_comment = True

        return CodePart


def ParseFolder(Path):
    try:
        # Parse all source files in this directory
        for subdir, dirs, files in os.walk(Path):
            if IgnoreThisDirFromScanning(subdir):  # skip old files.
                continue

            for file in files:
                if file.lower().endswith(('.cpp', '.hpp', '.h', '.c')):
                    # print os.path.join(subdir, file)
                    FileObj = FILE()
                    FileObj.ParseFile(os.path.join(subdir, file))
    except:
        report_error("Error in ParseFolder()")
        logging.exception("ERROR: Exception caught in ParseFolder(): ")


def main():
    try:
        if os.path.exists(Path):
            # Loop through each line of each source file and look for coding standard violations
            if os.path.isdir(Path):
                ParseFolder(Path)
            else:
                if os.path.abspath(Path).lower().endswith(('.cpp', '.hpp', '.h', '.c')):
                    FileObj = FILE()
                    FileObj.ParseFile(os.path.abspath(Path))
        else:
            print('Path does not exist')
            printUsage()
    except Error:
        report_error("Unable to perform Syntax check ")
        logging.exception("ERROR: Exception caught in main(): ")

    finally:
        global ErrCount

        ErrCount = ErrCount
        if ErrCount > 0:
            sys.exit(ErrCount)
        else:
            sys.exit(0)


main()
