using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class InitDisableLAN : InitEnvironment
    {
        IApplicationSettings _appSettings = null;
        private TestBase _context = null;
        public InitDisableLAN(IApplicationManager argManager)
            : base(argManager)
        {
            this._appSettings = argManager.ApplicationSettings;
        }
        public override void DoWork()
        {
            _context = _context.Load(base.Manager.ParamInfo[ArgumentType.TestName] as string);
            if (_context == null)
                return;
            if (_context.HasAttribute(TestType.ConnectedStandby))
            {
                NetParam netParam;
                netParam = new NetParam();
                netParam.adapter = Adapter.LAN;
                netParam.netWorkState = NetworkState.Disable;
                Log.Message("Disabling LAN connection..");
                NetworkExtensions.SetNetworkConnection(netParam);
            }
        }
    }
}
