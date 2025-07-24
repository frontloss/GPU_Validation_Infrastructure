
if exist WDTF64.txt (
del WDTF64.txt
exit
)

If not exist WDTF64.txt (
echo > WDTF64.txt
msiexec /i "Windows Driver Testing Framework (WDTF) Runtime Libraries-x64_en-us.msi" /l* WDTFInstall.log WDTFDir=c:\wdtf WDTF_SKIP_MACHINE_CONFIG=1
timeout /t 30
SHUTDOWN  /f /r /t 0

)
