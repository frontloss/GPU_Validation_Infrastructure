using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Specialized;
using System.IO;
using Microsoft.Win32.SafeHandles;

namespace Intel.VPG.Display.FlipsInterface.MPO
{
    public sealed class DivaInterface : IDisposable
    {
        //private static readonly ILog logger = LogManager.GetLogger(typeof(DivaInterface));
        DivaUtilityCLR divaUtility;
        SafeFileHandle hDivaDevice;
        DivaDisplayFeatureUtilityCLR objDivaDispFeatureUtil = null;
        uint _source_id = 0;
        uint _monitor_id = 0;
        bool dftEnabled = false;

        public DivaInterface(uint source_id, uint monitorId)
        {
            // Create CLR-Utility handle
            divaUtility = new DivaUtilityCLR();

            // Extract Version info of DIVA Device
            DIVA_VERSION_INFO_CLR newVersion = new DIVA_VERSION_INFO_CLR();
            divaUtility.GetDivaVersion(newVersion);
            //logger.InfoFormat("DIVA Version - 0x{0:X}", newVersion.Version);

            hDivaDevice = divaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice);
            _source_id = source_id;
            _monitor_id = monitorId;
        }

        ~DivaInterface()
        {
            divaUtility.Dispose();
        }


        public void EnableDFT()
        {
            this.Enable(true, this._source_id);
            dftEnabled = true;
            DivaInterface.ConfigureUnderRun(true);
        }


        public void CreateResourceDIVA(DIVA_CREATE_RES_ARGS_CLR createRes)
        {
            // Create 'Generic GFX Access DIVA CLR Utility'
            using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
            {
                objDivaDispFeatureUtil.CreateResource(createRes);
            }
        }


        public void FreeResourceDIVA(UInt64 pGmmBlock)
        {
            //logger.InfoFormat("Free resource for {0}", pGmmBlock.ToString());

            using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
            {
                objDivaDispFeatureUtil.FreeResource(pGmmBlock);
            }
        }


        public DIVA_MPO_CAPS_ARGS_CLR GetMPOCaps()
        {
            DIVA_MPO_CAPS_ARGS_CLR args = new DIVA_MPO_CAPS_ARGS_CLR();
            args.VidpnSourceID = this._source_id;

            using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
            {
                objDivaDispFeatureUtil.GetMPOCaps(args);
            }

            return args;
        }


        public DIVA_MPO_GROUP_CAPS_ARGS_CLR GetGroupMPOCaps(UInt32 groupIndex)
        {

            DIVA_MPO_GROUP_CAPS_ARGS_CLR args = new DIVA_MPO_GROUP_CAPS_ARGS_CLR();
            args.GroupIndex = groupIndex;
            args.VidpnSourceID = this._source_id;

            using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
            {
                objDivaDispFeatureUtil.GetMPOGroupCaps(args);
            }

            return args;
        }


        public bool CheckMPO(List<MPOPlane> planes)
        {
            // Create CLR-Utility handle
            bool result = false;

            List<DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR> testPlanes = Helper.MarshalPlaneData(ref planes);

            try
            {
                DIVA_CHECK_MPO_ARGS_CLR args = new DIVA_CHECK_MPO_ARGS_CLR();
                DIVA_MPO_CHECKMPOSUPPORT_PATH_INFO_CLR[] stCheckMpoSupportPathInfo = new DIVA_MPO_CHECKMPOSUPPORT_PATH_INFO_CLR[0];
                args.SourceID = this._source_id;
                args.Supported = 0;
                args.NumPaths = 1;
                args.Config = 1;

                for (int i = 0; i < args.CheckMPOPathInfo.Length; i++)
                {
                    int plane_index = 0;
                    args.CheckMPOPathInfo[i].PlaneCount = Convert.ToUInt32(planes.Count);

                    foreach (DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR plane in testPlanes)
                    {
                        args.CheckMPOPathInfo[i].pMPOPlaneInfo[plane_index] = plane;
                        plane_index++;
                    }
                }

                using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
                {
                    objDivaDispFeatureUtil.CheckMPO(args);
                }

                //logger.InfoFormat("DivaInterface::Checkmpo supported = {0}", args.Supported);
                result = (args.Supported == 1);
            }
            catch (Exception ex)
            {
                //logger.ErrorFormat("DivaInterface::CheckMPO: Error occurred - {0}", ex.Message);
                //logger.Error(ex.StackTrace);
            }
            return result;
        }


        public bool SetSrcAddressMPO(List<MPOPlane> planes, DIVA_SETVIDPNSRCADDR_FLAGS_CLR Flag)
        {
            bool result = false;
            List<DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR> testPlanes = Helper.MarshalPlaneData(ref planes);

            try
            {
                DIVA_SET_SRC_ADD_MPO_ARGS_CLR args = new DIVA_SET_SRC_ADD_MPO_ARGS_CLR();
                args.SourceID = this._source_id;
                args.NumPlanes = (uint)planes.Count;
                args.Flags = Flag;
                args.NumPlanes = Convert.ToUInt32(planes.Count);

                for (int i = 0; i < testPlanes.Count; i++)
                {
                    DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR plane = testPlanes[i];
                    args.DxgkMPOPlaneArgs[i].pPlaneAttributes = plane.pPlaneAttributes;
                    args.DxgkMPOPlaneArgs[i].Enabled = (byte)((planes[i].Enabled == true) ? 1 : 0);
                    args.DxgkMPOPlaneArgs[i].Affected = (byte)((planes[i].Affected == true) ? 1 : 0);
                    args.DxgkMPOPlaneArgs[i].LayerIndex = plane.LayerIndex;
                    args.DxgkMPOPlaneArgs[i].Allocation = planes[i].Get_Buffer();
                }

                using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
                {
                    objDivaDispFeatureUtil.SetSrcAddressMPO(args);
                }
                //logger.Info("DivaInterface::Set source address done");
                result = true;
            }
            catch (Exception ex)
            {
                //logger.ErrorFormat("DivaInterface::SetSrcAddrMPO: Error occurred - {0}", ex.Message);
                //logger.Error(ex.StackTrace);
            }
            return result;
        }


