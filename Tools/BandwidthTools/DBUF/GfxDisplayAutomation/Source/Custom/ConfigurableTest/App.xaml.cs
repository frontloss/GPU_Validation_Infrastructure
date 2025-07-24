using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Windows;
using Intel.VPG.Display.Automation;
namespace ConfigurableTest
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private void HandleApplicationStartup(object sender, StartupEventArgs e)
        {
            //var view = new MainWindow
            //{
            //    DataContext = new SearchViewModel()
            //};
            //this.MainWindow = view;

            //(this.MainWindow.DataContext as SearchViewModel).View = (this.MainWindow) as IView;
            //this.MainWindow.Show();

            this.MainWindow = new MainWindow();
            SearchViewModel svm = new SearchViewModel();
            svm.View = this.MainWindow as IView;
            this.MainWindow.DataContext = svm;
            this.MainWindow.Show();

            //this.MainWindow.DataContext = new SearchViewModel();                      
            //this.MainWindow.Show();
        }
    }
}
