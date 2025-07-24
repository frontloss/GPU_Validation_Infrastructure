Folder Structure:
-----------------
'bin' will contain all C DLLs & external tools; 
'Docs' contains tools for code documentation generation and coding guidelines
'Libs' contains the common libraries, which can be used by the tests
'Logs' folder will be the location of log generation, once test completes
'registers' contain the python headers for all hw registers
'Setup' folder contain the pre-requisite installer for DisplayAutomation2.0
'Src' contains the 'C' DLL/EXE source code projects.
'Tests' folder contains the test scripts, sub-foldered as individual features

Pre-requisites:
---------------
Run 'build64.bat' from root folder to generate all DLLs in 'bin' folder. This needs to be done on a machine with VS2013 installed.
Run 'setup.bat' on the Target machine from DisplayAutomation2.0 root. This installs all required packages to run the test.
Run 'env_setup.bat' to initialize the environment variables. This will also restart the machine after setting the environment variables
From DisplayAutomation2.0, run any test with following sample commandline.
	python Tests/DisplaySwitch/apply_configuration_ddc.py -edp_a -dp_b

Reboot the system

To Do:
------
New 'C' based DLL needs to be added as part of Src/MasterSolution.sln and will be automatically built by build64.bat
Follow python unittest framework for test script coding.
Good to run sanity_check.py before checking-in the code; sanity_check.py will check for any inclusion errors
Create and update feature.xml in Tests/Feature when a new test is added, modified or a new commandline is updated.

Not To Do:
----------
Dont check-in the dll along with the source, since dll building will be taken care by 'build64.bat'


Notes:
----------
For Driver versions ci-gen9_2015-59584, ci-gen9_2016-59583, ci-main-56340 and above, use automation binaries DispAutomation-CI-00023-ww52.1 or above.