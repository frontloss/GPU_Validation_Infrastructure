using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using log4net;

namespace Intel.VPG.Display.FlickerTestSuite.MPO
{
    public class MPODevice
    {
        private static readonly ILog logger = LogManager.GetLogger(typeof(MPODevice));
        IMPODevice mpoDevice = null;

        public MPODevice(uint source_id, uint monitorId)
        {

            logger.Info("Creating DIVA interface");
            mpoDevice = new DivaInterface(source_id, monitorId);

            if (ConfigItem.UnderRunCheck())
            {
                DivaInterface.ConfigureUnderRun(true);
            }
        }

        public void Init()
        {
            mpoDevice.Init();
        }

        public bool CheckMPO(List<MPOPlane> planes)
        {
            return mpoDevice.CheckMPO(planes);
        }

        public bool Blend(List<MPOPlane> planes, DIVA_SETVIDPNSRCADDR_FLAGS_CLR Flag)
        {
            return mpoDevice.Blend(planes, Flag);
        }

        public void DeInit()
        {
            mpoDevice.DeInit();
            if (ConfigItem.UnderRunCheck() == true)
            {
                DivaInterface.ConfigureUnderRun(false);
            }
        }

        public uint ReadRegister(uint offset)
        {
            return mpoDevice.ReadRegister(offset);
        }
    }
}
