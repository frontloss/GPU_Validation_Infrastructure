using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using log4net;


namespace Intel.VPG.Display.FlickerTestSuite.MPO
{
    public sealed class ULTInterface:IMPODevice
    {
        private static readonly ILog logger = LogManager.GetLogger(typeof(ULTInterface));

        //Below constansts should be based on Gen.
        public const int MAX_PLANES = 13;
        public const int MAX_PIPES = 3;
        List<char> pipes = new List<char>();

        ULT_MPO_CAPS _mpo_caps = new ULT_MPO_CAPS();
        CHECKMPOSUPPORT_RETURN_INFO checkMpoSupportReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
        ULT_MPO_GROUP_CAPS _mpo_group_caps = new ULT_MPO_GROUP_CAPS();
        uint _source_id = 0;
        uint _monitor_id = 0;

        public ULTInterface(uint source_id, uint monitorId)
        {
            _source_id = source_id;
            _monitor_id = monitorId;
            pipes.Add('0');
        }

        #region Private methods

        private void Update_Status(bool status)
        {
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.bEnableULT = status;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                logger.ErrorFormat("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }

        private void EnableFeature(bool status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = status;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                logger.ErrorFormat("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }

        private void EnableULT()
        {
            this.Update_Status(true);
        }

        private void DisableULT()
        {
            this.Update_Status(false);
        }

        private bool Get_Caps()
        {
            ULT_ESC_MPO_CAPS_ARGS ult_Esc_Args = new ULT_ESC_MPO_CAPS_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS;
            ult_Esc_Args.ulVidpnSourceID = this._source_id;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                logger.ErrorFormat("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                _mpo_caps = ult_Esc_Args.stMPOCaps;
                return true;
            }
            return false;
        }


        private bool Get_Group_Caps(uint groupIndex)
        {
            ULT_MPO_GROUP_CAPS_ARGS ult_Esc_Args = new ULT_MPO_GROUP_CAPS_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS;
            ult_Esc_Args.ulVidpnSourceID = this._source_id;
            ult_Esc_Args.uiGroupIndex = groupIndex;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                logger.ErrorFormat("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                _mpo_group_caps = ult_Esc_Args.stMPOGroupCaps;
                return true;
            }
            return false;
        }


        private void Check(SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] sbMpoCheckMpoSupportPathInfo, uint numPaths, uint config, ref bool supported, ref uint failureReason, ref CHECKMPOSUPPORT_RETURN_INFO checkMpoSupportReturnInfo)
        {
            SB_MPO_CHECKMPOSUPPORT_ARGS ult_Esc_Args = new SB_MPO_CHECKMPOSUPPORT_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.dwSourceID = 0;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CHECK_MPO;
            ult_Esc_Args.stCheckMPOPathInfo = sbMpoCheckMpoSupportPathInfo;
            ult_Esc_Args.ulNumPaths = numPaths;
            ult_Esc_Args.ulConfig = config;
            ult_Esc_Args.stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CHECK_MPO, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
            {
                logger.ErrorFormat("CheckMPO call failed : {0}", ult_Esc_Args.eULTEscapeCode);
                supported = false;
            }
            else
            {
                failureReason = ult_Esc_Args.ulFailureReason;
                supported = ult_Esc_Args.bSupported;
                checkMpoSupportReturnInfo = ult_Esc_Args.stMPOCheckSuppReturnInfo;
            }
        }

        private MPO_FLIP_PLANE_INFO[] Prepare_PlaneFlipInfo(List<MPOPlane> planes)
        {
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];
            int plane_index = 0;

            foreach (MPOPlane plane in planes)
            {
                mpoFlipPlaneInfo[plane_index].uiLayerIndex = plane.Zorder;
                mpoFlipPlaneInfo[plane_index].bEnabled = plane.Enabled;
                mpoFlipPlaneInfo[plane_index].bAffected = plane.Affected;
                mpoFlipPlaneInfo[plane_index].stPlaneAttributes = plane.Attributes;
                mpoFlipPlaneInfo[plane_index].stPlaneAttributes.DIRTYRECTS = new ULT_M_RECT[8];
                mpoFlipPlaneInfo[plane_index].hAllocation = plane.Get_Buffer();
                plane_index++;
            }

            return mpoFlipPlaneInfo;
        }

        #endregion


        #region Interfaces

        void IMPODevice.Init()
        {
            this.EnableULT();
            this.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            this.Get_Caps();
            this.Get_Group_Caps(0);
        }

        bool IMPODevice.CheckMPO(List<MPOPlane> planes)
        {
            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];

            for (int i = 0; i < pipes.Count; i++)
            {
                stCheckMpoSupportPathInfo[i].uiPlaneCount = Convert.ToUInt32(planes.Count);
                ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];
                int plane_index = 0;

                foreach (MPOPlane plane in planes)
                {
                    stCheckMpoSupportPlaneInfo[plane_index].uiLayerIndex = plane.Zorder;
                    stCheckMpoSupportPlaneInfo[plane_index].bEnabled = plane.Enabled;
                    stCheckMpoSupportPlaneInfo[plane_index].bIsAsyncMMIOFlip = plane.IsAsyncMMIOFlip;
                    stCheckMpoSupportPlaneInfo[plane_index].stPlaneAttributes = plane.Attributes;
                    stCheckMpoSupportPlaneInfo[plane_index].eSBPixelFormat = plane.Format;
                    stCheckMpoSupportPlaneInfo[plane_index].stSurfaceMemInfo = plane.Source.SurfaceMemOffsetInfo;
                    plane_index++;
                }
                stCheckMpoSupportPathInfo[i].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;
            }
            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            this.Check(stCheckMpoSupportPathInfo,
                                numPaths, 1,
                                ref supported,
                                ref failureReason,
                                ref stMPOCheckSuppReturnInfo);
            return supported;
        }

        bool IMPODevice.Blend(List<MPOPlane> planes, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag)
        {
            bool result = false;
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = Prepare_PlaneFlipInfo(planes);
            ULT_SET_SRC_ADD_MPO_ARG ult_Esc_Args = new ULT_SET_SRC_ADD_MPO_ARG();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO;
            ult_Esc_Args.stDxgkMPOPlaneArgs = mpoFlipPlaneInfo;
            ult_Esc_Args.ulNumPlanes = (uint)planes.Count;
            ult_Esc_Args.ulFlags = Flag;
            ult_Esc_Args.dwSourceID = this._source_id;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
            {
                result = false;
            }
            else
            {
                result = true;
            }
            return result;
        }

        void IMPODevice.DeInit()
        {
            logger.DebugFormat("Release all memory resources");
            MemoryPool.Free();                    
            this.EnableFeature(false, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            this.DisableULT();
        }

        #endregion

    }
}
