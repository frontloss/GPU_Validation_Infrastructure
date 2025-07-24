While running display config tests, need to enable VBT in setup to enable all the ports to support HDMI and DP

Example:

For KBL add below lines in setup and teardown -

[setup :setup]
test_media_core_executable -e VBT_enable.bat
    -test_media_core_executable.asset.exe_binary.asset_name: "enable"
    -test_media_core_executable.asset.exe_binary.asset_path: "gfx-sandbox-ba/VBT_REG/KBL"
    -test_media_core_executable.asset.exe_binary.asset_version: "V3"

[teardown :teardown]
test_media_core_executable -e VBT_disable.bat
    -test_media_core_executable.asset.exe_binary.asset_name: "disable"
    -test_media_core_executable.asset.exe_binary.asset_path: "gfx-sandbox-ba/VBT_REG/KBL"
    -test_media_core_executable.asset.exe_binary.asset_version: "V3"
windows_reboot

Note: Asset_path is same for KBL,SKL and CFL(gfx-sandbox-ba/VBT_REG/KBL)
In Production, it will be under gfx-display-assets-ba/DisplayAutomation2.0/VBT_REG

For Display config test command lines specific to "-user_event" flag, please find following deatils for power events:

Bits for power events:
Apply_CS -                          'Bit 0'
Apply_S3 -                          'Bit 1'
Apply_S4 -                          'Bit 2'
Apply_S5/Reboot -                   'Bit 3'
Enable dynamic CD clock for gfx_0 - 'Bit 4'
Enable dynamic CD clock for gfx_1 - 'Bit 5'
Disable MPO for gfx_0 -             'Bit 6'
Enable SSC for EFP on gfx_0 -       'Bit 7'
Enable SSC for EFP on gfx_1 -       'Bit 8'
Verify USB4 -                       'Bit 9'
Disable MPO for gfx_1 -             'Bit 10'
Reserved -                          'Bit 11 to bit 15'

Meaning of user event flag in command line:
1) -user_event 0x01 = apply_cs => System should be CS enabled
2) -user_event 0x06 = appy_s3_s4 => System should be S3 enabled(Non-CS system)
3) -user_event 0x08 = apply_s5 => Any system with reboot capability
4) -user_event 0x09 = apply_cs_s5 => System should be CS enabled
5) -user_event 0x0E = apply_s3_s4_s5 => System should be S3 enabled(Non-CS system)
6) -user_event 0x10 = enable_dynamic_cd_clk => Requires reboot so Any system with reboot capability
7) -user_event 0x11 = apply_cs_and_enable_dynamic_cd_clk => System should be CS enabled and Requires reboot so Any system with reboot capability
8) -user_event 0x16 = apply_s3_s4_and_enable_dynamic_cd_clk => System should be S3 enabled(Non-CS system) and Requires reboot so Any system with reboot capability
9) -user_event 0x18 = apply_s5_and_enable_dynamic_cd_clk => Requires reboot so Any system with reboot capability
10) -user_event 0x19 = apply_cs_s5_and_enable_dynamic_cd_clk => System should be CS enabled and Requires reboot so Any system with reboot capability
11) -user_event 0x1E = apply_s3_s4_s5_and_enable_dynamic_cd_clk => System should be S3 enabled(Non-CS system) and Requires reboot so Any system with reboot capability