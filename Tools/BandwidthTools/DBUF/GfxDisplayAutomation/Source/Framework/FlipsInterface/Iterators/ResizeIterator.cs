using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Intel.VPG.Display.FlipsInterface.MPO;

namespace Intel.VPG.Display.FlipsInterface.Iterators
{
   public  enum RESIZE_DIRECTION { UP, DOWN, LEFT, RIGHT, DIAGONALLY_UP, DIAGONALLY_DOWN };

    public class ResizeIterator : IPlaneVariationIterator
    {
        LinkedListNode<RESIZE_DIRECTION> direction_node = new LinkedListNode<RESIZE_DIRECTION>(RESIZE_DIRECTION.DIAGONALLY_DOWN);

        DIVA_M_RECT_CLR currentDstRect = new DIVA_M_RECT_CLR();
        MPOPlane mpoLayer = null;
        Dim lowerBound = new Dim();
        Dim upperBound = new Dim();
        Dim planeDim = new Dim();
        Random rnd = new Random();
        SurfacePoint startPoint = new SurfacePoint();
        int iterate_limit = 0;
        uint increment_value = 1;
        double scale_factor = 3;
        bool isBaseLayer = false;

        public ResizeIterator(MPOPlane plane, List<RESIZE_DIRECTION> resizeSequence, bool baseLayer, int iter_limit= 1000, uint inc_step = 5)
        {
            this.iterate_limit = iter_limit;
            this.increment_value = inc_step;
            this.isBaseLayer = baseLayer;

            if (resizeSequence != null)
            {                
                LinkedList<RESIZE_DIRECTION> ll = new LinkedList<RESIZE_DIRECTION>();
                ll.AddFirst(direction_node);
                foreach (RESIZE_DIRECTION dir in resizeSequence)
                {
                    ll.AddLast(dir);
                }
            }


            this.mpoLayer = Helper.Clone(plane);

            if (Helper.isPlanarFormat(this.mpoLayer.PixelFormat) == true)
            {
                this.mpoLayer.Attributes.MPOBlend = DIVA_MPO_BLEND_VAL_CLR.DIVA_MPO_BLEND_VAL_ALPHA_DISABLED;
                scale_factor = 2;
            }
            else
            {
                scale_factor = 3;
            }


            if (isBaseLayer == true)
            {
                currentDstRect.Right = ConfigItem.CurrentMode.Width;
                currentDstRect.Bottom = ConfigItem.CurrentMode.Height;
            }
            else
            {
                currentDstRect.Right = this.mpoLayer.Attributes.MPOSrcRect.Right;
                currentDstRect.Bottom = this.mpoLayer.Attributes.MPOSrcRect.Bottom;
            }

            this.planeDim.Width = currentDstRect.Right;
            this.planeDim.Height = currentDstRect.Bottom;

            upperBound.Width = ConfigItem.CurrentMode.Width;
            upperBound.Height = ConfigItem.CurrentMode.Height;

            double down_scale_width_limit = Math.Floor((double)this.planeDim.Width / scale_factor);
            double down_scale_height_limit = Math.Floor((double)this.planeDim.Height / scale_factor);

            lowerBound.Width = (uint)down_scale_width_limit;
            lowerBound.Height = (uint)down_scale_height_limit;

            mpoLayer.Attributes.MPODstRect.Right = currentDstRect.Right;
            mpoLayer.Attributes.MPODstRect.Bottom = currentDstRect.Bottom;
            mpoLayer.Attributes.MPOClipRect = mpoLayer.Attributes.MPODstRect;

            
            startPoint.X = 0;
            startPoint.Y = 0;

            if (isBaseLayer == false)
            {
                ChangeStartPoint();
            }
        }


        private bool ChangeStartPoint()
        {
            Dim bound = new Dim();
            bound.Width = (ConfigItem.CurrentMode.Width - this.planeDim.Width);
            bound.Height = (ConfigItem.CurrentMode.Height - this.planeDim.Height);

            bool check = false;
            do
            {
                startPoint.X = (uint)rnd.Next(0, (int)bound.Width);
                startPoint.Y = (uint)rnd.Next(0, (int)bound.Height);

                check = ((startPoint.X + 100 + planeDim.Width) < ConfigItem.CurrentMode.Width);
                check = check && ((startPoint.Y + 100 + planeDim.Height) < ConfigItem.CurrentMode.Height);
            } while (check == false);

            this.currentDstRect.Left = startPoint.X;
            this.currentDstRect.Top = startPoint.Y;
            this.currentDstRect.Right = this.currentDstRect.Left + this.planeDim.Width;
            this.currentDstRect.Bottom = this.currentDstRect.Top + this.planeDim.Height;
            return true;
        }

