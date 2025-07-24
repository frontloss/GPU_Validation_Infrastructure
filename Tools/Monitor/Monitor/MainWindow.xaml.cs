using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Timers;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Runtime.InteropServices;
using static Monitor.WriteBack;

namespace Monitor
{
    public class WriteBack
    {

        [StructLayout(LayoutKind.Sequential, Pack = 8)]
        public struct WB_CAPS
        {
            public int IsSupported;
            public int IsEnabled;
            public int HResolution;
            public int VResolution;
            public int PixelFormat;
        };
        [DllImport("DrvInterface.dll", CharSet = CharSet.Unicode)]
        public static extern void QueryWbStatus(ref WB_CAPS caps );
        [StructLayout(LayoutKind.Sequential, Pack = 8)]

        public struct WB_CAPTURE
        {
            public int WdSource;
            public int HResolution;
            public int VResolution;
            public int PixelFormat;
            public long BufferSize;
            public IntPtr pBuffer;
        }
        [DllImport("DrvInterface.dll", CharSet = CharSet.Unicode)]
        public static extern void CaptureFrame(ref WB_CAPTURE Capture, IntPtr pBuffer);
    }
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        
        public MainWindow()
        {
            InitializeComponent();
            RefreshTimer = new Timer(300);
            RefreshTimer.Elapsed += OnTimedEvent;
            RefreshTimer.AutoReset = true;
        }

        Timer RefreshTimer;
        
        // Byte[] FrameBuffer = new byte[720*480*4];
        static WriteableBitmap writeableBitmap;
        static Window w;
        static Image FrameBuffer;
        // The DrawPixel method updates the WriteableBitmap by using
        // unsafe code to write a pixel into the back buffer.
        static void DrawPixel(MouseEventArgs e)
        {
            int column = (int)e.GetPosition(FrameBuffer).X;
            int row = (int)e.GetPosition(FrameBuffer).Y;

            // Reserve the back buffer for updates.
            writeableBitmap.Lock();

            unsafe
            {
                // Get a pointer to the back buffer.
                int pBackBuffer = (int)writeableBitmap.BackBuffer;

                // Find the address of the pixel to draw.
                pBackBuffer += row * writeableBitmap.BackBufferStride;
                pBackBuffer += column * 4;

                // Compute the pixel's color.
                int color_data = 255 << 16; // R
                color_data |= 128 << 8;   // G
                color_data |= 255 << 0;   // B

                // Assign the color data to the pixel.
                *((int*)pBackBuffer) = color_data;
            }

            // Specify the area of the bitmap that changed.
            writeableBitmap.AddDirtyRect(new Int32Rect(column, row, 1, 1));

            // Release the back buffer and make it available for display.
            writeableBitmap.Unlock();
        }

        static void DrawFrame()
        {
            int column;
            int row;
            Random rnd = new Random();
            IntPtr pFbBuff;
            WB_CAPTURE Capture = new WB_CAPTURE();
            // Reserve the back buffer for updates.
            writeableBitmap.Lock();

            unsafe
            {


                int BuffSize = 3840 * 2160 * 4;
                pFbBuff = Marshal.AllocHGlobal(BuffSize);
                Capture.pBuffer = pFbBuff;
                Capture.BufferSize = BuffSize;
                WriteBack.CaptureFrame(ref Capture, pFbBuff);

                // Get a pointer to the back buffer.
                Int64 pBackBuffer = (Int64)writeableBitmap.BackBuffer;
                Int64 pFbWalker = (Int64)pFbBuff;
                int color_Opaque_mask =  0xFF << 28;// rnd.Next();
                int Pixel;
                //pFbWalker = pFbBuff;

                for (row = 0; row < Capture.VResolution; row++)
                {
                    pBackBuffer = (Int64)writeableBitmap.BackBuffer + row * writeableBitmap.BackBufferStride;
                    pFbWalker = (Int64)pFbBuff + row * Capture.HResolution *  4;
                    for (column = 0; column < Capture.HResolution; column++)
                    {
                        // Find the address of the pixel to draw.

                        // Assign the color data to the pixel.

                        Pixel = *((int*)pFbWalker) | color_Opaque_mask;
                        *((int*)pBackBuffer) = (int)(Pixel & 0xFF00FF00);
                        *((int*)pBackBuffer) |= (int)(Pixel & 0xFF) << 16;
                        *((int*)pBackBuffer) |= (int)((Pixel >> 16) & 0xFF);
                        pBackBuffer += 4;
                        pFbWalker += 4;
                    }
                }
                Marshal.FreeHGlobal(pFbBuff);
            }


            // Specify the area of the bitmap that changed.
            writeableBitmap.AddDirtyRect(new Int32Rect(0, 0, Capture.HResolution, Capture.VResolution));

            // Release the back buffer and make it available for display.
            writeableBitmap.Unlock();
        }

