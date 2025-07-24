using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
   public interface IView
    {
        void AddParameterUiElementToGrid();
        void ClearParameterUiElementFromGrid();
        void AddComboBoxItem();
        void DeleteCommandFromListBox();
        void OpenBatchFile();
        void ClearCommandLineListBox();
    }
}
