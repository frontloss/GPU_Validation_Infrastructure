# Copyright (2016) Intel Corporation All Rights Reserved.
#
# The source code, information and material ("Material") contained
# herein is owned by Intel Corporation or its suppliers or licensors,
# and title to such Material remains with Intel Corporation or its
# suppliers or licensors. The Material contains proprietary information
# of Intel or its suppliers and licensors. The Material is protected by
# worldwide copyright laws and treaty provisions. No part of the
# Material may be used, copied, reproduced, modified, published,
# uploaded, posted, transmitted, distributed or disclosed in any way
# without Intel's prior express written permission. No license under any
# patent, copyright or other intellectual property rights in the
# Material is granted to or conferred upon you, either expressly, by
# implication, inducement, estoppel or otherwise. Any license under such
# intellectual property rights must be express and approved by Intel in
# writing.
#
# Unless otherwise agreed by Intel in writing, you may not remove or alter
# this notice or any other notice embedded in Materials by Intel or Intel's
# suppliers or licensors in any way.
####################################################################################

GfxEvents is Intel Graphics manifest event provider registration tool and its helper scripts

=============================
Usage Instructions
=============================
1. Copy "GfxEvents" folder from TestTools to system under test
2. Run "Install.bat". This script will copy the resource file to c:\Intel\Graphics and register the provider
3. Download xperf (https://msdn.microsoft.com/en-us/windows/hardware/commercialize/test/wpt/index) 
4. Copy "xperf.exe" and "perfctrl.dll" from above download directory to
	a. In 32-bit system, copy to "GfxEvents/xperf/x86" folder. GfxEvents folder refers to folder as in #1
	b. In 64-bit system, copy to "GfxEvents/xperf/amd64" folder. GfxEvents folder refers to folder as in #1
5. Use the one of tracing options provided below to capture the trace
6. Run "Uninstall.bat" to un-register the provider

=============================
Different tracing options
=============================
1. Trace.bat

Traces all Gfx drvier events. All levels and all Keywords

=============================
2. TraceLite.bat

Traces the important trace events. 
All Key words and only the Critical and Log Always level events
Avoids Function exit of many DDIs
The SetsourceAddress and SetSourceAddressMPO are skipped (They are at Information Level)

=============================
3. DDITrace.bat

Traces only the DXGK DDIs.(Except Verbose)

=============================
4. DxgkrnlTrace.bat

Traces all Gfx events and the DxgKrnl events into one file.
the trace file sizes will be high

=============================
5. StopTrace.bat

Stops Tracing all events.

=============================
6. StackTrace.bat

Traces stack walk for event tracing.


=============================
Advanced tracing options
=============================

===================================
How to take a trace during a BSOD
===================================

1. Run the "TraceRealTime.bat" or "TraceRealTimeDxgKrnl.bat" file from the Advanced folder
2. Reproduce the BSOD
3. Reboot the system
4. Run the batch file "MergeRTTrace.bat"
5. MergedGfxTrace.etl will be generated

===================================
How to take a trace during Boot
===================================

1. Run the "Configure_Boot_Trace.bat" file from the Advanced folder
2. Reboot the system
3. Run the batch file "StopBootTrace.bat" to stop the tracing after boot
4. MergGfxBootTrace.etl will be generated