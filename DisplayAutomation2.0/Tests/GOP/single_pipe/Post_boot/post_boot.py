########################################################################################################################
# @file         post_boot.py
# @brief        To run all the verification python files after boot to OS.
# @author       GOLI S V N LAKSHMI BHAVANI
########################################################################################################################

import subprocess
import sys

if len(sys.argv) < 2:
    arg = '-CTL_A'
else:
    arg = sys.argv[1]


##
# @brief        To run all the verification python files after boot to OS.
# @param        None
# @return       None
def post_boot():
    subprocess.run(["python", "single_pipe_pipe_verification.py"])
    subprocess.run(["python", "single_pipe_plane_verification.py"])
    subprocess.run(["python", "single_pipe_port_verification.py", arg])
    subprocess.run(["python", "single_pipe_transcoder_verification.py"])


post_boot()
