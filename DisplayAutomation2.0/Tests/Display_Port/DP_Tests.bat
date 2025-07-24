python Tests\Display_Detection\plug_unplug_multiple.py -edp_a -dp_b -iteration 1
python Tests\Display_Detection\plug_unplug_multiple.py -edp_a -dp_b -iteration 5
python Tests\Display_Detection\plug_all_ddi_in_low_power.py -edp_a -dp_b -sleepstate s3
python Tests\Display_Detection\unplug_all_ddi_in_low_power.py -edp_a -dp_b -sleepstate s3
python Tests\Display_Port\DP_Tiled\dp_tiled_hw_ports_sync.py -config extended -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_disable-enable_tiled-to-tiled.py -config extended -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_TDR_simulation.py -config single -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_display_config_switching.py -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_hotplug_unplug_during_powerevents_tiled_to_tiled.py -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_1-input_sst.py -config extended -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_modes_enumeration.py -config extended -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_rotation.py -config extended -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_hotplugunplug_tiled_to_nontiled.py -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID
python Tests\Display_Port\DP_Tiled\dp_tiled_hotplugunplug_during_powerevents_tiled_to_nontiled.py -edp_a -dp_b DELL_U2715_M.EDID DELL_U2715_DPCD.bin -dp_c DELL_U2715_S.EDID