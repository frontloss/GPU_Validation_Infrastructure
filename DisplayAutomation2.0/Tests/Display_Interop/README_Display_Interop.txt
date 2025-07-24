
===================================================
Display Interop Binary Download and Installation
===================================================

    1. Download the latest DisplayAutomation2.0 CI binaries from Ubit server(http://ubit-gfxdispval.intel.com/overview/74) .
	2. Download "DisplayAutomation2.0_x64.zip and unzip.
	3. Run 'setup.bat'in Admin mode which is present in \Output folder ( unzipped binary ) on the Target machine. 
     		-> This installs all required packages(like vcredist_x64.exe, python-2.7, DIVA etc..,) to run the tests.
	5. Run 'env_setup.bat'in Admin mode which is present in \Output folder ( unzipped binary ) on the Target machine.( this is needed to initialize the environment variables)
	6. Install Additional Binaries - ( Refer - "Steps to Install - Additional Binaries"   Given below)
	7. Restart the machine.


===================================================
Display Interop UI for Test Execution (  To Generate custom test command line ) 
===================================================

Steps:  Display Interop GUI Usage (To RUN Display Interop suite for more command lines / custom usage of Interop test )
	1. Open command prompt in Admin mode from "Output" root folder and run command "python \Tests\Display_Interop\display_interop_ui.py".
	2. Display Interop UI / Application will open.
	3. Display Interop UI shows Physically Connected Displays to choose in Device1, Device2, Device3.
			Note: If Physically Connected Displays are not coming up, Disable Sink Simulation.
				  (Open command prompt in Admin mode from "Output" root folder and run command "python Libs\env_settings.py -SINK_SIMULATION DISABLE")
	4. Select required displays, Display1, Display2, Display3, if no display is selected it takes default as "DP_A" - which is eDP.
	5. Select "Single" for SINGLE Display Config Topology, "Extended" for EXTENDED Config Topology and "Clone" for CLONE Config Topology.
	    Note: If nothing is selected, it applies all possible combinations of Config Topology based on "\Tests\Display_Interop\DisplaySequence.xml".
	6. Choose Events based on test requirements, like Test Video with Audio Clip : Plays 4K video Clip and verify Plane Verification.
	7. Test Audio (Endpoints) : Verifies Audio Endpoints of displays and (7a)Test ModeSet : Applies MMM (Minimum,Middle,Maximum) modes 
	8. Test Cursor: Cursor moves along border of Panel in steps of 10 Pixels and (8a)Test Power Mode : Select "Power Events" based on test needs, by enabling CS\S3, S4
	9. Test Rotation : Rotates Desktop to 90 Degrees and comes back to normal orientation and (9a)Test HDCP : Verifies HDCP Type 0, Type 1 and Test Driver : it Disables and Enables Gfx Driver.
	10. Select Auto Randomization, which creates 'n' number of command lines and each command line will have all test events randomly assigned. ['n' value is No.of Events in UI]
	11. Select Repetition, which allows test events to run in loops ( Based on user input ) selected test to run.
    12. Select DE Verify to enable Display Engine Verification, Manually Verify : A pop-up prompts for user input to ensure functionality based on the test events, UnderRun Verify : To verify only Underrun.
	13. Click "Save" which will generates required command line and auto append to "run_interop.bat" batch file. [ Note : Generated command line will be shown in log window UI with test count] .
	14. Click "Run" Button to start / Execute all selected test command lines one by one.
	15. Test Log of each test case gets generated in "Output" root folder and it is renamed and stored as INTEROP_Test_Logs_1, INTEROP_Test_Logs_2,.........and so on.
	16. To reset all fields, click on "Reset" button.
	17. Click "Clear Log" to clean log window UI.
	    
	       
============================================
Steps to Install - Additional Binaries which is required for testing MPO ( Video clips and other tools ) 
============================================
Additional Binary package is available in Following Share location :
[ Link \ Location : TBD]

Step-1: Pre-Requisites for running Display config test with MPO tests
	Note : Video clips are not part of Display Automation 2.0 binary - ( due to GTA requirement )
	Hence it is necessary to copy following additional set of test binaries to target machine [ mainly for local test execution ]
	Binary needs to be copied in specific path.
	For MPO - Need to required video clips in following location     
		1. In Local Disk C drive, check "SHAREDBINARY\920697932\MPO" folder existed or not.
		
	Note : Make sure system BIOS setting is appropriate , so that system can Enter/Resume Power state without any issue.
	
Step-2: Install "GfxValSim" Driver.
		Navigate to path "Output\bin\GfxValSimdriver", Open command prompt in Admin mode and run command "installer.bat i"
===================================================