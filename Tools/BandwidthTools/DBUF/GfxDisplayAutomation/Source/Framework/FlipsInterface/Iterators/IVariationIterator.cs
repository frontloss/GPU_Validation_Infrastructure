using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Intel.VPG.Display.FlipsInterface.MPO;

namespace Intel.VPG.Display.FlipsInterface
{
    public abstract class MPOObject {
    }

    public interface IPlaneVariationIterator
    {
        MPOPlane NextVariationPlane();        
        bool NextVariationPlane(ref MPOPlane plane);
    }


    public interface IVariationIterator
    {
        List<MPOPlane> NextVariation();
    }
}
