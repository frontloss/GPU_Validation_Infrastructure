########################################################################################################################
# @file         mipi_timings.py
# @brief        This file contains helper functions for verifying if required register bits are programmed to enable
#               port sync in dual MIPI case.
# @author       Geesala, Sri Sumanth
########################################################################################################################
import importlib
import logging

from Libs.Feature.mipi import mipi_helper as _mipi_helper
from registers.mmioregister import MMIORegister


##
# @brief        Verifies if required register bits are programmed to enable port sync in dual MIPI case.
# @param[in]    mipi_helper - MipiHelper object containing VBT and helper fields and functions
# @param[in]    port - port name
# @return       None
def verify_timings(mipi_helper, port):
    panel_index = mipi_helper.get_panel_index_for_port(port)
    vbt_mipi_timings = _mipi_helper.VbtMipiTimings()
    vbt_mipi_timings.get_vbt_mipi_timings(mipi_helper.gfx_vbt, panel_index)
    vbt_mipi_timings.adjust_timings_for_mipi_config(mipi_helper, panel_index)

    # from VBT, get HACTIVE, Horizontal Sync Start, Horizontal sync end, HTOTAL, VACTIVE, Vertical Sync Start and Vertical Sync End, VTOTAL
    VBT_hactive = vbt_mipi_timings.hactive
    VBT_hsync_start = vbt_mipi_timings.hsync_start
    VBT_hsync_end = vbt_mipi_timings.hsync_end
    VBT_htotal = vbt_mipi_timings.htotal

    VBT_vactive = vbt_mipi_timings.vactive
    VBT_vsync_start = vbt_mipi_timings.vsync_start
    VBT_vsync_end = vbt_mipi_timings.vsync_end
    VBT_vtotal = vbt_mipi_timings.vtotal

    # all values programmed as zero based (first pixel is numbered 0. e.g: if hactive is 256, you program 255(256-1))

    ##
    # 1. compare HTOTAL with vbt :TRANS_HTOTAL[29:16]
    reg_trans_htotal = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL" + port, mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='TRANS_HTOTAL' + port, field='HTotal', expected=VBT_htotal,
                                       actual=(reg_trans_htotal.horizontal_total + 1))

    ##
    # 2. compare HACTIVE with vbt :TRANS_HTOTAL[13:0]
    # when transmitting an 18-bit RGB pixel format, the one-based size of hactive must be a multiple of 4 pixels
    trans_dsi_func_conf = importlib.import_module("registers.%s.TRANS_DSI_FUNC_CONF_REGISTER" % (mipi_helper.platform))
    reg_trans_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                                mipi_helper.platform)
    if ((reg_trans_dsi_func_conf.pixel_format == getattr(trans_dsi_func_conf,
                                                         "pixel_format_18_BIT_RGB__6_6_6_LOOSE") or
         reg_trans_dsi_func_conf.pixel_format == getattr(trans_dsi_func_conf,
                                                         "pixel_format_18_BIT_RGB__6_6_6_PACKED")) and
            (reg_trans_htotal.horizontal_active + 1) % 4 != 0):
        logging.error('FAIL: TRANS_DSI_FUNC_CONF_%s: Pixel format is RGB666, and hactive is not divisible by 4. '
                      'This is not allowed' % (port))
        mipi_helper.verify_fail_count += 1

    mipi_helper.verify_and_log_helper(register='TRANS_HTOTAL' + port, field='HActive', expected=VBT_hactive,
                                       actual=(reg_trans_htotal.horizontal_active + 1))

    ##
    # 3. compare VTOTAL with vbt :TRANS_VTOTAL[28:16]
    reg_trans_vtotal = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL" + port, mipi_helper.platform)
    mipi_helper.verify_and_log_helper(register='TRANS_VTOTAL' + port, field='VTotal', expected=VBT_vtotal,
                                       actual=(reg_trans_vtotal.vertical_total + 1))

    ##
    # 4. compare VACTIVE with vbt :TRANS_VTOTAL[12:0]
    mipi_helper.verify_and_log_helper(register='TRANS_VTOTAL' + port, field='VActive', expected=VBT_vactive,
                                       actual=(reg_trans_vtotal.vertical_active + 1))

    # TRANS_*SYNC programmed only for video mode
    if (mipi_helper.get_mode_of_operation(panel_index) == _mipi_helper.VIDEO_MODE):
        ##
        # 5. compare 'Horizontal Sync Start' with vbt :TRANS_HSYNC[12:0] (hactive+hfp -1)
        reg_trans_hsync = MMIORegister.read("TRANS_HSYNC_REGISTER", "TRANS_HSYNC" + port, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='TRANS_HSYNC' + port, field='HSync start', expected=VBT_hsync_start,
                                           actual=(reg_trans_hsync.horizontal_sync_start + 1))

        ##
        # 6. compare 'Horizontal Sync End' with vbt :TRANS_HSYNC[28:16] (hactive+hfp+hsync -1)
        mipi_helper.verify_and_log_helper(register='TRANS_HSYNC' + port, field='HSync end', expected=VBT_hsync_end,
                                           actual=(reg_trans_hsync.horizontal_sync_end + 1))

        ##
        # 7. compare 'Vertical Sync Start' with vbt :TRANS_VSYNC[12:0]
        reg_trans_vsync = MMIORegister.read("TRANS_VSYNC_REGISTER", "TRANS_VSYNC" + port, mipi_helper.platform)
        mipi_helper.verify_and_log_helper(register='TRANS_VSYNC' + port, field='VSync start', expected=VBT_vsync_start,
                                           actual=(reg_trans_vsync.vertical_sync_start + 1))

        ##
        # 8. compare 'Vertical Sync End' with vbt :TRANS_VSYNC[28:16]
        mipi_helper.verify_and_log_helper(register='TRANS_VSYNC' + port, field='VSync end', expected=VBT_vsync_end,
                                           actual=(reg_trans_vsync.vertical_sync_end + 1))
