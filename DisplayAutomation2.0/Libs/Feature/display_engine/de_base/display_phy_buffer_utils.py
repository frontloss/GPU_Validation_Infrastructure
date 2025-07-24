########################################################################################################################
# @file         display_phy_buffer_utils.py
# @brief        Utilities file to store bspec phy buffer values and combo phy, type-c phy dictionaries
# @author       Kumar V Arun, Veluru Veena, Goutham N
########################################################################################################################

PHY_BASE_DICT = {"HIP_168_Base": 0x168000, "HIP_169_Base": 0x169000, "HIP_16A_Base": 0x16A000,
                 "HIP_16B_Base": 0X16B000, "HIP_16C_Base": 0X16C000, "HIP_16D_Base": 0X16D000 }

supported_platform_list = ["ICLLP","TGL","DG1","ADLP","RKL","ADLS", "MTL", "LNL", "ELG"]

combo_phy_platform_supported_ports_dict = {
    "ICLLP":["A","B"],
    "TGL":["A","B"],
    "DG1":["A","B","C","D"],
    "ADLP":["A","B"],
    "RKL":["A","B","C","D"],
    "DG2": ["A", "B", "C", "D"],
    "ADLS":["A","B","C","D","E"],
    "MTL":["A", "B"],
    "LNL":["A"]
    # BMG/ELG: eDP will be programmed on C20 PHY
}

typec_phy_platform_supported_ports_dict = {
    "ICLLP":["C","D","E","F"],
    "TGL":["D","E","F","G","H","I"],
    "ADLP":["F","G","H","I"],
    "MTL":["F","G","H","I"],
    "LNL":["F","G","H"],
    "ELG":["A","F","G","H","I"]
}

combo_phy_platform_supported_vswing_preemp_dict ={
    "ICLLP": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "TGL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "DG1":[[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "ADLP": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "RKL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "DG2": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "ADLS": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "MTL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "LNL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "ELG": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]]
}

typec_phy_platform_supported_vswing_preemp_dict ={
    "ICLLP": [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1]],
    "TGL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "ADLP": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "MTL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "LNL": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]],
    "ELG": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [3, 0]]
}

DP_2P0_SUPPORTED_TX_FFE_PRESET_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# B-Spec Link for TGL, DG1, DG2 Settings- https://gfxspecs.intel.com/Predator/Home/Index/49291
# B-Spec Link for ICL Settings- https://gfxspecs.intel.com/Predator/Home/Index/21257



