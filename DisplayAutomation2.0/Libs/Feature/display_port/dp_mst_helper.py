######################################################################################################################
# @file         dp_mst_helper.py
# @brief        Contains All the Helper Functions For DP MST Related Tests and Verification
#
# @author       Balaji Gurusamy
#######################################################################################################################
import logging

from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import dp_mst
from Libs.Core import system_utility
from Libs.Core.machine_info import machine_info
from Libs.Core.display_config import display_config

DP_HOTPLUG_GOLDEN_VALUE = 0x00000001

DELAY_5000_MILLISECONDS = 15000
DELAY_1000_MILLISECONDS = 1000.0
ZERO = 0
FOUR = 4
RESUME_TIME = 30
HZRES_4K = 3840
VERRES_2K = 2160
HZRES_2560 = 2560
VERRES_1600 = 1600
HZRES_1920 = 1920
VERRES_1080 = 1080
HZRES_5K = 5120
VERRES_3K = 2880
HZRES_8K = 7680
VERRES_4K = 4320
REFRESH_RATE_60 = 60
REFRESH_RATE_96 = 96
REFRESH_RATE_120 = 120


##
# @brief        Class method that contains DP MST related helper functions are required.
class DPMSTHelper:

    ##
    # @brief        Method to initialize above class when object is created
    def __init__(self):
        self.display_config_obj = display_config.DisplayConfiguration()
        self.machine_info = machine_info.SystemInfo()
        self.system_utility = system_utility.SystemUtility()
        self.mst_lib = dp_mst.DisplayPort()

    ##
    # @brief        This is exposed API to verify topology between CUI and Driver
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    action
    #                   Valid actions include ['PLUG', 'UNPLUG']
    # @return       boolean.
    def verify_mst_topology(self, port_type, action="PLUG"):
        if action not in ['PLUG', 'UNPLUG']:
            logging.error("[Test Issue]: Invalid plug action for display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Invalid plug action-'{}' received for display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
        # Topology verification is dependant on CUI SDK API's
        if not self.system_utility.is_ddrw():
            ret_status = self.mst_lib.verify_topology(port_type)
        else:
            # In Yangra driver CUI is not supported hence
            # making verification success by default
            if action == 'PLUG':
                ret_status = ZERO
            else:
                ret_status = FOUR
        if action == 'PLUG' and ret_status == ZERO:
            logging.info("MST Topology Verification Success, Applied and Expected topologies are matching")
        elif action == 'UNPLUG' and ret_status == FOUR:
            logging.info("MST Topology Verification Success: HPD(UNPLUG) event")
        else:
            try:
                logging.error(
                    "MST Topology Verification Failed..Status Code:%s" % dp_mst.TOPOLOGY_STATUS_CODE(ret_status).name)
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] MST Topology verification Failed with Status Code: {}".
                        format(dp_mst.TOPOLOGY_STATUS_CODE(ret_status).name),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return False
            except ValueError as Error:
                logging.error("MST Topology Verification Failed.. No Matching Status Code Fund...%s" % Error)
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] MST Topology verification Failed with unknown error code",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return False

        return True

    ##
    # @brief        This method verifies whether tiled mode (tiled could be enabled/disabled in panel OSD) applied
    #               successfully or not
    # @param[in]    tiled_target_id: int
    #                   Target id of the tiled display
    # @param[in]    is_tiled: bool
    #                   This flag indicates whether panel is tiled or not.True if tiled, False otherwise
    # @param[in]    is_sst_master_only: bool
    #                   This flag Indicates whether only master tile of SST panel is plugged
    # @return       boolean
    def verify_tiled_nontiled_mode(self, tiled_target_id, is_tiled, is_sst_master_only):
        # Extract Native X, Y and RR from EDID
        native_x_resolution, native_y_resolution, native_rr = 0, 0, 0
        native_mode = self.display_config_obj.get_native_mode(tiled_target_id)
        if native_mode is not None:
            native_x_resolution = native_mode.hActive
            native_y_resolution = native_mode.vActive
            native_rr = native_mode.refreshRate
        logging.info("Native mode details of %d panel: %sx%s@%s" % (tiled_target_id, native_x_resolution,
                                                                    native_y_resolution, native_rr))

        # Get the currently applied mode from Graphics driver.
        current_mode = self.display_config_obj.get_current_mode(tiled_target_id)
        logging.info("Current mode details of %d panel: %sx%s@%s" % (tiled_target_id, current_mode.HzRes,
                                                                     current_mode.VtRes, current_mode.refreshRate))

        # Verify whether it is tiled display or not
        if is_tiled:
            # Tiled display found! Get the corresponding tiled information
            tile_info = self.mst_lib.get_tiled_display_information(tiled_target_id)

            # Verify tiled display's X, Y present in the tiled information variable
            if tile_info.TiledStatus:
                tiled_x_resolution = tile_info.HzRes
                tiled_y_resolution = tile_info.VtRes
            else:
                logging.error("Tiled information not available in the Tiled display. Exiting ...")
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] DP Tiled tests are running on non-tiled display",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return False

            tiled_rr = native_rr  # Tiled RR is same as native resolution's RR
            logging.info("%d is Tiled panel with mode details: %sx%s@%s" % (tiled_target_id, tiled_x_resolution,
                                                                            tiled_y_resolution, tiled_rr))

            '''
                Algorithm to verify whether current and expected modes are identical or not.
            '''

            # Sometimes RR b/w Gfx driver and EDID may vary by ~1-5%. We consider RRs are same if diff b/w RRs are
            # max deviated by 5%
            # FIXME:    Commenting below lines due to https://hsdes.intel.com/resource/1606760328
            #           difference = abs(tiled_rr - current_mode.refreshRate)
            #           max_refresh_rate = max(tiled_rr,current_mode.refreshRate)
            #           diff_in_percentage = (float(difference)/max_refresh_rate) * 100

            # TODO:     For now X and Y are hard-coded to 4k & 2k respectively for 5k3k SST tiled panel but ideally,
            #           when master port only connected, Driver sets mode present in the CEA DTD timing. Currently,
            #           system utility library doesn't supports API to read timings from CEA block. Once, CEA block
            #           parsing support added, we will remove this hard-coding.

            gfx_display_hw_info_list = self.machine_info.get_gfx_display_hardwareinfo()
            if len(gfx_display_hw_info_list) != 0:
                platform_name = gfx_display_hw_info_list[0].DisplayAdapterName
            else:
                logging.error('Failed to get Platform Name. Exiting...')
                return False

            # Restrict the Max Resolution based on the panel capability as well as platform.
            if is_sst_master_only or platform_name == 'LKF1':
                tiled_x_resolution = HZRES_4K
                tiled_y_resolution = VERRES_2K

            # Verify whether current and expected modes are identical or not
            if current_mode.HzRes == tiled_x_resolution and current_mode.VtRes == tiled_y_resolution:
                logging.info("Tiled mode (enumerated by Gfx driver) and expected tiled mode (as per EDID) are "
                             "identical: %sx%s@%s" % (current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate))
            else:
                logging.error(
                    "[Driver Issue]: Tiled mode (enumerated by Gfx driver): %sx%s@%s and expected tiled mode (as per EDID): "
                    "%sx%s@%s are different!" % (current_mode.HzRes, current_mode.VtRes,
                                                 current_mode.refreshRate, tiled_x_resolution,
                                                 tiled_y_resolution, tiled_rr))
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Tiled Mode enumerated by Driver({}x{}@{}) and"
                          " Tiled EDID mode({}x{}@{}) are not matching".
                        format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, tiled_x_resolution,
                               tiled_y_resolution, tiled_rr),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return False

        # Tiled mode disabled! It is tiled panel but tiled mode disabled in the panel OSD
        else:
            '''
                Algorithm to verify whether current and expected modes are identical or not.
            '''
            # As the RR between driver and EDID may vary, we consider RRs are same if differences b/w RRs is
            # max 5% deviation
            # FIXME:    Commenting below lines due to https://hsdes.intel.com/resource/1606760328
            #           difference = abs(native_rr - current_mode.refreshRate)
            #           max_refresh_rate = max(native_rr,current_mode.refreshRate)
            #           diff_in_percentage = (float(difference)/max_refresh_rate) * 100

            # TODO:     For now XxYxRR are hard-coded to 4kx2k@60 for 4k2k MST tiled panel but ideally,
            #           when MST is disabled, driver sets mode present in the CEA DTD timing. Currently, system utility
            #           library doesn't supports API to read timings from CEA  block. Once, CEA block parsing support
            #           added, we will remove this hard-coding.

            tiled_mst_disable_h_res = HZRES_4K
            tiled_mst_disable_v_res = VERRES_2K
            tiled_mst_disable_rr = 30

            if current_mode.HzRes == native_x_resolution and current_mode.VtRes == native_y_resolution:
                logging.info("MST tiled disabled mode (enumerated by Gfx driver) and expected tiled disabled mode "
                             "(as per EDID) are identical")
            else:
                logging.error(
                    "[Driver Issue]: MST tiled disabled mode (enumerated by Gfx driver): %sx%s@%s and expected tiled disabled"
                    " mode (as per EDID): %sx%s@%s are different!" % (current_mode.HzRes, current_mode.VtRes,
                                                                      current_mode.refreshRate,
                                                                      tiled_mst_disable_h_res,
                                                                      tiled_mst_disable_v_res,
                                                                      tiled_mst_disable_rr))
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] MST Tiled disabled Mode enumerated by Driver({}x{}@{}) and"
                          " Tiled disabled EDID mode({}x{}@{}) are not matching".
                        format(current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate,
                               tiled_mst_disable_h_res, tiled_mst_disable_v_res, tiled_mst_disable_rr),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return False
        return True

    ##
    # @brief        This method Verifies tiled/non-tiled applied successfully or not
    # @param[in]    is_mst: bool
    #                   Flag indicating MST or SST tiled mode. TRUE indicates MST mode and FALSE indicates SST mode
    # @param[in]    mst_status: bool
    #                   Flag indicates whether MST enabled or disabled in panel OSD
    # @param[in]    is_sst_master_only: bool
    #                   Indicates only master tile of SST panel is plugged
    # @param[in]    tiled_target_id: int
    #                   Target id of the tiled display
    # @return       boolean
    # @note         Below verify_tiled_mode is generic function which should work for both SST and MST tiled modes.
    #               Currently DFT based SST tiled simulation uses different function verify_tiled_mode
    #               (Display_Port/DP_Tiled/display_port_base.py).Ensure to switch to below new function when moving from
    #               DFT based to Simulation driver based approach.

    def verify_tiled_display(self, is_mst, mst_status, is_sst_master_only, tiled_target_id):
        if is_mst is False:
            # Set flag is_sst_master_only to FALSE to indicate we are in SST path
            logging.info("Plugged panel %d is SST tiled" % tiled_target_id)
            status = self.verify_tiled_nontiled_mode(tiled_target_id, True, is_sst_master_only)

        # is_MST TRUE means, we are in MST tiled path
        else:
            # Set flag is_sst_master_only to TRUE to indicate we are in MST path
            is_sst_master_only = True

            # Its MST panel and MST is enabled in panel's OSD
            if mst_status:
                logging.info("Plugged panel %d is MST tiled and MST is enabled in panel OSD" % tiled_target_id)
                # Tiled modes verification algorithm is same for both SST and MST tiled (with MST enabled in panel OSD)
                status = self.verify_tiled_nontiled_mode(tiled_target_id, True, is_sst_master_only)

            # Its MST panel but MST is disabled in panel's OSD
            else:
                # If we hit ELSE logic means, plugged panel is MST tiled but MST disabled in panel OSD
                logging.info("Plugged panel %d is MST tiled but MST is disabled in panel OSD" % tiled_target_id)
                status = self.verify_tiled_nontiled_mode(tiled_target_id, False, is_sst_master_only)

        return status

    ##
    # @brief        This method gets list of all tiled display's target ids attached to the system.
    # @return       Boolean value, List of tiled target ids: bool, list
    #                   returns boolean value with list of target ids
    def get_tiled_displays_list(self):
        tiled_display_found = False

        # List to hold list of all tiled display's target ids
        tiled_target_ids_list = []

        # List to hold list of all non-tiled display's target ids
        nontiled_target_ids_list = []

        # get the current display config from DisplayConfig
        config = self.display_config_obj.get_all_display_configuration()

        for index in range(config.numberOfDisplays):

            # Get target id of the display
            target_id = config.displayPathInfo[index].targetId

            # Get tiled information if display associated with target id is Tiled display
            tile_info = self.mst_lib.get_tiled_display_information(target_id)

            # Check for tiled status
            if tile_info.TiledStatus:
                # Tiled display found! append to the list
                tiled_target_ids_list.append(target_id)
                tiled_display_found = True

            else:
                # Tiled display found! append to the list
                nontiled_target_ids_list.append(target_id)

        if tiled_display_found:
            # If at least one tiled display found, then return TRUE and list containing tiled target ids to the caller
            return True, tiled_target_ids_list

        else:
            # Tiled display(s) not found! Return FALSE to the caller
            return False, nontiled_target_ids_list

    ##
    # @brief        This is exposed API to Read DPCD from the offset
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    nativeDPCDRead: bool
    #                   True for Native DPCD read, False otherwise
    # @param[in]    length: int
    #                   length of DPCD Values to be read
    # @param[in]    addr: str
    #                   DPCD offset
    # @param[in]    node_rad: object
    #                   MST Relative address object
    # @param[in]    action: str
    #                   Valid DPCD actions include ['PLUG', 'VERSION', 'MST_CAP']
    # @return       dpcd_reg_val[0]: str
    #                   Return the register value
    def dpcd_read(self, port_type, nativeDPCDRead, length, addr, node_rad, action="PLUG"):
        action = action.upper()
        if action not in ['PLUG', 'VERSION', 'MST_CAP']:
            logging.error("Invalid dpcd action for display. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Invalid dpcd action-'{}' received for display".format(action),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None
        dpcd_flag, dpcd_reg_val = self.mst_lib.read_dpcd(port_type, nativeDPCDRead, length, addr, node_rad)

        if action == 'PLUG' and dpcd_flag:
            logging.info("DPCD Read Value: %s" % (dpcd_reg_val[0]))
            reg_val = dpcd_reg_val[0] & 0x000000FF
            if reg_val == DP_HOTPLUG_GOLDEN_VALUE:
                logging.info("DPCD read successful for Hotplug: Register Value: %s" % reg_val)
            else:
                logging.error("DPCD Flag:%s & Register value:%s during DPCD Read Failure" % (dpcd_flag, reg_val))
                logging.error("DPCD read failed for Hotplug. Exiting ...")
                gdhm.report_bug(
                    title="[Interfaces][DP_MST] Unexpected reg value {} at register {} during Hotplug ".
                          format(reg_val, hex(addr)),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return None

        elif action == 'VERSION' and dpcd_flag:
            logging.info("DPCD Version Value: %x" % dpcd_reg_val[0])
            return dpcd_reg_val[0]

        elif action == 'MST_CAP' and dpcd_flag:
            logging.info("DPCD MST CAP offset 0x21 Value: %x" % dpcd_reg_val[0])
            return dpcd_reg_val[0]

        else:
            logging.error("Read DPCD api Failed, Exiting ...")
            # Gdhm bug reporting should be handled in display_port.read_dpcd
            return None