        public void Enable(bool bEnable, uint sourceid)
        {
            if (bEnable == true)
            {
                using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
                {
                    DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR fwArgs = new DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR();
                    fwArgs.EnableFramework = true;
                    objDivaDispFeatureUtil.EnableDisableFramework(fwArgs);

                    DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR featureArgs = new DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR();
                    featureArgs.EnableFeature = true;
                    featureArgs.FeatureType = DIVA_DISPLAY_FEATURE_TYPE_CLR.PRIVATE_MPOFLIP;
                    objDivaDispFeatureUtil.EnableDisableFeature(featureArgs);
                }

                //logger.Info("DivaInterface::Enabled MPO successfully !");
            }
            else
            {                
                using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
                {
                    DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR featureArgs = new DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR();
                    featureArgs.EnableFeature = false;
                    featureArgs.FeatureType = DIVA_DISPLAY_FEATURE_TYPE_CLR.PRIVATE_MPOFLIP;
                    objDivaDispFeatureUtil.EnableDisableFeature(featureArgs);

                    DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR fwArgs = new DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR();
                    fwArgs.EnableFramework = false;
                    objDivaDispFeatureUtil.EnableDisableFramework(fwArgs);
                }
                //logger.Info("DivaInterface::Disabled MPO successfully !");
            }
        }


        public bool SetSrcAddr(DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR plane, UInt64 pGmmBlock)
        {
            bool result = false;

            if (plane == null || pGmmBlock == 0)
            {
                throw new Exception("DivaInterface::Oops, Invalid set source address parameters");
            }

            try
            {
                DIVA_SET_SRC_ADD_ARGS_CLR args = new DIVA_SET_SRC_ADD_ARGS_CLR();

                args.SrcID = this._source_id;
                args.GmmBlock = pGmmBlock;
                args.Flags = DIVA_SETVIDPNSRCADDR_FLAGS_CLR.DIVA_SETVIDPNSRCADDR_FLAG_FLIPIMMEDIATE;

                using (objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice))
                {
                    objDivaDispFeatureUtil.SetSrcAddress(args);
                }
                //logger.Info("DivaInterface::Set source address done");
                result = true;
            }
            catch (Exception ex)
            {
                //ErrorFormat("DivaInterface::SetSrcAddrMPO: Error occurred - {0}", ex.Message);
                //logger.Error(ex.StackTrace);
            }
            return result;
        }


        public static void ConfigureUnderRun(bool bEnable)
        {
            // Create CLR-Utility handle
            using (DivaUtilityCLR DivaUtility = new DivaUtilityCLR())
            {
                // Extract Version info of DIVA Device
                DIVA_VERSION_INFO_CLR newVersion = new DIVA_VERSION_INFO_CLR();
                DivaUtility.GetDivaVersion(newVersion);
                //logger.InfoFormat("DivaInterface::DIVA Version - 0x{0:X}", newVersion.Version);
                // Get DIVA device handle
                SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

                // Create 'Generic GFX Access DIVA CLR Utility'
                DivaDisplayFeatureUtilityCLR objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice);
                DIVA_PIPE_UNDER_RUN_ARGS_CLR pipe_under = new DIVA_PIPE_UNDER_RUN_ARGS_CLR();
                pipe_under.Enable = bEnable;
                pipe_under.UnderRunEventType = DIVA_UNDER_RUN_EVENTS_CLR.DIVA_UNDERRUN_ALL_PIPE_CLR;
                objDivaDispFeatureUtil.ConfigureGfxPipeUnderRun(pipe_under);
            }
        }


        public uint ReadRegister(uint offset)
        {
            using (DivaGenericGfxAccessUtilityCLR objGfxUtil = new DivaGenericGfxAccessUtilityCLR(hDivaDevice))
            {
                DIVA_MMIO_ACCESS_ARGS_CLR args = new DIVA_MMIO_ACCESS_ARGS_CLR();
                args.Offset = offset;
                args.Value = 0;
                objGfxUtil.ReadMmio(args);
                return args.Value;
            }
        }


        public void DisableDFT()
        {
            GMMPool.FreePool();
            this.Enable(false, this._source_id);
            DivaInterface.ConfigureUnderRun(false);
            dftEnabled = false;
        }


        public void Dispose()
        {
            if (dftEnabled == true)
            {
                this.DisableDFT();
            }
            GC.SuppressFinalize(this);
        }


        public static bool CheckUnderRun()
        {
            bool result = false;

            //if (ConfigItem.UnderRunCheck() == true)
            {
                // Create CLR-Utility handle
                using (DivaUtilityCLR DivaUtility = new DivaUtilityCLR())
                {
                    SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();
                    DivaDisplayFeatureUtilityCLR objDivaDispFeatureUtil = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

                    DIVA_VERIFY_PIPE_UNDER_RUN_ARGS_CLR verify_under_run = new DIVA_VERIFY_PIPE_UNDER_RUN_ARGS_CLR();
                    objDivaDispFeatureUtil.VerifyGfxPipeUnderRun(verify_under_run);
                    result = (verify_under_run.UnderRunOnPIPE_A | verify_under_run.UnderRunOnPIPE_B | verify_under_run.UnderRunOnPIPE_C);
                }
            }
            return result;
        }

    }
}
