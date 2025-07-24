using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
using log4net;

namespace Intel.VPG.Display.FlickerTestSuite.MPO
{
    [Serializable()]
    public class Surface
    {
        private static readonly ILog logger = LogManager.GetLogger(typeof(Intel.VPG.Display.FlickerTestSuite.MPO.Surface));
        UInt64 pGmmBlock = 0;
        IntPtr pUserVirtualAddress = IntPtr.Zero;
        ulong size = 0;
        uint width;
        uint height;
        uint zorder;

        public uint Zorder
        {
            get { return zorder; }
            set { zorder = value; }
        }


        DIVA_SURFACE_MEMORY_TYPE_CLR eSurfaceMemType = DIVA_SURFACE_MEMORY_TYPE_CLR.DIVA_SURFACE_MEMORY_TILED;
        DIVA_SURFACE_MEM_OFFSET_INFO_CLR mSurfaceMemOffsetInfo = new DIVA_SURFACE_MEM_OFFSET_INFO_CLR();
        DIVA_PIXELFORMAT_CLR format = DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_R8G8B8A8;
        DIVA_SURFACE_TILEFORMAT_CLR tileFormat = DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Y;

        #region Properties

        public uint Height
        {
            get { return height; }
            set { height = value; }
        }

        public uint Width
        {
            get { return width; }
            set { width = value; }
        }


        public ulong Size
        {
            get { return size; }
            set { size = value; }
        }

        public UInt64 PGmmBlock
        {
            get { return pGmmBlock; }
            set { pGmmBlock = value; }
        }

        public IntPtr getUserVirtualAddress()
        {
            return pUserVirtualAddress;
        }


        public DIVA_PIXELFORMAT_CLR Format
        {
            get { return format; }
            set { format = value; }
        }

        public DIVA_SURFACE_TILEFORMAT_CLR TileFormat
        {
            get { return tileFormat; }
            set { tileFormat = value; }
        }

        #endregion


        public Surface()
        {
            this.width = 0;
            this.height = 0;
        }

        public Surface(uint uiWidth, uint uiHeight)
        {
            this.width = uiWidth;
            this.height = uiHeight;
        }

        public DIVA_SURFACE_MEM_OFFSET_INFO_CLR SurfaceMemOffsetInfo
        {
            get { return mSurfaceMemOffsetInfo; }
            set { mSurfaceMemOffsetInfo = value; }
        }

        public DIVA_SURFACE_MEMORY_TYPE_CLR SurfaceMemType
        {
            get { return eSurfaceMemType; }
            set { eSurfaceMemType = value; }
        }


        private void FillBuffer()
        {
            IntPtr temp_ptr = new IntPtr(pUserVirtualAddress.ToInt64());
            UInt32[] colors = { 0xffffffaa, 0xaa00ff88, 0xd3da2b2 };

            Int64 color_val = colors[(int)zorder];
            logger.InfoFormat("Zorder = {0} and color_value = {1}", zorder, color_val);
            bool planarFormat = Helper.isPlanarFormat(this.format);

            if (planarFormat == false)
            {
                for (int i = 0; i < (int)this.Size; i = i + 4)
                {
                    Marshal.WriteByte(temp_ptr, i, (byte)(color_val >> 24));
                    Marshal.WriteByte(temp_ptr, i + 1, (byte)(color_val >> 16));
                    Marshal.WriteByte(temp_ptr, i + 2, (byte)(color_val >> 8));
                    Marshal.WriteByte(temp_ptr, i + 3, (byte)color_val);
                }
            }
        }


        public void CreateResource()
        {
            try
            {
                DIVA_CREATE_RES_ARGS_CLR createRes = new DIVA_CREATE_RES_ARGS_CLR();
                createRes.Format = (DIVA_PIXELFORMAT_CLR)(this.format);
                createRes.AuxSurf = false;
                createRes.TileFormat = (DIVA_SURFACE_TILEFORMAT_CLR)this.tileFormat;
                createRes.BaseWidth = this.width;
                createRes.BaseHeight = this.height;

                using (DivaInterface diva = new DivaInterface(0, ConfigItem.EdpMonitor_ID()))
                {
                    // Create 'Generic GFX Access DIVA CLR Utility'
                    diva.CreateResourceDIVA(createRes);
                }

                this.PGmmBlock = createRes.GmmBlock;
                this.Size = createRes.SurfaceSize;
                this.pUserVirtualAddress = (IntPtr)createRes.UserVirtualAddress;
                this.FillBuffer();
                if ((this.Size) == 0)
                {
                    throw new Exception("CreateResource failed size = 0!!");
                }
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public UInt64 Get_Buffer()
        {
            return pGmmBlock;
        }


        public void FreeResource()
        {
            logger.DebugFormat("Freeing pGmmBlock {0}", this.pGmmBlock);

            try
            {
                using (DivaInterface diva = new DivaInterface(0, ConfigItem.EdpMonitor_ID()))
                {
                    diva.FreeResourceDIVA(this.pGmmBlock);
                }

                this.pGmmBlock = 0;
                this.pUserVirtualAddress = IntPtr.Zero;
            }
            catch (Exception ex)
            {
                logger.ErrorFormat("Freeing pGmmBlock {0}", this.pGmmBlock);
                logger.Error(ex.StackTrace);
                throw new Exception("FreeResource failed!!");
            }
        }
    }
}
