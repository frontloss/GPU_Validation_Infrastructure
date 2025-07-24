namespace Intel.VPG.Display.Automation
{
        public enum PlaneType
        {
            DISPLAY,
            SPRITE,
            CURSOR,
            FBC
        }

        public enum WatermarkType
        {
            WM_PIPE,
            WM_LP1,
            WM_LP2,
            WM_LP3
        }

        public enum WatermarkLevel
        {
            Level_0,
            Level_1,
            Level_2,
            Level_3,
            Level_4,
            Level_5,
            Level_6,
            Level_7,
        }

        public enum AllPlanes
        {
            Unsupported = -1,
            PLANE_A = 0,
            PLANE_B = 1,
            PLANE_C,
            SpriteA,
            SpriteB,
            SpriteC,
            CursorA,
            CursorB,
            CursorC
        }
}
