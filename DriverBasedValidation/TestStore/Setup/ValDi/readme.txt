ValDi is an on-demand kernel-mode driver meant for validation purpose. In the current form
it supports MMIO RW logs and CRC dumps per pipe and port. For more details about ValDi driver visit
https://github.intel.com/keolinsk/ValDi

Usage guide:-
***************
1.	Goto ValDi folder and open command line console in administrator mode
2.	Run pre.bat to install ValDi driver
3.	Execute test scenario
4.  Goto ValDi folder in c:\ and open command line console in administrator mode
5.	Run post.bat
6.	Trace files with *.valdi extension should be created at c:\AppCrashDumps

