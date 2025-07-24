This tool takes the following 3 files as input:

1. RmExport.dll
2. PlatformConfig.xml
3. Timings.xml

And the tool generates "SupportedConfigs.txt" which contains data of 
combination of all possible supported 4 displays from the Timings.xml file 


Reference: ..\gfx-driver\Tools\Display\OMP


-------------------------------------------------------------------------------
                                 RmExport.dll                                 
-------------------------------------------------------------------------------

Path: 
	..\DRAM_BW\Include\RmExport.dll

How to Generate the file: 
	Build the following project from Gfx Driver code base
	..\gfx-driver\Tools\Display\Exports\ResourceManager

-------------------------------------------------------------------------------
                              PlatformConfig.xml                              
-------------------------------------------------------------------------------
Path: 
	..\DRAM_BW\Include\ConfigFiles\PlatformConfig.xml

How to Generate the file: 
	Collect ETL trace with Start Device sequence and parse that ETL through 
	Diana. Start device sequence can be captured with Driver restart or System 
	Boot Trace.

-------------------------------------------------------------------------------
                                 Timings.xml                                 
-------------------------------------------------------------------------------
Path: 
	..\DRAM_BW\Include\ConfigFiles\Timings.xml

How to Generate the file: 
	Data can be collected through EDID and added to the XML manually. Mainly 
	check for HActive, VActive and RefreshRate related data.