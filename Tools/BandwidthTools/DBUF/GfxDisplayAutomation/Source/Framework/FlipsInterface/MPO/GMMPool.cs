using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Intel.VPG.Display.FlipsInterface.MPO
{
    public static class GMMPool
    {
        //private static readonly ILog logger = LogManager.GetLogger(typeof(GMMPool));
        private static List<GmmObject> _available = new List<GmmObject>();
        private static List<GmmObject> _inUse = new List<GmmObject>();


        public static GmmObject AcquireBuffer(MPOPlane plane)
        {
            bool acquired = false;
            GmmObject allocatedObject = null;

            try
            {
                lock (_available)
                {
                    foreach (GmmObject surf in _available)
                    {
                        if (surf.MatchCriterion(plane))
                        {
                            acquired = true;
                            allocatedObject = surf;
                            //logger.DebugFormat("Resource found in pool : {0}", allocatedObject.GmmBlock);
                            break;
                        }
                    }

                    if (acquired == false)
                    {
                        //logger.Debug("Resource not found in pool, allocate");
                        allocatedObject = new GmmObject(ConfigItem.CurrentMode.Width, ConfigItem.CurrentMode.Height,
                                       plane.Zorder, plane.PixelFormat, plane.Tile_format);

                        allocatedObject.CreateResource();
                    }
                    else
                    {
                        _available.Remove(allocatedObject);
                    }
                    _inUse.Add(allocatedObject);
                }
            }
            catch (Exception ex)
            {
                //logger.Error(ex.Message);
                //logger.Error(ex.StackTrace);
            }
            return allocatedObject;
        }

        public static bool ReleaseBuffer(UInt64 pGmmBlock)
        {
            bool found = false;
            GmmObject freedObject = null;

            lock (_inUse)
            {
                foreach (GmmObject surf in _inUse)
                {
                    if (surf.GmmBlock == pGmmBlock)
                    {
                        found = true;
                        freedObject = surf;
                        break;
                    }
                }

                if (found == false)
                {
                    //logger.Debug("Hmm, something fishy not reference to allocated surface!!");
                }
                else
                {
                    //logger.DebugFormat("Resource released to pool : {0}", freedObject.GmmBlock);

                    _inUse.Remove(freedObject);
                    _available.Add(freedObject);
                }
            }
            return found;
        }

        public static void FreePool()
        {
            lock (_available)
            {
                foreach (GmmObject surf in _available)
                {
                    surf.FreeResource();
                }
            }

            _available.Clear();

            lock (_inUse)
            {
                foreach (GmmObject surf in _inUse)
                {
                    surf.FreeResource();
                }
            }
            _inUse.Clear();
        }
    }
}
