REM======== TEST SUIT FOR DISPLAY DEV BAT VERSION 1 ========
python Tests\Display_Dev_BAT\display_dev_bat_v1.py -GFX_0 -EDP_A SINK_EDP050 -GFX_0 -DP_D SINK_DPS003 -GFX_0 -HDMI_B SINK_HDM008 -GFX_0 -DP_F SINK_DPS027 -USR_EVE MPO2 -PWR_EVE S3 S4 -MODE_LVL L0 -SIM
timeout /t 5
rename Logs BAT_Test_log_1
