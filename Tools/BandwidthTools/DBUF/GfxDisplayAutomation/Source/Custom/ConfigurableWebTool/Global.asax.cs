﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace ConfigurableWebTool
{
    // Note: For instructions on enabling IIS6 or IIS7 classic mode, 
    // visit http://go.microsoft.com/?LinkId=9394801

    public class MvcApplication : System.Web.HttpApplication
    {
        public static void RegisterGlobalFilters(GlobalFilterCollection filters)
        {
            filters.Add(new HandleErrorAttribute());
        }

        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            routes.MapRoute(
                "Default", // Route name
                "{controller}/{action}/{id}", // URL with parameters
                new { controller = "Home", action = "Index", id = UrlParameter.Optional } // Parameter defaults
            );

        }

        protected void Application_Start()
        {
            AreaRegistration.RegisterAllAreas();
            RegisterGlobalFilters(GlobalFilters.Filters);
            RegisterRoutes(RouteTable.Routes);             
        }
        
        void Session_Start(object sender, EventArgs e)
        {
            Intel.VPG.Display.Automation.SearchViewModel obj = new Intel.VPG.Display.Automation.SearchViewModel();
            obj.TestName = "Test1";
          Guid id=  System.Guid.NewGuid();
          HttpContext.Current.Session["Guid"] = id;
          HttpContext.Current.Session[id.ToString()] = obj;
        }

        void Session_End(object sender, EventArgs e)
        {
            int k = 1; 
        }
    }
}