        static void ErasePixel(MouseEventArgs e)
        {
            byte[] ColorData = { 0, 0, 0, 0 }; // B G R

            Int32Rect rect = new Int32Rect(
                    (int)(e.GetPosition(FrameBuffer).X),
                    (int)(e.GetPosition(FrameBuffer).Y),
                    1,
                    1);

            writeableBitmap.WritePixels(rect, ColorData, 4, 0);
        }

        static void i_MouseRightButtonDown(object sender, MouseButtonEventArgs e)
        {
            ErasePixel(e);
        }

        static void i_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            // DrawPixel(e);
        }

        static void i_MouseMove(object sender, MouseEventArgs e)
        {
            /*
             * if (e.LeftButton == MouseButtonState.Pressed)
            {
                DrawPixel(e);
            }
            else if (e.RightButton == MouseButtonState.Pressed)
            {
                ErasePixel(e);
            }
            */
        }

        static void w_MouseWheel(object sender, MouseWheelEventArgs e)
        {
            System.Windows.Media.Matrix m = FrameBuffer.RenderTransform.Value;

            if (e.Delta > 0)
            {
                m.ScaleAt(
                    1.5,
                    1.5,
                    e.GetPosition(w).X,
                    e.GetPosition(w).Y);
            }
            else
            {
                m.ScaleAt(
                    1.0 / 1.5,
                    1.0 / 1.5,
                    e.GetPosition(w).X,
                    e.GetPosition(w).Y);
            }

            FrameBuffer.RenderTransform = new MatrixTransform(m);
        }
        private void OnTimedEvent(Object source, ElapsedEventArgs e)
        {
            Dispatcher.Invoke((Action)delegate ()
            {
                try
                {
                    DrawFrame();
                    // DoD.Foreground = new System.Windows.Media.SolidColorBrush((Color)ColorConverter.ConvertFromString("#" + (Rnd.Next() | 0xFF000000).ToString("X")));
                }
                catch (Exception Ex)
                {
                    MessageBox.Show(Ex.Message);
                }
            });
        }
        private void LiveView_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                FrameBuffer = new Image();
                RenderOptions.SetBitmapScalingMode(FrameBuffer, BitmapScalingMode.NearestNeighbor);
                RenderOptions.SetEdgeMode(FrameBuffer, EdgeMode.Aliased);

                w = new Window();
                w.Content = FrameBuffer;


                WB_CAPS WbCaps = new WB_CAPS();
                WriteBack.QueryWbStatus(ref WbCaps);
                w.Width = WbCaps.HResolution;
                w.Height = WbCaps.VResolution;
                writeableBitmap = new WriteableBitmap(
                    WbCaps.HResolution,
                    WbCaps.VResolution,
                    96,
                    96,
                    PixelFormats.Bgr32,
                    null);

                FrameBuffer.Source = writeableBitmap;

                FrameBuffer.Stretch = Stretch.None;
                FrameBuffer.HorizontalAlignment = HorizontalAlignment.Left;
                FrameBuffer.VerticalAlignment = VerticalAlignment.Top;

                FrameBuffer.MouseMove += new MouseEventHandler(i_MouseMove);
                FrameBuffer.MouseLeftButtonDown +=
                    new MouseButtonEventHandler(i_MouseLeftButtonDown);
                FrameBuffer.MouseRightButtonDown +=
                    new MouseButtonEventHandler(i_MouseRightButtonDown);

                FrameBuffer.MouseWheel += new MouseWheelEventHandler(w_MouseWheel);
                RefreshTimer.Start();
                w.Show();
            }
            catch(Exception Ex)
            {
                MessageBox.Show(Ex.Message);
            }
        }
    }

}
