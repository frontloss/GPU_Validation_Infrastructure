using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Intel.VPG.Display.Automation
{
   public class Customer:BaseEntity
    {
        private int id;
        private string name;
        private string address;
        private int creditLimit;
        private bool activeStatus;
        private string remarks;

        public int Id
        {
            get { return id; }
            set { id = value; Notify("Id"); }
        }

        public string Name
        {
            get { return name; }
            set { name = value; Notify("Name"); }
        }

        public string Address
        {
            get { return address; }
            set { address = value; Notify("Address"); }
        }

        public int CreditLimit
        {
            get { return creditLimit; }
            set { creditLimit = value; Notify("CreditLimit"); }
        }

        public bool ActiveStatus
        {
            get { return activeStatus; }
            set { activeStatus = value; Notify("ActiveStatus"); }
        }

        public string Remarks
        {
            get { return remarks; }
            set { remarks = value; Notify("Remarks"); }
        }

        public override string ToString()
        {
            return string.Format(@"{0}, {1}, {2}, {3}, {4}, {5}",
                this.id, this.name, this.address, this.creditLimit,
                this.activeStatus, this.remarks);
        }
    }
}
