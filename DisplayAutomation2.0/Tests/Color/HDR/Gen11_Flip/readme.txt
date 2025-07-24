Pre-Requisites:
----------------
1) All the DFT based HDR tests need to have DIVA(mainline) or ValSim(Yangra) installed
2) All the DFT based HDR tests need to be run on "Driver-Release-Internal" only
3) On PreSi, 
	- Please create separate TPs for Linear and Non-Linear tests as there is a dependency on the "ForceHDRMode" reg key.
	- For Linear tests alone, please add the iReg plugin to set the "ForceHDRMode" reg key in the GTA jobs.
	- For Linear tests, depending on the Driver key path, the path to add the "ForceHDRMode" reg key is :
		REG ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000" /v ForceHDRMode /t REG_QWORD /d 1 /f 
	- Please refer the TGL_HDRCommandlines.xls to categorise the tests as Linear and Non-Linear.