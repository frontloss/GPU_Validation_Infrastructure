namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Windows;
    using System.Windows.Controls;
    using System.Windows.Input;
    using System.IO;
    public partial class MainWindow : Window, IView
    {
        ListBoxItem _draggedItem = null;
 
        public MainWindow()
        {
            InitializeComponent();
            //  (this.DataContext as SearchViewModel).View = this as IView;
            Style itemContainerStyle = new Style(typeof(ListBoxItem));
            itemContainerStyle.Setters.Add(new Setter(ListBoxItem.AllowDropProperty, true));
            itemContainerStyle.Setters.Add(new EventSetter(ListBoxItem.PreviewMouseLeftButtonDownEvent, new MouseButtonEventHandler(CommandListBox_PreviewMouseLeftButtonDown)));
            itemContainerStyle.Setters.Add(new EventSetter(ListBoxItem.DropEvent, new DragEventHandler(MouseDrop)));
            CommandLineListBox.ItemContainerStyle = itemContainerStyle;
        }

        public void AddParameterUiElementToGrid()
        {
            Dictionary<string, List<string>> data = (this.DataContext as SearchViewModel).ParameterContents.ParameterData;
            Dictionary<string, string> parameterData = (this.DataContext as SearchViewModel).parameterValue;
            foreach (String curKey in data.Keys)
            {
                Label paramLabel = new Label();
                paramLabel.Content = curKey;
                if (data[curKey] != null)
                {

                    ComboBox paramTypecomboBox = new ComboBox();
                    // paramTypecomboBox.Style = this.Resources["comboboxStyle"] as Style;
                    foreach (var curEnum in data[curKey])
                    {
                        ComboBoxItem comboBoxItem = new ComboBoxItem();
                        comboBoxItem.Content = curEnum.ToString();
                        paramTypecomboBox.Items.Add(comboBoxItem);
                    }
                    paramTypecomboBox.SelectedIndex = 0;
                    paramTypecomboBox.Name = curKey.Split(':').First();
                    paramTypecomboBox.IsEnabled = true;
                    paramTypecomboBox.Height = 20;
                    paramTypecomboBox.SelectionChanged += paramTypecomboBox_SelectionChanged;
                    paramTypecomboBox.VerticalAlignment = VerticalAlignment.Top;

                    parameterData.Add(paramTypecomboBox.Name, data[curKey].First());//add to dictionary
                    #region my firstTrial
                    //Binding myBinding2 = new Binding();
                    //myBinding2.Source = this;
                    //myBinding2.Path = new PropertyPath("Parameter");
                    //paramTypecomboBox.SetBinding(ComboBox.SelectedItemProperty, myBinding2);
                    #endregion
                    #region option1
                    // Binding dataContextBinding = new Binding();
                    // dataContextBinding.Path = new PropertyPath("SelectedItem");
                    //// dataContextBinding.Source = this;
                    // BindingOperations.SetBinding(paramTypecomboBox, ComboBox.SelectedItemProperty, dataContextBinding);  
                    #endregion
                    parameterStackPanel.Children.Add(paramLabel);
                    parameterStackPanel.Children.Add(paramTypecomboBox);
                }
                else
                {
                    //create text box
                    TextBox paramTextBox = new TextBox();
                    paramTextBox.Name = curKey.Split(':').First().Trim().Replace(' ', '_'); ;
                    paramTextBox.Text = "";
                    parameterData.Add(paramTextBox.Name, "");//add to dictionary
                    paramTextBox.IsReadOnly = false;
                    paramTextBox.TextChanged += paramTextBox_TextChanged;

                    parameterStackPanel.Children.Add(paramLabel);
                    parameterStackPanel.Children.Add(paramTextBox);
                }
            }
        }

        private void paramTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            TextBox selectedTextBox = sender as TextBox;
            string value = selectedTextBox.Text;
            Dictionary<string, string> parameterData = (this.DataContext as SearchViewModel).parameterValue;
            if (parameterData.ContainsKey(selectedTextBox.Name))
            {
                parameterData[selectedTextBox.Name] = value;
            }
        }

        void paramTypecomboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ComboBox selectedComboBox = sender as ComboBox;
            string name = selectedComboBox.Name;
            Dictionary<string, string> parameterData = (this.DataContext as SearchViewModel).parameterValue;
            if (parameterData.ContainsKey(selectedComboBox.Name))
            {
                parameterData[selectedComboBox.Name] = selectedComboBox.SelectedItem.ToString().Split(':').Last().Trim();
            }
        }
        public void ClearParameterUiElementFromGrid()
        {
            parameterStackPanel.Children.Clear();
        }

        private void CommandListBox_PreviewMouseLeftButtonDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            CommandLineListBox.UnselectAll();
            if (sender is ListBoxItem)
            {
                _draggedItem = sender as ListBoxItem;
                DragDrop.DoDragDrop(_draggedItem, _draggedItem.Content, DragDropEffects.Move);
                _draggedItem.IsSelected = true;
            }
        }
        private void MouseDrop(object sender,DragEventArgs e)
        {
            int Sourceindex = CommandLineListBox.Items.IndexOf(_draggedItem);
            ListBoxItem droppedItem = sender as ListBoxItem;
            int destinationIndex = CommandLineListBox.Items.IndexOf(droppedItem);

            if (Sourceindex == destinationIndex)
            {
                CommandLineListBox.SelectedIndex = Sourceindex;
            }
            else
            {
                CommandLineListBox.Items.RemoveAt(Sourceindex);
                ListBoxItem insertedListBox = new ListBoxItem();
                insertedListBox.Content = _draggedItem.Content;
                CommandLineListBox.Items.Insert(destinationIndex, insertedListBox);
                UpdateCommandLineToViewmodel();
            }
        }
        public void AddComboBoxItem()
        {
            List<string> commandLineList = (this.DataContext as SearchViewModel).CommandLineList;
            string curCommand = commandLineList.Last();
            ListBoxItem commandItem = new ListBoxItem();
            commandItem.Content = curCommand;
            CommandLineListBox.Items.Add(commandItem);
            CommandLineListBox.AllowDrop = true;           
        }      
        public void DeleteCommandFromListBox()
        {
           int deleteIndex = CommandLineListBox.SelectedIndex;
           if (deleteIndex != -1)
           {
               CommandLineListBox.Items.RemoveAt(deleteIndex);
               UpdateCommandLineToViewmodel();
           }
        }
        private void UpdateCommandLineToViewmodel()
        {
            //update the list in view model
            List<string> commandLine = new List<string>();
            foreach (ListBoxItem curItem in CommandLineListBox.Items)
            {
                commandLine.Add(curItem.Content.ToString().Split(':').Last().Trim());
            }
            (this.DataContext as SearchViewModel).CommandLineList = commandLine;
        }


        public void OpenBatchFile()
        {
            Microsoft.Win32.OpenFileDialog fileDlg = new Microsoft.Win32.OpenFileDialog();
            fileDlg.InitialDirectory = Directory.GetCurrentDirectory();
            fileDlg.DefaultExt = ".bat";
            fileDlg.Filter = "Text documents(.bat)|*.bat";
            Nullable<bool> result = fileDlg.ShowDialog();
            if (result == true)
            {
                (this.DataContext as SearchViewModel).TestName = fileDlg.FileName.Split('\\').Last();

               // (this.DataContext as SearchViewModel).FeatureList
                List<string> batchFileLines = File.ReadAllLines(fileDlg.FileName).ToList();
                CommandLineListBox.Items.Clear();
                foreach (String curLine in batchFileLines)
                {
                    if (curLine.StartsWith("Execute"))
                    {
                        ListBoxItem curItem = new ListBoxItem();
                        curItem.Content = curLine;
                        CommandLineListBox.Items.Add(curItem);
                    }
                }
                UpdateCommandLineToViewmodel();
                
            }
        }


        public void ClearCommandLineListBox()
        {
            CommandLineListBox.Items.Clear();
        }
    }
}
