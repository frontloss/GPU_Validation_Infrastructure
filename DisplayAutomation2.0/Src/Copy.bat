xcopy Certificates ..\bin\GfxValSimdriver\Certificates /s /i /Y
xcopy Templates ..\bin\GfxValSimdriver\Templates /s /i /Y
xcopy ..\bin ..\..\PublishValBin\ValBin_Output\bin /s /i /Y
xcopy ..\Libs ..\..\PublishValBin\ValBin_Output\Libs /s /i /Y
cd ..\..\PublishValBin\ValBin_Output\Libs\Core && ren Wrapper wrapper && cd ..\..\..\..\DisplayAutomation2.0\Src
xcopy ..\DisplayRegs ..\..\PublishValBin\ValBin_Output\DisplayRegs /s /i /Y
xcopy ..\registers ..\..\PublishValBin\ValBin_Output\registers /s /i /Y
xcopy ..\Tests ..\..\PublishValBin\ValBin_Output\Tests /s /i /Y
xcopy ..\TestStore ..\..\PublishValBin\ValBin_Output\TestStore /s /i /Y
xcopy ..\TestUtilities ..\..\PublishValBin\ValBin_Output\TestUtilities /s /i /Y
xcopy ..\*.py ..\..\PublishValBin\ValBin_Output /i /Y
xcopy ..\*.txt ..\..\PublishValBin\ValBin_Output /i /Y
xcopy ..\*.bat ..\..\PublishValBin\ValBin_Output /i /Y
xcopy ..\Doxyfile ..\..\PublishValBin\ValBin_Output /i /Y
