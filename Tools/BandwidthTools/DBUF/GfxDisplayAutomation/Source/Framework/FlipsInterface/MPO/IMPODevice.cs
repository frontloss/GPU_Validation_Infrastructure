using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.FlickerTestSuite.MPO
{
    public interface IMPODevice
    {
        void Init();
        bool CheckMPO(List<MPOPlane> planes);
        bool Blend(List<MPOPlane> planes, DIVA_SETVIDPNSRCADDR_FLAGS_CLR Flag);
        void DeInit();
        uint ReadRegister(uint offset);
    }
}
