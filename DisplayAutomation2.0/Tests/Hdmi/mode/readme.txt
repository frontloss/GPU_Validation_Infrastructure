Pre-Requisites:
----------------
Below are the Pre-requristes to run scripts planned in XML  "TestSet_hdmi_sd_modes_presi_crc.xml"
1) Test case Should be executed in Pre-Silicon Environment
2) Execute below scripts and do windows reboot, before executing test cases ( In GTA excute below scripts in Setup phase)
	python Libs\env_settings.py -silicon_type SIMULATOR -crc_presi COMPARE
	python Libs\Feature\presi\presi_crc_env_settings.py