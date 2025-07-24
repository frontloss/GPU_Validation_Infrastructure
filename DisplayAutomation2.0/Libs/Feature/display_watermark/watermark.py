######################################################################################
# @file         watermark.py
# @addtogroup   PyLibs_DisplayWatermark
# @brief        Python wrapper helper module to verify watermarks
# @author       Kumar V,Arun, Bhargav Adigarla
######################################################################################
import logging

from Libs.Core.test_env import test_context
from Libs.Feature.display_watermark import watermark_utils
from Libs.Core.logger import gdhm
GDHM_FEATURE_TAG = "[WM_DBUF]"

##
# Platform details for all connected adapters
PLATFORM_INFO = {
    gfx_index: {
        'gfx_index': gfx_index,
        'name': adapter_info.get_platform_info().PlatformName,
        #: system_utility.SystemUtility().is_ddrw(gfx_index=adapter_info.gfxIndex)
    }
    for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
}


##
# @brief        This class contains generic watermark and dbuf verification API
class DisplayWatermark(object):

    ##
    # @brief        Verifies watermark values programmed by driver for given adapter
    # @param[in]    is_48hz_test default with value False
    # @param[in]    gfx_index as optional arg with default value 'gfx_0'
    # @param[in]    min_dbuf_check as optional arg with default value False
    # @return       True if watermark verification was done on a minimum of 1 plane, else False
    def verify_watermarks(self, is_48hz_test=False, gfx_index='gfx_0', min_dbuf_check=False):

        # WA skipping watermark verification for Multiadapter Displays https://hsdes.intel.com/appstore/article/#/16016652551
        # This WA to be removed once the issue is fixed with MA
        if len(watermark_utils.gfx_display_hwinfo) > 1:
            logging.info("Skipping Watermark verifiation for MultiAdapter commandlines")
            return True


        status = False
        platform = PLATFORM_INFO[gfx_index]['name'].lower()
        logging.info('*********** [Platform: {0}] WATERMARK VERIFICATION STARTED ***********'.format(platform.upper()))
        wm_obj = self.__get_wm_obj(gfx_index)
        if wm_obj is not None:
            status = wm_obj.verify_watermarks(is_48hz_verification=is_48hz_test, gfx_index = gfx_index,
                                              min_dbuf_check=min_dbuf_check)
        logging.info('************ [Platform: {0}] WATERMARK VERIFICATION ENDED ************'.format(platform.upper()))
        return status

    ##
    # @brief        Get Watermark Object
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       None
    def __get_wm_obj(self, gfx_index='gfx_0'):
        platform = PLATFORM_INFO[gfx_index]['name'].lower()
        if platform in watermark_utils.GEN9_PLATFORMS:
            from Libs.Feature.display_watermark.gen9watermarks import Gen9Watermarks
            return Gen9Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN10_PLATFORMS:
            from Libs.Feature.display_watermark.gen10watermarks import Gen10Watermarks
            return Gen10Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN11_PLATFORMS:
            from Libs.Feature.display_watermark.gen11watermarks import Gen11Watermarks
            return Gen11Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN12_PLATFORMS:
            from Libs.Feature.display_watermark.gen12watermarks import Gen12Watermarks
            return Gen12Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN13_PLATFORMS:
            from Libs.Feature.display_watermark.gen13watermarks import Gen13Watermarks
            return Gen13Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN14_PLATFORMS:
            from Libs.Feature.display_watermark.gen14watermarks import Gen14Watermarks
            return Gen14Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN15_PLATFORMS:
            from Libs.Feature.display_watermark.gen15watermarks import Gen15Watermarks
            return Gen15Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN16_PLATFORMS:
            from Libs.Feature.display_watermark.gen16watermarks import Gen16Watermarks
            return Gen16Watermarks(gfx_index=gfx_index)
        elif platform in watermark_utils.GEN17_PLATFORMS:
            from Libs.Feature.display_watermark.gen17watermarks import Gen17Watermarks
            return Gen17Watermarks(gfx_index=gfx_index)
        else:
            logging.error('Platform not defined for Watermark verification')
            gdhm.report_test_bug_os(f"{GDHM_FEATURE_TAG} Platform not defined for Watermark Verification")
            return None
