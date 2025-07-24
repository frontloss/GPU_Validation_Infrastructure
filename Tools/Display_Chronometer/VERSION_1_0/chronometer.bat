ECHO CHRONOMETER BATCH FILE 

ECHO Event Enter Sleep

Perfprofiling.exe 1

PerfParser.exe GfxPerfEvent_Enter_Sleep.dat


ECHO Mode Change


PerfProfiling.exe 7

PerfParser.exe GfxPerfEvent_Mode_Change.dat



ECHO Event Enter Hibernation

PerfProfiling.exe 3

PerfParser.exe GfxPerfEvent_Enter_Hibernation.dat


ECHO Monitor Off

PerfProfiling.exe 5

PerfParser.exe GfxPerfEvent_Monitor_Turn_Off.dat


ECHO Resume From Hibernation

PerfProfiling.exe 4

PerfParser.exe GfxPerfEvent_Resume_From_Hibernation.dat


ECHO Monitor ON

PerfProfiling.exe 6

PerfParser.exe GfxPerfEvent_Monitor_Turn_On.dat


ECHO Event Resume From Sleep

PerfProfiling.exe 2

PerfParser.exe GfxPerfEvent_Resume_From_Sleep.dat


ECHO Event Boot

PerfProfiling.exe 8


pause