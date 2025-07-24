*****************************************************************************************************************
Read Me for TestManager Script
\file         test_deployment_status.py
\addtogroup   PyTools_TestDeploymentStatus
\brief        This Utility scans all the valid "<TestSet>.xml" files present in Automation 2.0 framework and converts
              test details present in <TestSet>.xml to .csv file format (Which can be used for test management like
              to get supported platform , OS , Test qualification status etc..).

Created By : Gurusamy, BalajiX
Created On : 18WW10
*****************************************************************************************************************

Command lines:

To get RAW Dump:
		python test_deployment_status.py -a dump -p <xml file path>
		Example: python test_deployment_status.py -a dump -p C:\User\gta\Desktop\DisplayAutomation

To get RAW dump with Query Data and its count:
		python test_deployment_status.py -a dump -p <xml file path> -x <Query XML file>
		Example: python test_deployment_status.py -a dump -p C:\User\gta\Desktop\DisplayAutomation -x Query_template.xml

To Convert CSV file to XML file
		python test_deployment_status.py -a update -p <xml file path> -c <CSV File>
		Example: python test_deployment_status.py -a update -p C:\User\gta\Desktop\DisplayAutomation -c Test_Deployment_status.csv

Platform Name (Used in TestSet XML):
	Apollo Lake	: APL
	Gemini Lake	: GLK
	Lake Field	: LKF1
	Jasper Lake	: JSL
	Coffee Lake	: CFL, CFL_DT, CFL_HALO, CFL_ULT, CFL_ULX
	Cannon Lake	: CNL, CNL_ULT, CNL_ULX, CNL_HALO
	Ice Lake	: ICL, ICL_HP, ICL_LP, ICL_ULT
	Kaby Lake	: KBL, KBL_HALO, KBL_ULT, KBL_ULX
	Sky Lake	: SKL, SKL_DT, SKL_HALO, SKL_ULT, SKL_ULX
	Tiger Lake	: TGL, TGL_LP, TGL_HP, TGL_ULT, TGL_ULX

Note: For updated/Recent Platform Names refer FrameworkFolder\Tests\Smoke\TestSet_Bat\testset_xml_bat_config.xml