using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using Intel.VPG.Display.FlipsInterface.MPO;

namespace Intel.VPG.Display.FlipsInterface
{

    [Serializable]
    public class Dim
    {
        uint m_width;

        public uint Width
        {
            get { return m_width; }
            set { m_width = value; }
        }
        uint m_height;

        public uint Height
        {
            get { return m_height; }
            set { m_height = value; }
        }

        public Dim()
        {

        }
        public Dim(uint width, uint height)
        {
            this.m_width = width;
            this.m_height = height;
        }
    }


    [Serializable()]
    public struct SurfaceDim
    {
        public List<Dim> rects;
        public uint increment_val;
        public uint iteration_limit;
    }


    public class SurfacePoint
    {
        uint x;

        public uint X
        {
            get { return x; }
            set { x = value; }
        }
        uint y;

        public uint Y
        {
            get { return y; }
            set { y = value; }
        }
    }

    public class SurfaceFormat
    {
        DIVA_PIXELFORMAT_CLR m_Format;
        List<DIVA_SURFACE_TILEFORMAT_CLR> m_tileFormats = new List<DIVA_SURFACE_TILEFORMAT_CLR>();

        public List<DIVA_SURFACE_TILEFORMAT_CLR> TileFormats
        {
            get { return m_tileFormats; }
            set { m_tileFormats = value; }
        }

        public DIVA_PIXELFORMAT_CLR Format
        {
            get { return m_Format; }
            set { m_Format = value; }
        }
    }


    public class Helper
    {
        public static T Clone<T>(T source)
        {
            if (!typeof(T).IsSerializable)
            {
                throw new ArgumentException("The type must be serializable.", "source");
            }

            // Don't serialize a null object, simply return the default for that object
            if (Object.ReferenceEquals(source, null))
            {
                return default(T);
            }

            IFormatter formatter = new BinaryFormatter();
            Stream stream = new MemoryStream();
            using (stream)
            {
                formatter.Serialize(stream, source);
                stream.Seek(0, SeekOrigin.Begin);
                return (T)formatter.Deserialize(stream);
            }
        }

        public static string ToString(DIVA_M_RECT_CLR rect)
        {
            string retValue = "0,0,0,0";

            retValue = string.Format("{0},{1},{2},{3}", rect.Left, rect.Top, rect.Right, rect.Bottom);
            return retValue;
        }


        public static List<Dim> MediaRectangles()
        {
            List<Dim> retValues = new List<Dim>();
            retValues.Add(new Dim(720, 480));
            retValues.Add(new Dim(720, 576));
            retValues.Add(new Dim(1280, 720));
            retValues.Add(new Dim(3840, 2160));
            return retValues;
        }

        public static bool isPlanarFormat(DIVA_PIXELFORMAT_CLR format)
        {
            if (format == DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_NV12YUV420 ||
            format == DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_YUV422)
            {
                return true;
            }

            return false;
        }

        public static DIVA_M_RECT_CLR Parse_Rectangles(string dim)
        {

            DIVA_M_RECT_CLR temp = new DIVA_M_RECT_CLR();
            temp.Left = 0;
            temp.Right = 0;
            temp.Top = 0;
            temp.Bottom = 0;

            if (string.IsNullOrEmpty(dim) == false)
            {
                string[] rect = dim.Split(',');
                temp.Left = Convert.ToUInt32(rect[0]);
                temp.Top = Convert.ToUInt32(rect[1]);
                temp.Right = Convert.ToUInt32(rect[2]);
                temp.Bottom = Convert.ToUInt32(rect[3]);
            }

            return temp;
        }

        public static List<DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR> MarshalPlaneData(ref List<MPOPlane> planes)
        {
            List<DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR> testPlanes = new List<DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR>();

            foreach (MPOPlane mpoPlane in planes)
            {
                DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR plane = new DIVA_MPO_CHECKMPOSUPPORT_PLANE_INFO_CLR();

                plane.LayerIndex = mpoPlane.Zorder;
                plane.Enabled = mpoPlane.Enabled;
                plane.IsAsyncMMIOFlip = mpoPlane.IsAsyncMMIOFlip;
                plane.PixelFormat = mpoPlane.PixelFormat;

                switch (mpoPlane.Tile_format)
                {
                    case DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_X:
                        plane.SurfaceMemInfo.SurfaceMemType = DIVA_SURFACE_MEMORY_TYPE_CLR.DIVA_SURFACE_MEMORY_X_TILED;
                        break;
                    case DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_L:
                        plane.SurfaceMemInfo.SurfaceMemType = DIVA_SURFACE_MEMORY_TYPE_CLR.DIVA_SURFACE_MEMORY_LINEAR;
                        break;
                    case DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_W:
                        plane.SurfaceMemInfo.SurfaceMemType = DIVA_SURFACE_MEMORY_TYPE_CLR.DIVA_SURFACE_MEMORY_TILED;
                        break;
                    case DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Yf:
                        plane.SurfaceMemInfo.SurfaceMemType = DIVA_SURFACE_MEMORY_TYPE_CLR.DIVA_SURFACE_MEMORY_Y_F_TILED;
                        break;
                    default:
                        plane.SurfaceMemInfo.SurfaceMemType = DIVA_SURFACE_MEMORY_TYPE_CLR.DIVA_SURFACE_MEMORY_Y_LEGACY_TILED;
                        break;
                }
                plane.pPlaneAttributes = mpoPlane.Attributes;
                testPlanes.Add(plane);
            }

            return testPlanes;
        }
    }
}
