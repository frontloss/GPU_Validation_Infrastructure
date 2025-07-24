using System.Diagnostics;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    internal class InitCheckDriverVerify : InitEnvironment
    {
        IApplicationSettings _appSettings = null;

        public InitCheckDriverVerify(IApplicationManager argManager)
            : base(argManager)
        {
            this._appSettings = argManager.ApplicationSettings;
        }
        public override void DoWork()
        {
            if (AccessInterface.GetFeature<bool>(Features.DriverVerifier, Action.Get))
                Log.Message("Driver verifier is enabled");
            else
                AccessInterface.SetFeature<bool>(Features.DriverVerifier, Action.SetNoArgs);

            if (CommonExtensions.VerifyWDTFStatus())
            {
                Log.Verbose("Windows Driver Testing Framework (WDTF) installed on test machine");
            }
            else
            {
                Log.Verbose("Windows Driver Testing Framework (WDTF) was not installed on test machine");
            }
        }
    }
}