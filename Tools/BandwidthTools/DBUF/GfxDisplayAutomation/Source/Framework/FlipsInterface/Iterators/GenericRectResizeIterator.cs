using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Intel.VPG.Display.FlipsInterface.MPO;

namespace Intel.VPG.Display.FlipsInterface.Iterators
{
    /// <summary>
    /// Resize the rectangle left, right, down, up, diagonally up, diagonally down
    /// </summary>
    public class GenericRectResizeIterator
    {

        #region members
        DIVA_M_RECT_CLR currentRect = new DIVA_M_RECT_CLR();
        Dim lowerBound = new Dim();
        Dim upperBound = new Dim();
        Dim planeDim = new Dim();
        SurfacePoint startPoint = new SurfacePoint();

        #endregion


        #region Properties

        public DIVA_M_RECT_CLR CurrentRect
        {
            get { return currentRect; }
            set { currentRect = value; }
        }

        #endregion



        public GenericRectResizeIterator(DIVA_M_RECT_CLR rect, Dim viewPort)
        {
            this.upperBound = viewPort;
            this.currentRect = rect;
            
            startPoint.X = rect.Left;
            startPoint.Y = rect.Top;

            lowerBound.Width = 32;
            lowerBound.Height = 32;
        }


        public bool Resize(string direction, uint increment_value)
        {
            Dim tmpDim = new Dim();
            RESIZE_DIRECTION path = RESIZE_DIRECTION.RIGHT;

            if (Enum.TryParse<RESIZE_DIRECTION>(direction, true, out path) == false)
            {
                path = RESIZE_DIRECTION.RIGHT;
            }

            switch (path)
            {
                case RESIZE_DIRECTION.DOWN:
                    //TODO: Increment destination Y
                    currentRect.Bottom = currentRect.Bottom + increment_value;
                    break;
                case RESIZE_DIRECTION.UP:
                    currentRect.Bottom = currentRect.Bottom - increment_value;
                    break;
                case RESIZE_DIRECTION.LEFT:
                    currentRect.Right = currentRect.Right - increment_value;
                    break;
                case RESIZE_DIRECTION.RIGHT:
                    //TODO: Decrement destination Height
                    currentRect.Right = currentRect.Right + increment_value;
                    break;
                case RESIZE_DIRECTION.DIAGONALLY_UP:
                    currentRect.Right = currentRect.Right - increment_value;
                    currentRect.Bottom = currentRect.Bottom - increment_value;
                    break;
                case RESIZE_DIRECTION.DIAGONALLY_DOWN:
                    //TODO: Diagonally down
                    currentRect.Bottom = currentRect.Bottom + increment_value;
                    currentRect.Right = currentRect.Right + increment_value;
                    break;
            }

            tmpDim.Width = (currentRect.Right - currentRect.Left);
            tmpDim.Height = (currentRect.Bottom - currentRect.Top);

            if (tmpDim.Width == 0)
            {
                return false;
            }

            if (tmpDim.Height == 0)
            {
                return false;
            }


            if (tmpDim.Width <= lowerBound.Width)
            {
                currentRect.Right = currentRect.Right + increment_value;
                return false;
            }

            if (tmpDim.Height <= lowerBound.Height)
            {
                currentRect.Bottom = currentRect.Bottom + increment_value;
                return false;
            }

            tmpDim.Width = (currentRect.Right - currentRect.Left);
            tmpDim.Height = (currentRect.Bottom - currentRect.Top);

            if (tmpDim.Width > upperBound.Width || currentRect.Right >= upperBound.Width)
            {
                currentRect.Right = currentRect.Right - increment_value;
                return false;
            }

            if (tmpDim.Height > upperBound.Height || currentRect.Bottom >= upperBound.Height)
            {
                currentRect.Bottom = currentRect.Bottom - increment_value;
                return false;
            }

            currentRect.Left = startPoint.X;
            currentRect.Top = startPoint.Y;
            return true;
        }
    }
}
