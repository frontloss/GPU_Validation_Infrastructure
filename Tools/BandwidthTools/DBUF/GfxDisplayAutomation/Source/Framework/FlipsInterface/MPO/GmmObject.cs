using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;

namespace Intel.VPG.Display.FlipsInterface.MPO
{
    [Serializable()]
    public class GmmObject
    {
        //private static readonly ILog logger = LogManager.GetLogger(typeof(GmmObject));
        UInt64 pGmmBlock = 0;
        IntPtr pUserVirtualAddress = IntPtr.Zero;
        ulong size = 0;
        uint width;
        uint height;
        uint zorder;
        DIVA_PIXELFORMAT_CLR format = DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_R8G8B8A8;
        DIVA_SURFACE_TILEFORMAT_CLR tileFormat = DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Y;

        #region Properties

        public uint Height
        {
            get { return height; }
        }

        public uint Width
        {
            get { return width; }
        }


        public ulong Size
        {
            get { return size; }
        }

        public UInt64 GmmBlock
        {
            get { return pGmmBlock; }

        }

        public IntPtr UserVirtualAddress
        {
            get { return pUserVirtualAddress; }
        }


        public DIVA_PIXELFORMAT_CLR Format
        {
            get { return format; }
        }

        public DIVA_SURFACE_TILEFORMAT_CLR TileFormat
        {
            get { return tileFormat; }
        }

        public uint Zorder
        {
            get { return zorder; }
        }

        #endregion

        public GmmObject(uint uiWidth, uint uiHeight, uint uiZorder, DIVA_PIXELFORMAT_CLR format, DIVA_SURFACE_TILEFORMAT_CLR tileFormat)
        {
            this.width = uiWidth;
            this.height = uiHeight;
            this.zorder = uiZorder;
            this.format = format;
            this.tileFormat = tileFormat;
        }



        private void FillBuffer()
        {
            IntPtr temp_ptr = new IntPtr(pUserVirtualAddress.ToInt64());
            UInt32[] colors = { 0xffffffaa, 0xaa00ff88, 0xd3da2b2 };

            Int64 color_val = colors[(int)zorder];
            //logger.InfoFormat("Zorder = {0} and color_value = {1}", zorder, color_val);
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
                createRes.Format = (this.format);
                createRes.AuxSurf = false;
                createRes.TileFormat = this.tileFormat;
                createRes.BaseWidth = this.width;
                createRes.BaseHeight = this.height;

                using (DivaInterface diva = new DivaInterface(0, ConfigItem.EdpMonitor_ID()))
                {
                    // Create 'Generic GFX Access DIVA CLR Utility'
                    diva.CreateResourceDIVA(createRes);
                }

                this.pGmmBlock = createRes.GmmBlock;
                this.size = createRes.SurfaceSize;
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


        public void FreeResource()
        {
            //logger.DebugFormat("Freeing pGmmBlock {0}", this.pGmmBlock);

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
                //logger.ErrorFormat("Freeing pGmmBlock {0}", this.pGmmBlock);
                //logger.Error(ex.StackTrace);
                throw new Exception("FreeResource failed!!");
            }
        }

        public bool MatchCriterion(MPOPlane plane)
        {
            if (this.Format == plane.PixelFormat
                                    && this.TileFormat == plane.Tile_format
                                    && this.Zorder == plane.Zorder)
            {
                return true;
            }
            return false;
        }
    }
}

