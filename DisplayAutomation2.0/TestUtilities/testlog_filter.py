########################################################################################################################
# \file
# \addtogroup PyLibs_HelperLibs
# \section Helper Script to filter the test logs based on verbosity
# \remarks
# <pre>
# python -v INFO -i input_log_file.log -o output_log_file.log
# python -v WARN -i input_log_file.log -o output_log_file.log
# python -v ERROR -i input_log_file.log -o output_log_file.log
# python -v DEBUG -i input_log_file.log -o output_log_file.log
# </pre>
# \author Beeresh
########################################################################################################################

import argparse
import re
import sys

parser = argparse.ArgumentParser(description='Filter the DisplayAutomation2.0 log file based on verbosity.')
parser.add_argument('-v', choices=('INFO', 'DEBUG', 'WARN', 'ERROR',),
                    help="Verbosity ['INFO', 'DEBUG', 'WARN', 'ERROR']",
                    required=True)
parser.add_argument('-i', type=argparse.FileType('r'), default=sys.stdin, help='Input log file',
                    required=True)
parser.add_argument('-o', type=argparse.FileType('w'), default=sys.stdout, help='Output filtered log file',
                    required=True)

args = parser.parse_args()
args_dict = vars(args)

input_file = args_dict['i']
output_file = args_dict['o']
verbosity_to_filter = args_dict['v']

print("%s will be filtered for verbosity '%s' and output will be saved to %s" % (
input_file.name, verbosity_to_filter, output_file.name))

lines = input_file.readlines()

# Log_format = '[ %(asctime)s %(filename)-32s:%(lineno)-4s - %(funcName)32s() : %(levelname)-8s] %(message)s'
log_pattern = re.compile(r'(\[\s+\d{2}:\d{2}:\d{2}\s+\w+\.[a-z]{2}\s+:\d+\s+\-\s+\w+().*\])')

for line in lines:
    if log_pattern.match(line) is not None:
        if verbosity_to_filter in line:
            output_file.write(line)
    else:
        output_file.write(line)

print("Done...")
