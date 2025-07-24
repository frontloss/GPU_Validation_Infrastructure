##
# @file         per_process_helper.py
# @brief        This script contains helper functions that will be used by Per Process test scripts
# @author       Joshi, Prateek

from enum import Enum


##
# @brief    Contains helper function for feature mapping of application with gaming feature
class FeatureMapping(Enum):
    FLIPAT_SMOOTHSYNC = {'FLIPAT': 'SMOOTH_SYNC'}

    CLASSICD3D_VSYNCON = {'CLASSICD3D': 'VSYNC_ON'}

    CLASSICD3D_VSYNCOFF = {'CLASSICD3D': 'VSYNC_OFF'}

    FLIPMODEL_SPEEDFRAME = {'FLIPMODELD3D12': 'SPEEDFRAME'}

    FLIPAT_CFPS = {'FLIPAT': 'CAPPED_FPS'}

    FLIPAT_VSYNCON_CLASSICD3D_SMOOTHSYNC = {'FLIPAT': 'VSYNC_ON',
                                            'CLASSICD3D': 'SMOOTH_SYNC'}

    FLIPAT_VSYNCOFF_CLASSICD3D_VSYNCON = {'FLIPAT': 'VSYNC_OFF',
                                          'CLASSICD3D': 'VSYNC_ON'}

    FLIPAT_SPEEDFRAME_FLIPMODEL_VSYNCON = {'FLIPAT': 'SPEEDFRAME',
                                           'FLIPMODELD3D12': 'VSYNC_ON'}

    FLIPMODEL_SPEEDFRAME_CLASSICD3D_CFPS = {'FLIPMODELD3D12': 'SPEEDFRAME',
                                            'CLASSICD3D': 'CAPPED_FPS'}

    FLIPAT_SMOOTHSYNC_CLASSICD3D_VSYNCON_FLIPMODEL_CFPS = {'FLIPAT': 'SMOOTH_SYNC',
                                                           'CLASSICD3D': 'VSYNC_ON',
                                                           'FLIPMODELD3D12': 'CAPPED_FPS'}
