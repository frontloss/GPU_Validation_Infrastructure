########################################################################################################################
# @file         post_boot.py
# @brief        To run all the verification python files after boot to OS.
# @author       GOLI S V N LAKSHMI BHAVANI
########################################################################################################################

import subprocess
import sys

if len(sys.argv) < 2:
    print("ERROR: Expected port as an argument")
    sys.exit(1)


##
# @brief        To run all the verification python files after boot to OS.
# @param        None
# @return       None
def post_boot():
    subprocess.run(["python", "clone_pipe_verification.py"])
    subprocess.run(["python", "clone_plane_verification.py"])
    subprocess.run(["python", "clone_port_verification.py", '-CTL_A', sys.argv[1]])
    subprocess.run(["python", "clone_transcoder_verification.py"])


post_boot()