        private void NextDirection()
        {
            if (this.direction_node.Next == null)
            {
                this.ChangeStartPoint();
                this.direction_node = this.direction_node.List.First;
            }
            else
            {
                this.direction_node = this.direction_node.Next;
            }
        }

        private bool Next()
        {
            bool switch_direct = false;
            Dim currentDim = new Dim();


            RESIZE_DIRECTION path = this.direction_node.Value;
            if (iterate_limit <= 0)
            {
                return false;
            }

            if (isBaseLayer == false)
            {
                switch (path)
                {
                    case RESIZE_DIRECTION.DOWN:
                        //TODO: Increment destination Y
                        currentDstRect.Bottom = currentDstRect.Bottom + increment_value;
                        break;
                    case RESIZE_DIRECTION.UP:
                        currentDstRect.Bottom = currentDstRect.Bottom - increment_value;                        
                        break;
                    case RESIZE_DIRECTION.LEFT:                       
                        currentDstRect.Right = currentDstRect.Right - increment_value;                        
                        break;
                    case RESIZE_DIRECTION.RIGHT:
                        //TODO: Decrement destination Height
                        currentDstRect.Right = currentDstRect.Right + increment_value;
                        break;
                    case RESIZE_DIRECTION.DIAGONALLY_UP:
                        currentDstRect.Right = currentDstRect.Right - increment_value;
                        currentDstRect.Bottom = currentDstRect.Bottom - increment_value;
                        break;
                    case RESIZE_DIRECTION.DIAGONALLY_DOWN:
                        //TODO: Diagonally down
                        currentDstRect.Bottom = currentDstRect.Bottom + increment_value;
                        currentDstRect.Right = currentDstRect.Right + increment_value;
                        break;
                }

                currentDim.Width = (currentDstRect.Right - currentDstRect.Left);
                currentDim.Height = (currentDstRect.Bottom - currentDstRect.Top);

                if (currentDim.Width == 0)
                {
                    return false;
                }

                if (currentDim.Height == 0)
                {
                    return false;
                }


                if (currentDim.Width <= lowerBound.Width)
                {
                    currentDstRect.Right = currentDstRect.Right + increment_value;
                    if (path == RESIZE_DIRECTION.LEFT || path == RESIZE_DIRECTION.DIAGONALLY_UP)
                    {
                        switch_direct = true;
                    }
                }

                if (currentDim.Height <= lowerBound.Height)
                {
                    currentDstRect.Bottom = currentDstRect.Bottom + increment_value;
                    if (path == RESIZE_DIRECTION.UP || path == RESIZE_DIRECTION.DIAGONALLY_UP)
                    {
                        switch_direct = true;
                    }
                }

                currentDim.Width = (currentDstRect.Right - currentDstRect.Left);
                currentDim.Height = (currentDstRect.Bottom - currentDstRect.Top);

                if (currentDim.Width > upperBound.Width || currentDstRect.Right >= ConfigItem.CurrentMode.Width)
                {
                    currentDstRect.Right = currentDstRect.Right - increment_value;
                    if (path == RESIZE_DIRECTION.RIGHT || path == RESIZE_DIRECTION.DIAGONALLY_DOWN)
                        switch_direct = true;
                }

                if (currentDim.Height > upperBound.Height || currentDstRect.Bottom >= ConfigItem.CurrentMode.Height)
                {
                    currentDstRect.Bottom = currentDstRect.Bottom - increment_value;
                    if (path == RESIZE_DIRECTION.DOWN || path == RESIZE_DIRECTION.DIAGONALLY_DOWN)
                        switch_direct = true;
                }

                currentDstRect.Left = startPoint.X;
                currentDstRect.Top = startPoint.Y;

                if (switch_direct)
                {
                    this.NextDirection();
                }
            }
            else
            {
                currentDstRect.Right = ConfigItem.CurrentMode.Width;
                currentDstRect.Bottom = ConfigItem.CurrentMode.Height;
                iterate_limit = 1;
            }

            iterate_limit--;
            Console.WriteLine("Iteration limit = {0}", iterate_limit);
            return true;
        }


        MPOPlane IPlaneVariationIterator.NextVariationPlane()
        {
            MPOPlane plane = null;

            if (this.isBaseLayer == false)
            {
                if (this.Next() == false)
                {
                    return null;
                }
            }

            plane = Helper.Clone(this.mpoLayer);
            plane.Attributes.MPODstRect = currentDstRect;
            plane.Attributes.MPOClipRect = currentDstRect;
            return plane;
        }


        public bool NextVariationPlane(ref MPOPlane plane)
        {            

            if (this.isBaseLayer == false)
            {
                if (this.Next() == false)
                {
                    return false;
                }
            }
            
            plane.Attributes.MPODstRect = currentDstRect;
            plane.Attributes.MPOClipRect = currentDstRect;
            return true;
        }
    }
}
