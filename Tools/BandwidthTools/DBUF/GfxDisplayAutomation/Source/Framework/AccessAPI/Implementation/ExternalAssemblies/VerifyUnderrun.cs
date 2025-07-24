using Microsoft.Win32.SafeHandles;
using System;
using System.Text;

namespace Intel.VPG.Display.Automation
{
    public class VerifyUnderrun : FunctionalBase, ISetMethod, IGetMethod
    {
        /* 
         * If Diva Driver is installed and useDivaFramework is true we are enabling underrun return status is true.
         * else we are not enabling underrun and return status is false
         */
        public bool SetMethod(object argMessage)
        {
            bool configureType = (bool)argMessage;
            if (base.AppManager.ApplicationSettings.UseDivaFramework &&
                base.MachineInfo.Driver.Name.ToLower().Contains("intel") &&
                base.MachineInfo.Driver.Status.ToLower().Contains("running"))
            {
                DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility;

                //#### Not verifying DIVA Driver status since InitVerifyDivaStatus already verified. #####
                //Create Diva Util object to call exposed functionalify present in DIVA Util.
                DivaDisplayFeatureUtility = GetDivaDisplayFeatureUtility();
                DIVA_PIPE_UNDER_RUN_ARGS_CLR DivaPipeUnderrun = new DIVA_PIPE_UNDER_RUN_ARGS_CLR();

                DivaPipeUnderrun.Enable = configureType; // variable used for enable or disable under run.
                DivaPipeUnderrun.UnderRunEventType = DIVA_UNDER_RUN_EVENTS_CLR.DIVA_UNDERRUN_ALL_PIPE_CLR; //enable under run for all pipe.
                DivaDisplayFeatureUtility.ConfigureGfxPipeUnderRun(DivaPipeUnderrun);

                if (!TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.Underrun))
                    TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.Underrun, null);

                return true;
            }
            return false;
        }

        public object GetMethod(object argMessage)
        {
            if (base.AppManager.ApplicationSettings.UseDivaFramework &&
                base.MachineInfo.Driver.Name.ToLower().Contains("intel") &&
                base.MachineInfo.Driver.Status.ToLower().Contains("running"))
            {
                DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility;
                //#### Not verifying DIVA Driver status since InitVerifyDivaStatus already verified. #####

                //#### Create Diva Util object to call exposed functionalify present in DIVA Util. ####
                DivaDisplayFeatureUtility = GetDivaDisplayFeatureUtility();

                //#### DIVA_VERIFY_PIPE_UNDER_RUN_ARGS_CLR is a reference type so driver will update ########
                //#### underrun information on perticular fields                                     ########
                DIVA_VERIFY_PIPE_UNDER_RUN_ARGS_CLR verifyUnderrun = new DIVA_VERIFY_PIPE_UNDER_RUN_ARGS_CLR();
                DivaDisplayFeatureUtility.VerifyGfxPipeUnderRun(verifyUnderrun);
                StringBuilder sb = new StringBuilder();

                if (verifyUnderrun.UnderRunOnPIPE_A)
                    sb.Append("PIPE A ");
                if (verifyUnderrun.UnderRunOnPIPE_B)
                    sb.Append("PIPE B ").Append(Environment.NewLine);
                if (verifyUnderrun.UnderRunOnPIPE_C)
                    sb.Append("PIPE C ").Append(Environment.NewLine);
                if (verifyUnderrun.UnderRunOnPIPE_A == false &&
                    verifyUnderrun.UnderRunOnPIPE_B == false &&
                    verifyUnderrun.UnderRunOnPIPE_C == false)
                {
                    Log.Verbose("Could not find any UnderRun on PIPE-A, PIPE-B and PIPE-C");
                    return false;
                }
                else
                {
                    Log.Fail("Observed Underrun on {0}", sb.ToString());
                    return true;
                }
            }
            return false;
        }

        private DivaDisplayFeatureUtilityCLR GetDivaDisplayFeatureUtility()
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();
            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            return DivaDisplayFeatureUtility;
        }
    }
}
