using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net;


namespace Intel.VPG.Display.FlickerTestSuite.MPO
{
    public static class MemoryPool
    {
        private static readonly ILog logger = LogManager.GetLogger(typeof(MemoryPool));
        private static List<Surface> _available = new List<Surface>();
        private static List<Surface> _inUse = new List<Surface>();

        private static bool AllocateBuffer(ref  MPOPlane plane)
        {
            Surface surf = new Surface(ConfigItem.CurrentMode.Width, ConfigItem.CurrentMode.Height);
            surf.Format = plane.PixelFormat;
            surf.TileFormat = plane.Tile_format;
            surf.Zorder = plane.Zorder;
            try
            {
                surf.CreateResource();
                _available.Add(surf);
                plane.SetBuffer(surf.PGmmBlock, surf.getUserVirtualAddress());
            }
            catch (Exception ex)
            {
                logger.Error(ex.Message);
                logger.Error(ex.StackTrace);
                return false;
            }

            return true;
        }

        public static bool AcquireBuffer(ref MPOPlane plane)
        {
            bool found = false;
            Surface allocatedObject = null;

            lock (_available)
            {
                foreach (Surface surf in _available)
                {
                    if (surf.Format == plane.PixelFormat && surf.TileFormat == plane.Tile_format && surf.Zorder == plane.Zorder)
                    {
                        plane.SetBuffer(surf.PGmmBlock, surf.getUserVirtualAddress());
                        found = true;
                        allocatedObject = surf;
                        logger.DebugFormat("Resource found in pool : {0}", allocatedObject.PGmmBlock);
                        break;
                    }
                }

                if (found == false)
                {
                    logger.Debug("Resource not found in pool, allocate");
                    return AllocateBuffer(ref plane);
                }
                else
                {
                    _available.Remove(allocatedObject);
                    _inUse.Add(allocatedObject);
                }
            }
            return found;
        }

        public static bool ReleaseBuffer(ref MPOPlane plane)
        {
            bool found = false;
            Surface freedObject = null;

            lock (_inUse)
            {
                foreach (Surface surf in _inUse)
                {
                    if (surf.PGmmBlock == plane.Get_Buffer())
                    {
                        found = true;
                        freedObject = surf;
                        break;
                    }
                }

                if (found == false)
                {
                    logger.Debug("Hmm, something fishy not reference to allocated surface!!");
                }
                else
                {
                    logger.DebugFormat("Resource released to pool : {0}", freedObject.PGmmBlock);
                    _inUse.Remove(freedObject);
                    _available.Add(freedObject);
                }
            }
            return found;
        }

        public static void Free()
        {
            lock (_available)
            {
                foreach (Surface surf in _available)
                {
                    surf.FreeResource();
                }
            }

            _available.Clear();

            lock (_inUse)
            {
                foreach (Surface surf in _inUse)
                {
                    surf.FreeResource();
                }
            }
            _inUse.Clear();
        }
    }
}
