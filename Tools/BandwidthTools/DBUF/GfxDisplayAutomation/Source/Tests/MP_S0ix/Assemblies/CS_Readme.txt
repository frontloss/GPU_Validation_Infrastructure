To run CS resume time test please follow below instructions:

1. Install WDTF manually based on OS and verify WDTF is installed properly through control pannel.

2. command line is generic for all platform.

3. command: Execute.exe MP_S0ix_Gfx_Resumetime [DisplayConfig] [DisplayType]
		[DisplayConfig = SD]
		[DisplayType = EDP/MIPI]

	example:
		Execute.exe MP_S0ix_Gfx_Resumetime SD EDP
		Execute.exe MP_S0ix_Gfx_Resumetime SD MIPI

4. Need to Run cmd in admin mode.
 
5. befor run the test need to install visual studio redistributable 2012 both (64bit and 32bit). from "vcredist2012"
	
6. modify "S0ixdata.map" file on demand basis.
	benchmark value by default HSW, KBL, APL, GLK 185 ms.

7. by default framework will verify driver verifier
	if want to remove driver verifier modify "EnvironmentInit.map" file by removing 
	"<Init class="InitCheckDriverVerify" source="CoreLibrary" runOnReboot="false" runSeperate="true" />"