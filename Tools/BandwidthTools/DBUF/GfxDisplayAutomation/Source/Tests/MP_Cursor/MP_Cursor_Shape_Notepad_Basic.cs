namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Drawing;
    using System.Windows.Forms;
    using System.Collections.Generic;

    class MP_Cursor_Shape_Notepad_Basic : TestBase
    {
        private string _processName = "notepad";
        protected Dictionary<Point, Cursor> _myDictionary = null;
        AppHandle classHandle = new AppHandle();
        AppHandle appHandle = new AppHandle();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Check if mouse is connected");
            cursorInfo cursorInfo = AccessInterface.GetFeature<cursorInfo>(Features.CursorEvent, Action.GetMethod, Source.AccessAPI);
            if (cursorInfo.hCursor == (IntPtr)0)
                Log.Abort("Mouse is not connected");
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Connect all the displays planned in the grid.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Launch the Application");
            if (AccessInterface.SetFeature<bool, string>(Features.LaunchApp, Action.SetMethod, _processName))
                Log.Success("Application launched successfully");
            else
                Log.Fail("Error in launching the application");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Get coordinates of Application and corresponding class within App");
            AppDetail appDetail = new AppDetail();
            AppDetail classDetail = new AppDetail();
            appDetail.className = null;
            appDetail.handle = (IntPtr)null;
            appDetail.processName = _processName;
            appDetail.displayConfig = base.CurrentConfig;
            appDetail.displayHierarchy = DisplayHierarchy.Display_2;
            Log.Message("Get the Handle and Rect coordinates of the App");
            appHandle = AccessInterface.GetFeature<AppHandle, AppDetail>(Features.LaunchApp, Action.GetMethod, Source.AccessUI, appDetail);

            classDetail.className = "edit";
            classDetail.handle = appHandle.handle;
            Log.Message("Get the Handle and Rect coordinates of the Class");
            classHandle = AccessInterface.GetFeature<AppHandle, AppDetail>(Features.LaunchApp, Action.GetMethod, Source.AccessUI, classDetail);
            if (checkClassWithinApp(appHandle.rectCoordinate, classHandle.rectCoordinate))
                Log.Success("Coordinates of the class are within the coordinates of Application");
            else
                Log.Fail("Coordinates of the class are out of bounds with the coordinates of Application");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            _myDictionary = new Dictionary<Point, Cursor>();
            Log.Message(true, "Create a distionary of the cursor positions");
            Log.Message("Get 15 random coordinates in text area where cursor type is IBEAM");
            Point point = new Point();
            Random r1 = new Random();
            for (int i = 0; i < 15;)
            {
                point.X = r1.Next(classHandle.rectCoordinate.Left + 10, classHandle.rectCoordinate.Right - 30);
                point.Y = r1.Next(classHandle.rectCoordinate.Top + 10, classHandle.rectCoordinate.Bottom - 30);
                if (!_myDictionary.ContainsKey(point))
                {
                    _myDictionary.Add(point, Cursors.IBeam);
                    i++;
                } 
            }
            Log.Message("Get 15 random coordinates in title area where cursor type is DEFAULT");
            Log.Message("{0},{1},{2},{3}", appHandle.rectCoordinate.Left, appHandle.rectCoordinate.Right, appHandle.rectCoordinate.Top, appHandle.rectCoordinate.Bottom);
            for (int i = 0; i < 15; )
            {
                point.X = r1.Next(appHandle.rectCoordinate.Left + 10, appHandle.rectCoordinate.Right - 10);
                point.Y = r1.Next(appHandle.rectCoordinate.Top + 10, classHandle.rectCoordinate.Top - 10);
                if (!_myDictionary.ContainsKey(point))
                {
                    _myDictionary.Add(point, Cursors.Default);
                    i++;
                }
            }
            Log.Message("Get 8 coordinates in title area where cursor type is DOUBLE ARROW");
            point.X = appHandle.rectCoordinate.Left + 1; point.Y = appHandle.rectCoordinate.Top + 1;
            _myDictionary.Add(point, Cursors.SizeNWSE);
            point.X = appHandle.rectCoordinate.Right - 1; point.Y = appHandle.rectCoordinate.Bottom - 1;
            _myDictionary.Add(point, Cursors.SizeNWSE);
            point.X = appHandle.rectCoordinate.Left + 1; point.Y = appHandle.rectCoordinate.Bottom - 1;
            _myDictionary.Add(point, Cursors.SizeNESW);
            point.X = appHandle.rectCoordinate.Right - 1; point.Y = appHandle.rectCoordinate.Top + 1;
            _myDictionary.Add(point, Cursors.SizeNESW);
            point.X = appHandle.rectCoordinate.Left + (appHandle.rectCoordinate.Right - appHandle.rectCoordinate.Left) / 2; point.Y = appHandle.rectCoordinate.Top + 1;
            _myDictionary.Add(point, Cursors.SizeNS);
            point.X = appHandle.rectCoordinate.Left + (appHandle.rectCoordinate.Right - appHandle.rectCoordinate.Left) / 2; point.Y = appHandle.rectCoordinate.Bottom - 1;
            _myDictionary.Add(point, Cursors.SizeNS);
            point.X = appHandle.rectCoordinate.Left + 1; point.Y = (appHandle.rectCoordinate.Bottom - appHandle.rectCoordinate.Top)/2;
            _myDictionary.Add(point, Cursors.SizeWE);
            point.X = appHandle.rectCoordinate.Right - 1; point.Y = (appHandle.rectCoordinate.Bottom - appHandle.rectCoordinate.Top) / 2;
            _myDictionary.Add(point, Cursors.SizeWE);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Move the cursor to various positions and check if the shape of cursor changes accordingly");
            foreach (Point p1 in _myDictionary.Keys)
            {
                Log.Message("Set the cursor position");
                if (!AccessInterface.SetFeature<bool, Point>(Features.CursorEvent, Action.SetMethod, p1))
                    Log.Fail("Error in setting Cursor Position.");
                else
                {
                    Log.Message("Get the Cursor Information");
                    cursorInfo cursorInfo = AccessInterface.GetFeature<cursorInfo>(Features.CursorEvent, Action.GetMethod, Source.AccessAPI);
                    Cursor cursor = new Cursor(cursorInfo.hCursor);
                    if (cursor.Equals(_myDictionary[p1]))
                        Log.Success("Correct Cursor Shape");
                    else
                        Log.Fail("Cursor Shape not matching");
                }
            }
        }
        private bool checkClassWithinApp(Rect appRect , Rect classRect)
        {
            if ((appRect.Left < classRect.Left) && (appRect.Top < classRect.Top) && (appRect.Right > classRect.Right) && (appRect.Bottom > classRect.Bottom))
                return true;
            else
                return false;
        }

    }
}