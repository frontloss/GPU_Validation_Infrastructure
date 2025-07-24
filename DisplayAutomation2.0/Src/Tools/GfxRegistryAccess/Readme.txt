
******************************************************************** GfxRegistryAccess **********************************************************************************
=========================================================================================================================================================================
GfxRegistryAccess tool can be used for any graphics registry access like read or write operation 
for a given registry key. Tools accepts command line input parameters for any registry services. 
Sample Command line inputs are given below.

!!!!!!!!!!!!!!!!!!!!!!!!!!    TOOL MUST BE RUN IN ADMIN PRIVILEGES    !!!!!!!!!!!!!!!!!!!!!!!!!!

Supported Data Type (/TYEP | /T) for Gfx Registry Access
a) REG_DWORD 
b) REG_BINARY 

Supported Access Providers (/AP) for Gfx Registry Access
a) GFX_0
b) GFX_1
c) AUDIO_BUS_DRV
d) USB_KEYBOARD
e) INTERNAL_KEYBOARD

[/VALUE | /V] {value} must be semicolon seperateed.


1) Registry Read
    GfxRegistryAccess  [/READ | /R] [/AP] {name} [/KEY | /K] {key_name} [/TYEP | /T] {data_type} [/DATA_COUNT | /C] {count}
    
    Example:
    GfxRegistryAccess /R /AP GFX_0 /K TiledDisplaySupport /T REG_DWORD /C 1
    GfxRegistryAccess /R /AP GFX_0 /K CurrentState /T REG_BINARY /C 300

2) Registry Read with sub Keys
    GfxRegistryAccess  [/READ | /R] [/AP] {name} [/KEY | /K] {key_name} [/SUB_KEY | /SK] {sub_key_name} [/TYEP | /T] {data_type} [/DATA_COUNT | /C] {count}
    
    Example:
    GfxRegistryAccess /R /AP GFX_0 /K test_key /SK "Software\Intel\Display\igfxcui\igfxtray\Test" /T REG_DWORD /C 1
    GfxRegistryAccess /R /AP GFX_0 /K test_key /SK "Software\Intel\Display\igfxcui\igfxtray\Test" /T REG_BINARY /C 300

3) Registry Write
    GfxRegistryAccess  [/WRITE | /W] [/AP] {name} [/KEY | /K] {key_name} [/TYEP | /T] {data_type} [/DATA_COUNT | /C] {count} [/VALUE | /V] {value}
    
    Example:
    GfxRegistryAccess /W /AP GFX_0 /K TiledDisplaySupport /T REG_DWORD /C 1 /V 01
    GfxRegistryAccess /W /AP GFX_0 /K TiledDisplaySupport /T REG_BINARY /C 2 /V 01;6E

4) Registry Write with sub keys
    GfxRegistryAccess  [/WRITE | /W] [/AP] {name} [/KEY | /K] {key_name} [/SUB_KEY | /SK] {sub_key_name} [/TYEP | /T] {data_type} [/DATA_COUNT | /C] {count} [/VALUE | /V] {value}
    
    Example:
    GfxRegistryAccess /W /AP GFX_0 /K test_key /SK "Software\Intel\Display\igfxcui\igfxtray\Test" /T REG_DWORD /C 1 /V 01
    GfxRegistryAccess /W /AP GFX_0 /K test_key /SK "Software\Intel\Display\igfxcui\igfxtray\Test" /T REG_BINARY /C 2 /V 01;6E

===========================================================================================================================================================================