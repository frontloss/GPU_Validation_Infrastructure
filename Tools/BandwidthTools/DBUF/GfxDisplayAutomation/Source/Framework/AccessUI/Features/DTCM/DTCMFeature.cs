namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    using Ranorex;
    using Ranorex.Core;

    public class DTCMFeature : FunctionalBase, IGet, ISet, ISetMethod, IGetAll, IVisibleMethod
    {
        private MenuItem _context = null;

        public void ClearContext()
        {
            this._context = null;
        }
        public object Set
        {
            set 
            {
                IList<Ranorex.MenuItem> descendants = this._context.FindDescendants<Ranorex.MenuItem>();
                //Log.Verbose("*****************************");
                //descendants.ToList().ForEach(mI => Log.Verbose("{0}", mI.Text));
                //Log.Verbose("*****************************");

                MenuItem item = descendants.Where(mI => mI.Text.Equals(value.ToString())).FirstOrDefault();
                if (null != item)
                {
                    if (!item.Checked)
                    {
                        Log.Verbose("Selecting {0} from last navigated context", value);
                        item.Click();
                        Delay.Seconds(6);
                    }
                }
                else
                {
                    Log.Sporadic("Set:: Item {0} not found in DTCM!", value);
                    AccessUIExtensions.RebootHandler(base.CurrentMethodIndex);
                }
            }
        }
        public object Get
        {
            get
            {
                Log.Verbose("Fetching checked item from last navigated context");
                return this._context.FindDescendants<Ranorex.MenuItem>().First(m => m.Checked).Text; 
            }
        }
        public bool SetMethod(object argMessage)
        {
            ((List<string>)argMessage).ForEach(item =>
            {
                Log.Verbose("Navigating to {0}", item);
                IList<Ranorex.MenuItem> descendants = null;
                if (null == this._context)
                    descendants = DTCMRepo.Instance.ContextMenuExplorer.Self.FindDescendants<Ranorex.MenuItem>();
                else
                    descendants = this._context.FindDescendants<Ranorex.MenuItem>();

                this._context = descendants.Where(mI => mI.Text.Equals(item)).FirstOrDefault();
                if (null != this._context)
                    this._context.Click();
                else
                {
                    Log.Sporadic("SetMethod:: Item {0} not found in DTCM!", item);
                    AccessUIExtensions.RebootHandler(base.CurrentMethodIndex);
                }
            });
            Delay.Seconds(2);
            return (null != this._context);
        }
        public object GetAll
        {
            get 
            {
                if (null == this._context)
                {
                    Log.Verbose("Context menu reference not set earlier! Assuming initial menu.");
                    this._context = DTCMRepo.Instance.ContextMenuExplorer.Self.FindDescendant<Ranorex.MenuItem>();
                }
                Log.Verbose("Fetching all item(s) from last navigated context");
                return this._context.FindDescendants<Ranorex.MenuItem>().Select(mI => mI.Text).ToList(); 
            }
        }
        public bool VisibleMethod(object argMessage)
        {
            Log.Verbose("Checking visible status of {0}", argMessage);
            return ((List<string>)this.GetAll).Contains(argMessage.ToString());
        }
    }
}