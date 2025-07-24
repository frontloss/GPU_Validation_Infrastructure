using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.IO;


namespace Intel.VPG.Display.FlipsInterface.MPO
{
    [Serializable()]
    public class MPOPlane : DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR, IDisposable
    {
        //private static readonly ILog logger = LogManager.GetLogger(typeof(Intel.VPG.Display.FlickerTestSuite.MPO.MPOPlane));
        private GmmObject frontBuffer = null;
        DIVA_SURFACE_TILEFORMAT_CLR tile_format;
        private bool affected = true;

        public bool Affected
        {
            get { return affected; }
            set { affected = value; }
        }

        public DIVA_SURFACE_TILEFORMAT_CLR Tile_format
        {
            get { return tile_format; }
            set { tile_format = value; }
        }

        public DIVA_MPO_PLANE_ATTRIBUTES_CLR Attributes
        {
            get { return this.pPlaneAttributes; }
            set { this.pPlaneAttributes = value; }
        }

        public uint Zorder
        {
            get { return this.LayerIndex; }
            set { this.LayerIndex = value; }

        }

        private void Init()
        {
            this.Enabled = true;
            this.IsAsyncMMIOFlip = false;
            this.Affected = true;

            this.PixelFormat = DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_B8G8R8A8;
            this.tile_format = DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Y;
            this.Attributes = new DIVA_MPO_PLANE_ATTRIBUTES_CLR();
            this.Attributes.MPOBlend = 0;
            this.Attributes.DIRTYRECTS = new DIVA_M_RECT_CLR[8];
            this.Attributes.MPOStereoFlipMode = DIVA_MPO_STEREO_FLIP_MODE_CLR.DIVA_MPO_FLIP_NONE;
            this.Attributes.MPOVideoFormat = DIVA_MPO_VIDEO_FRAME_FORMAT_CLR.DIVA_MPO_VIDEO_FRAME_FORMAT_PROGRESSIVE;
            this.Attributes.MPOStereoFormat = DIVA_MPO_STEREO_FORMAT_CLR.DIVA_MPO_FORMAT_MONO;
            this.Attributes.StretchQuality = DIVA_MPO_STRETCH_QUALITY_CLR.DIVA_MPO_STRETCH_QUALITY_BILINEAR;
            this.Attributes.MPORotation = DIVA_MPO_ROTATION_CLR.DIVA_MPO_ROTATION_IDENTITY;
            this.Attributes.MPOYCbCrFlags = 0;
        }

        public MPOPlane()
        {
            Init();
        }


        public MPOPlane(uint width, uint height, DIVA_PIXELFORMAT_CLR format, DIVA_SURFACE_TILEFORMAT_CLR tile_format, uint zorder)
        {
            Init();

            this.LayerIndex = zorder;
            this.PixelFormat = format;
            this.tile_format = tile_format;

            this.Attributes.MPOSrcRect.Right = width;
            this.Attributes.MPOSrcRect.Bottom = height;
            this.Attributes.MPODstRect = this.Attributes.MPOSrcRect;
            this.Attributes.MPOClipRect = this.Attributes.MPODstRect;
        }

        public Dim SourceRect
        {
            get
            {
                Dim tmp = new Dim();
                tmp.Width = (this.Attributes.MPOSrcRect.Right - this.Attributes.MPOSrcRect.Left);
                tmp.Height = (this.Attributes.MPOSrcRect.Bottom - this.Attributes.MPOSrcRect.Top);
                return tmp;
            }
        }

        public uint GetSourceWidth()
        {
            return this.Attributes.MPOSrcRect.Right - this.Attributes.MPOSrcRect.Left;
        }
        public uint GetDestinationWidth()
        {
            return this.Attributes.MPODstRect.Right - this.Attributes.MPODstRect.Left;
        }
        public uint GetSourceHeight()
        {
            return this.Attributes.MPOSrcRect.Bottom - this.Attributes.MPOSrcRect.Top;
        }
        public uint GetDestinationHeight()
        {
            return this.Attributes.MPODstRect.Bottom - this.Attributes.MPODstRect.Top;
        }

        private string GetString(DIVA_M_RECT_CLR val)
        {
            return string.Format("{0},{1},{2},{3}", val.Left, val.Top, val.Right, val.Bottom);
        }

        public override string ToString()
        {
            StringBuilder sb = new StringBuilder();
            String layer_info = String.Empty;
            layer_info = String.Format("DIM({0}x{1}x{2}x{3})", this.SourceRect.Width, this.SourceRect.Height,
                                this.PixelFormat, this.tile_format);
            sb.Append(layer_info);

            layer_info = String.Format("+FLIP({0})+ORT({1})", this.Attributes.MPOStereoFlipMode,
                                        this.Attributes.HWOrientation);
            sb.Append(layer_info);

            layer_info = String.Format("+RECT(SRC({0})+DST({1})+CLIP({2}))", GetString(this.Attributes.MPOSrcRect),
                                    GetString(this.Attributes.MPODstRect),
                                    GetString(this.Attributes.MPOClipRect));

            sb.Append(layer_info);

            layer_info = String.Format("+BLEND({0})+ZORDER({1})", this.Attributes.MPOBlend, this.Zorder);
            sb.Append(layer_info);
            return sb.ToString();
        }

        //public void ToXML(ref XmlWriter output)
        //{
        //    System.Xml.Serialization.XmlSerializer writer = new System.Xml.Serialization.XmlSerializer(this.GetType());

        //    StringBuilder sb = new StringBuilder();
        //    System.Xml.XmlWriter xmlWriter = System.Xml.XmlWriter.Create(sb);

        //    writer.Serialize(xmlWriter, this);
        //    xmlWriter.Flush();
        //    xmlWriter.Close();

        //    TextReader textReader = new StringReader(sb.ToString());
        //    XDocument xmlDocument = XDocument.Load(textReader);
        //    XElement plane_info = (from xml2 in xmlDocument.Descendants("MPOPlane")
        //                           select xml2).FirstOrDefault();

        //    plane_info.WriteTo(output);
        //}


        #region Memory Management

        public UInt64 Get_Buffer()
        {
            return frontBuffer.GmmBlock;
        }



        public bool Allocate()
        {
            if (frontBuffer == null 
                            || frontBuffer.GmmBlock == 0 
                            || frontBuffer.MatchCriterion(this) == false)
            {
                this.Free();
                frontBuffer = GMMPool.AcquireBuffer(this);

                if (frontBuffer == null || frontBuffer.GmmBlock == 0)
                {
                    return false;
                }
            }

            return true;
        }

        public void Free()
        {
            if (frontBuffer != null)
            {
                GMMPool.ReleaseBuffer(frontBuffer.GmmBlock);
                frontBuffer = null;
            }
        }

        #endregion


        void IDisposable.Dispose()
        {
            this.Free();
        }
    }
}