# Below Table used to verify in case of eDP upto HBR2(default swing vbt setting), DP upto HBR2 for combophy ports in ICL
gen11_combo_phy_vswing_preemp_table_dp_uptoHBR2 ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of eDP upto HBR2(low swing vbt setting) for ICL
combo_phy_vswing_preemp_table_edp_uptoHBR2 ={
    "0,0": [0b0000, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1000, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b0001, 0x7F, 0x33, 0x00, 0x0C, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b1001, 0x7F, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1000, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b0001, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b1001, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b0001, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b1001, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b1001, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of eDP HBR3(low swing vbt setting) for ICL
combo_phy_vswing_preemp_table_edp_HBR3 ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of eDP upto HBR(default swing vbt setting), DP upto HBR for combophy ports in all TGL Skus
TGL_DG2_combo_phy_vswing_preemp_table_dp_uptoHBR ={
    "0,0": [0b1010, 0x32, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7D, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of eDP HBR2(default swing vbt setting), DP HBR2 for combophy ports in TGLU and TGLY Skus
TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x60, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b1100, 0x7F, 0x2D, 0x00, 0x12, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1100, 0x47, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x6F, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7D, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b0110, 0x60, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of eDP HBR2(default swing vbt setting), DP HBR2 for combophy ports in Non TGLU and TGLY Skus
TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2 ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x63, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x47, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x63, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x61, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7b, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP upto HBR for combophy ports in all DG1 Skus
gen13_DG1_combo_phy_vswing_preemp_table_dp_uptoHBR ={
    "0,0": [0b1010, 0x32, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x48, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x63, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2C, 0x00, 0x13, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x43, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x60, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x30, 0x00, 0x0F, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x60, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP HBR2/HBR3 for combophy ports in all DG1 Skus
gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3 ={
    "0,0": [0b1010, 0x32, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x48, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x63, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2C, 0x00, 0x13, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x43, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x60, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x30, 0x00, 0x0F, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x58, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of EDP upto HBR2 for combophy ports in all DG1 Skus
gen13_DG1_combo_phy_vswing_preemp_table_edp_upto_HBR2 ={
    "0,0": [0b0000, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1000, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b0001, 0x7F, 0x33, 0x00, 0x0C, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b1001, 0x7F, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1000, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b0001, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b1001, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b0001, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b1001, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b1001, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of EDP HBR3 for combophy ports in all DG1 Skus
gen13_DG1_combo_phy_vswing_preemp_table_edp_HBR3 ={
    "0,0": [0b1010, 0X35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP upto HBR for combophy ports in all ADLP Skus
gen13_ADLP_combo_phy_vswing_preemp_table_dp_uptoHBR ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2C, 0x00, 0x13, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0b, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x7C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0a, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP HBR2/HBR3 for combophy ports in all ADLP Skus
gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3 ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x30, 0x00, 0x0F, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x30, 0x00, 0x0F, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x63, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of EDP upto HBR2 for combophy ports in all ADLP Skus
gen13_ADLP_combo_phy_vswing_preemp_table_edp_upto_HBR2 ={
    "0,0": [0b0100, 0x50, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b0100, 0x58, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b0100, 0x60, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0100, 0x6A, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b0100, 0x5E, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b0100, 0x61, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0100, 0x6B, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b0100, 0x69, 0x39, 0x00, 0x06, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0100, 0x73, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0100, 0x7A, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}


# Below Table used to verify in case of EDP HBR3 for combophy ports in all ADLP Skus
gen13_ADLP_combo_phy_vswing_preemp_table_edp_HBR3 ={
    "0,0": [0b1010, 0X35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x30, 0x00, 0x0F, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x30, 0x00, 0x0F, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x63, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP upto HBR for combophy ports in all RKL Skus
gen13_RKL_combo_phy_vswing_preemp_table_dp_uptoHBR ={
    "0,0": [0b1010, 0x2F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x63, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7D, 0x2A, 0x00, 0x15, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0b, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6E, 0x3E, 0x00, 0x01, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0a, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP HBR2/HBR3 for combophy ports in all RKL Skus
gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3 ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x50, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x61, 0x33, 0x00, 0x0C, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2E, 0x00, 0x11, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x47, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x5F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x5F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7E, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of EDP upto HBR2 for combophy ports in all RKL Skus
gen13_RKL_combo_phy_vswing_preemp_table_edp_upto_HBR2 ={
    "0,0": [0b0000, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1000, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b0001, 0x7F, 0x33, 0x00, 0x0C, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b1001, 0x7F, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1000, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b0001, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b1001, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b0001, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b1001, 0x7F, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b1001, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}


# Below Table used to verify in case of EDP HBR3 for combophy ports in all RKL Skus
gen13_RKL_combo_phy_vswing_preemp_table_edp_HBR3 ={
    "0,0": [0b1010, 0X35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP upto HBR for combophy ports in all ADLS Skus
gen13_ADLS_combo_phy_vswing_preemp_table_dp_uptoHBR ={
    "0,0": [0b1010, 0x32, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x71, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7D, 0x2B, 0x00, 0x14, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x4C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x73, 0x34, 0x00, 0x0B, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x7F, 0x2F, 0x00, 0x10, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x6C, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of DP HBR2/HBR3 for combophy ports in all ADLS Skus
gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3 ={
    "0,0": [0b1010, 0x35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x63, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2C, 0x00, 0x13, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x47, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x63, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x73, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x58, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}

# Below Table used to verify in case of EDP upto HBR2 for combophy ports in all ADLS Skus
gen13_ADLS_combo_phy_vswing_preemp_table_edp_upto_HBR2 ={
    "0,0": [0b1001, 0x73, 0x3D, 0x00, 0x02, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1001, 0x7A, 0x3C, 0x00, 0x03, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1001, 0x7F, 0x3B, 0x00, 0x04, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0100, 0x6C, 0x33, 0x00, 0x0C, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b0010, 0x73, 0x3A, 0x00, 0x05, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b0010, 0x7C, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0100, 0x5A, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b0100, 0x57, 0x3D, 0x00, 0x02, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0100, 0x65, 0x38, 0x00, 0x07, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0100, 0x6C, 0x3A, 0x00, 0x05, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}


# Below Table used to verify in case of EDP HBR3 for combophy ports in all ADLS Skus
gen13_ADLS_combo_phy_vswing_preemp_table_edp_HBR3 ={
    "0,0": [0b1010, 0X35, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,1": [0b1010, 0x4F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,2": [0b1100, 0x63, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "0,3": [0b0110, 0x7F, 0x2C, 0x00, 0x13, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,0": [0b1010, 0x47, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,1": [0b1100, 0x63, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "1,2": [0b0110, 0x73, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,0": [0b1100, 0x58, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "2,1": [0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
    "3,0": [0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
}



# Below Table used to verify  DP Type C settings upto HBR in ICL
gen11_typec_phy_vswing_preemp_table_RBR_HBR ={
    "0,0": [0x18, 1, 0, 0x00],
    "0,1": [0x1D, 1, 0, 0x05],
    "0,2": [0x24, 1, 0, 0x0C],
    "0,3": [0x2B, 1, 0, 0x14],
    "1,0": [0x21, 1, 0, 0x00],
    "1,1": [0x2B, 1, 0, 0x08],
    "1,2": [0x30, 1, 0, 0x0F],
    "2,0": [0x31, 1, 0, 0x03],
    "2,1": [0x34, 1, 0, 0x0B],
    "3,0": [0x3F, 1, 0, 0x00]
}

# Below Table used to verify  DP Type C settings for HBR2 and HBR3 in ICL
gen11_typec_phy_vswing_preemp_table_HBR2_HBR3 ={
    "0,0": [0x18, 1, 0, 0x00],
    "0,1": [0x1D, 1, 0, 0x05],
    "0,2": [0x24, 1, 0, 0x0C],
    "0,3": [0x2B, 1, 0, 0x14],
    "1,0": [0x26, 1, 0, 0x00],
    "1,1": [0x2C, 1, 0, 0x07],
    "1,2": [0x33, 1, 0, 0x0C],
    "2,0": [0x2E, 1, 0, 0x00],
    "2,1": [0x36, 1, 0, 0x09],
    "3,0": [0x3F, 1, 0, 0x00]
}

gen12_typec_phy_vswing_preemp_table_RBR_HBR ={
    "0,0": [7, 0, 0x0],
    "0,1": [5, 0, 0x5],
    "0,2": [2, 0, 0xB],
    "0,3": [0, 0, 0x18],
    "1,0": [5, 0, 0x0],
    "1,1": [2, 0, 0x8],
    "1,2": [0, 0, 0x14],
    "2,0": [2, 0, 0x0],
    "2,1": [0, 0, 0xB],
    "3,0": [0, 0, 0x0]
}

# Below Table used to verify  DP Type C settings for HBR2 and HBR3 in TGL
gen12_typec_phy_vswing_preemp_table_HBR2_HBR3 ={
    "0,0": [7, 0, 0x0],
    "0,1": [5, 0, 0x5],
    "0,2": [2, 0, 0xB],
    "0,3": [0, 0, 0x19],
    "1,0": [5, 0, 0x0],
    "1,1": [2, 0, 0x8],
    "1,2": [0, 0, 0x14],
    "2,0": [2, 0, 0x0],
    "2,1": [0, 0, 0xB],
    "3,0": [0, 0, 0x0]
}

gen13_ADLP_typec_phy_vswing_preemp_table_RBR_HBR ={
    "0,0": [7, 0, 0x1],
    "0,1": [5, 0, 0x6],
    "0,2": [2, 0, 0xB],
    "0,3": [0, 0, 0x17],
    "1,0": [5, 0, 0x0],
    "1,1": [2, 0, 0x8],
    "1,2": [0, 0, 0x14],
    "2,0": [2, 0, 0x0],
    "2,1": [0, 0, 0xB],
    "3,0": [0, 0, 0x0]
}

# Below Table used to verify  DP Type C settings for HBR2 and HBR3 in TGL
gen13_ADLP_typec_phy_vswing_preemp_table_HBR2_HBR3 ={
    "0,0": [7, 0, 0x0],
    "0,1": [5, 0, 0x4],
    "0,2": [2, 0, 0xA],
    "0,3": [0, 0, 0x18],
    "1,0": [5, 0, 0x0],
    "1,1": [2, 0, 0x6],
    "1,2": [0, 0, 0x14],
    "2,0": [2, 0, 0x0],
    "2,1": [0, 0, 0x9],
    "3,0": [0, 0, 0x0]
}

# Below Table used to verify  DP Type C settings for HBR2 and HBR3 in TGL
gen13_ADLP_hdmi_typec_phy_vswing_preemp_table ={
    "1": [7, 0, 0x0],
    "2": [6, 0, 0x0],
    "3": [4, 0, 0x0],
    "4": [2, 0, 0x0],
    "5": [0, 0, 0x0],
    "6": [0, 0, 0x5],
    "7": [0, 0, 0x6],
    "8": [0, 0, 0x7],
    "9": [0, 0, 0x8],
    "10": [0, 0, 0xA]
}

# Below table to verify DP 2.1 settings for UHBR10 and UHBR20 for RPLP
# Reference link https://gfxspecs.intel.com/Predator/Home/Index/54956
gen13_rplp_dp2_0_tx_ffe_preset_table = {
    0:[0x0, 0x00, 0x00, 0x00, 0x00, 0x00],
    1:[0x0, 0x00, 0x04, 0x00, 0x00, 0x00],
    2:[0x0, 0x00, 0x07, 0x00, 0x00, 0x00],
    3:[0x0, 0x00, 0x0A, 0x00, 0x00, 0x00],
    4:[0x0, 0x00, 0x0F, 0x00, 0x00, 0x00],
    5:[0x0, 0x02, 0x00, 0x00, 0x00, 0x00],
    6:[0x0, 0x02, 0x04, 0x00, 0x00, 0x00],
    7:[0x0, 0x02, 0x07, 0x00, 0x00, 0x00],
    8:[0x0, 0x02, 0x0A, 0x00, 0x00, 0x00],
    9:[0x0, 0x03, 0x0D, 0x00, 0x00, 0x00],
    10:[0x0, 0x03, 0x00, 0x00, 0x00, 0x00],
    11:[0x0, 0x06, 0x04, 0x00, 0x00, 0x00],
    12:[0x0, 0x06, 0x06, 0x00, 0x00, 0x00],
    13:[0x0, 0x07, 0x0B, 0x00, 0x00, 0x00],
    14:[0x0, 0x0B, 0x00, 0x00, 0x00, 0x00],
    15:[0x0, 0x02, 0x02, 0x04, 0x10, 0x17]
}

# Below Table used to verify DP 1.4 Tx equalization settings for MTL C10 PHY
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/65449
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen14_MTL_C10_phy_DP1_4_vswing_preemp_table = {
    "0,0": [0, 26, 0],
    "0,1": [0, 33, 6],
    "0,2": [0, 38, 11],
    "0,3": [0, 43, 19],
    "1,0": [0, 39, 0],
    "1,1": [0, 45, 7],
    "1,2": [0, 46, 13],
    "2,0": [0, 46, 0],
    "2,1": [0, 55, 7],
    "3,0": [0, 62, 0]
}

# Below Table used to verify DP 1.4 Tx equalization settings for MTL C20 PHY
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/65449
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen14_MTL_C20_phy_DP1_4_vswing_preemp_table = {
    "0,0": [0, 20, 0],
    "0,1": [0, 24, 4],
    "0,2": [0, 30, 9],
    "0,3": [0, 34, 14],
    "1,0": [0, 29, 0],
    "1,1": [0, 34, 5],
    "1,2": [0, 38, 10],
    "2,0": [0, 36, 0],
    "2,1": [0, 40, 6],
    "3,0": [0, 48, 0]
}
# Below Table used to verify DP 1.4 Tx equalization settings for ELG C20 PHY
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/65449
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen14_ELG_C20_phy_DP1_4_vswing_preemp_table = {
    "0,0": [0, 20, 0],
    "0,1": [0, 24, 4],
    "0,2": [0, 30, 9],
    "0,3": [0, 34, 14],
    "1,0": [0, 29, 0],
    "1,1": [0, 34, 5],
    "1,2": [0, 38, 10],
    "2,0": [0, 36, 0],
    "2,1": [0, 40, 6],
    "3,0": [0, 48, 0]
}

# Below Table used to verify C20 DP 2.1 Tx equalization settings for MTL
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/65449
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen14_MTL_C20_phy_DP2_0_ffe_preset_table = {
    0:  [0, 48, 0],
    1:  [0, 43, 5],
    2:  [0, 40, 8],
    3:  [0, 37, 11],
    4:  [0, 33, 15],
    5:  [2, 46, 0],
    6:  [2, 42, 4],
    7:  [2, 38, 8],
    8:  [2, 35, 11],
    9:  [2, 33, 13],
    10: [4, 44, 0],
    11: [4, 40, 4],
    12: [4, 37, 7],
    13: [4, 33, 11],
    14: [8, 40, 0],
    15: [2, 30, 2]
}

# Below Table used to verify C20 DP 2.1 Tx equalization settings for ELG
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/65449
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen14_ELG_C20_phy_DP2_1_ffe_preset_table = {
    0:  [0, 48, 0],
    1:  [0, 43, 5],
    2:  [0, 40, 8],
    3:  [0, 37, 11],
    4:  [0, 33, 15],
    5:  [2, 46, 0],
    6:  [2, 42, 4],
    7:  [2, 38, 8],
    8:  [2, 35, 11],
    9:  [2, 33, 13],
    10: [4, 44, 0],
    11: [4, 40, 4],
    12: [4, 37, 7],
    13: [4, 33, 11],
    14: [8, 40, 0],
    15: [2, 30, 2]
}

# Below table is used to verify lane commit bit for offset - 0xD71 for dp native displays
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/64539
# Format: {[Number of lanes]: [Tx1, Tx2]}
gen14_MTL_expected_lane_commit_bit_native = {
    1: [1, 0],
    2: [1, 1],
    4: [1, 1]
}

# Below table is used to verify lane commit bit for offset - 0xD71 for type-c displays
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/64539
# Format: {[Number of lanes]: [Tx1, Tx2]}
gen14_MTL_expected_lane_commit_bit_type_c = {
    1: [0, 1],
    2: [1, 1],
    4: [1, 1]
}

# This table verifies the lane commit bit for offset 0xD71 in DP native displays. When writing to TX1 or TX2 of PHY
# Lane 0 or PHY Lane 1, bit 0 or bit 2, respectively, of register 0xD71 (lane_commit_bit) is set to 1. According to
# the PHY Lane and Transmitter Usage table provided in https://gfxspecs.intel.com/Predator/Home/Index/68960,
# if the lane count is 1, only bit 0 is set for TX1 of PHY Lane 0. For a lane count of 2, both bits 0 and 2 are set
# for TX1 and TX2 of PHY Lane 0. For a lane count of 4, bits 0 and 2 are set for TX1 and TX2 of both Lane 0 and Lane
# 1, where Lane 0 TX2 is equivalent to Lane 1 TX2 and Lane 0 TX1 is equivalent to Lane 1 TX1.
# format: {[lane count]: [Tx1, Tx2]}
gen14_ELG_expected_lane_commit_bit_native = {
    1: [1, 0],
    2: [1, 1],
    4: [1, 1]
}

# Below Table used to verify DP 1.4 Tx equalization settings for LNL C10 PHY
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/68963
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen15_LNL_C10_phy_DP1_4_vswing_preemp_table = {
    "0,0": [0, 26, 0],
    "0,1": [0, 33, 6],
    "0,2": [0, 38, 11],
    "0,3": [0, 43, 19],
    "1,0": [0, 39, 0],
    "1,1": [0, 45, 7],
    "1,2": [0, 46, 13],
    "2,0": [0, 46, 0],
    "2,1": [0, 55, 7],
    "3,0": [0, 62, 0]
}

# Below Table used to verify DP 1.4 Tx equalization settings for LNL C20 PHY
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/68963
# Format: {[voltage swing level,Pre-emphasis]:[Pre Cursor, Main Cursor, Post Cursor]}
gen15_LNL_C20_phy_DP1_4_vswing_preemp_table = {
    "0,0": [0, 20, 0],
    "0,1": [0, 24, 4],
    "0,2": [0, 30, 9],
    "0,3": [0, 34, 14],
    "1,0": [0, 29, 0],
    "1,1": [0, 34, 5],
    "1,2": [0, 38, 10],
    "2,0": [0, 36, 0],
    "2,1": [0, 40, 6],
    "3,0": [0, 48, 0]
}

# Below Table used to verify C20 DP 2.1 Tx equalization settings for LNL
# Bspec reference: https://gfxspecs.intel.com/Predator/Home/Index/68963
# Format: {[preset]:[Pre Cursor, Voltage Swing Select, Post Cursor]}
gen15_LNL_C20_phy_DP2_0_ffe_preset_table = {
    0:  [0, 48, 0],
    1:  [0, 43, 5],
    2:  [0, 40, 8],
    3:  [0, 37, 11],
    4:  [0, 33, 15],
    5:  [2, 46, 0],
    6:  [2, 42, 4],
    7:  [2, 38, 8],
    8:  [2, 35, 11],
    9:  [2, 33, 13],
    10: [4, 44, 0],
    11: [4, 40, 4],
    12: [4, 37, 7],
    13: [4, 33, 11],
    14: [8, 40, 0],
    15: [2, 30, 2]
}

# This table verifies the lane commit bit for offset 0xD71 in DP native displays. When writing to TX1 or TX2 of PHY
# Lane 0 or PHY Lane 1, bit 0 or bit 2, respectively, of register 0xD71 (lane_commit_bit) is set to 1. According to
# the PHY Lane and Transmitter Usage table provided in https://gfxspecs.intel.com/Predator/Home/Index/68960,
# if the lane count is 1, only bit 0 is set for TX1 of PHY Lane 0. For a lane count of 2, both bits 0 and 2 are set
# for TX1 and TX2 of PHY Lane 0. For a lane count of 4, bits 0 and 2 are set for TX1 and TX2 of both Lane 0 and Lane
# 1, where Lane 0 TX2 is equivalent to Lane 1 TX2 and Lane 0 TX1 is equivalent to Lane 1 TX1.
# format: {[lane count]: [Tx1, Tx2]}
gen15_LNL_expected_lane_commit_bit_native = {
    1: [1, 0],
    2: [1, 1],
    4: [1, 1]
}

# This table verifies the lane commit bit for offset 0xD71 in DP TC displays. When writing to TX1 or TX2 of PHY
# Lane 0 or PHY Lane 1, bit 0 or bit 2, respectively, of register 0xD71 (lane_commit_bit) is set to 1. According to
# the PHY Lane and Transmitter Usage table provided in https://gfxspecs.intel.com/Predator/Home/Index/68960,
# if the lane count is 1, only bit 2 is set for TX2 of PHY Lane 0. For a lane count of 2, both bits 0 and 2 are set
# for TX1 and TX2 of PHY Lane 0. For a lane count of 4, bits 0 and 2 are set for TX1 and TX2 of both Lane 0 and Lane
# 1, where Lane 0 TX2 is equivalent to Lane 1 TX2 and Lane 0 TX1 is equivalent to Lane 1 TX1.
# format: {[lane count]: [Tx1, Tx2]}
gen15_LNL_expected_lane_commit_bit_type_c = {
    1: [0, 1],
    2: [1, 1],
    4: [1, 1]
}


DPCD_OFFSET_TRAINING_LANE_SET = [0x103, 0x104, 0x105, 0x106]
DPCD_OFFSET_TRAINING_LANE_SET_LTTPR = [0xF0011, 0xF0012, 0xF0013, 0xF0014]
MAIN_LINK_CHANEL_CODING_CAP = 0X00006
DPCD_OFFSET_LTTPR = 0xF0000
VSWING_LEVEL_SET = 0x3
PREEMP_LEVEL_SET = 0x18
FFE_PRESET_SET_MASK = 0xF


ICL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX = 0
ICL_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX = 1
ICL_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX = 2
ICL_MGPHY_VSWING_INDEX = 3

TGL_COMBO_PHY_VSWING_UPTO_HBR_INDEX = 0
TGL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX = 1
TGL_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX = 2
TGL_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX = 3
TGL_DKL_PHY_VSWING_UPTO_HBR_INDEX = 4
TGL_DKL_PHY_VSWING_UPTO_HBR3_INDEX = 5

DG1_COMBO_PHY_VSWING_UPTO_HBR_INDEX = 0
DG1_COMBO_PHY_VSWING_UPTO_HBR2_INDEX = 1
DG1_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX = 2
DG1_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX = 3

ADLP_COMBO_PHY_VSWING_UPTO_HBR_INDEX = 0
ADLP_COMBO_PHY_VSWING_UPTO_HBR2_HBR3_INDEX = 1
ADLP_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX = 2
ADLP_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX = 3
ADLP_DKL_PHY_VSWING_INDEX_UPTO_HBR_INDEX = 4
ADLP_DKL_PHY_VSWING_INDEX_HBR2_INDEX = 5

RKL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX = 0
RKL_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX = 1
RKL_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX = 2
RKL_DKL_PHY_VSWING_INDEX = 3

ADLS_COMBO_PHY_VSWING_UPTO_HBR_INDEX = 0
ADLS_COMBO_PHY_VSWING_UPTO_HBR2_INDEX = 1
ADLS_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX = 2
ADLS_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX = 3
