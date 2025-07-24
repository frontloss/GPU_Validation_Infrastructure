using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;
using System.IO;
using System.Reflection;
using System.Diagnostics;
namespace Intel.VPG.Display.Automation
{
    public class ToolController : Controller
    {
        SearchViewModel viewModelObj=new SearchViewModel();
        
       
        public ActionResult Index()
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
          SearchViewModel obj=(SearchViewModel)  HttpContext.Session[id.ToString()];
            ToolViewModel model = new ToolViewModel();
            List<SelectListItem> featureList = new List<SelectListItem>();
            // List<Feature> features = ToolService.GetFeatureList();
            List<string> features = DataProvider.GetFeatureList();
            featureList.Add(new SelectListItem { Text = "Select Feature", Value = "Select", Selected = true });
            foreach (string feature in features)
            {
                featureList.Add(new SelectListItem { Text = feature, Value = feature });
            }
            model.list = featureList;          
            return View(model);
        }       
        [HttpPost]
        public ActionResult TestNameChanged(string argTestName)
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.TestName = argTestName;
            HttpContext.Session[id.ToString()] = viewModelObj;
            return Json(new { status=true });
        }
        [HttpPost]
        public ActionResult GetInterfaceForFeature(String selectedFeature)
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.FeatureSelectedByWeb = selectedFeature;
            HttpContext.Session[id.ToString()] = viewModelObj;
            return Json(new { interfaceList = DataProvider.GetInterfaceList(selectedFeature) });
        }
        [HttpPost]
        public ActionResult GetParameterForInterface(String selectedInterface)
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.InterfaceSelectedByWeb = selectedInterface;
            HttpContext.Session[id.ToString()] = viewModelObj;
            viewModelObj.DelegateCommand_InterfaceSelected(selectedInterface);
            foreach(string curKey in viewModelObj.ParameterContents.ParameterData.Keys)
            {
                if (viewModelObj.ParameterContents.ParameterData[curKey]!=null)
                    viewModelObj.parameterValue.Add(curKey, viewModelObj.ParameterContents.ParameterData[curKey].First());
                else
                    viewModelObj.parameterValue.Add(curKey, "");
            }
            HttpContext.Session[id.ToString()] = viewModelObj;
            return Json(new { parameterList = viewModelObj.ParameterContents.ParameterData });
        }
        [HttpPost]
        public ActionResult UpdateParameterDictionary(String argParameter,string argParamValue)
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.UpdateParameterDictionary(argParameter, argParamValue);
            HttpContext.Session[id.ToString()] = viewModelObj;
            return Json(new { status=true });
        }
        [HttpPost]
        public ActionResult AddCommandButtonClicked()
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            if (viewModelObj.DelegateCommand_AddCommandLine(viewModelObj.FeatureSelectedByWeb, viewModelObj.InterfaceSelectedByWeb))
            {
                HttpContext.Session[id.ToString()] = viewModelObj;
                return Json(new { command = viewModelObj.CommandLineList.Last() });
            }
            else
            {
                return Json(new { command="" });
            }
        }
        [HttpPost]
        public ActionResult ExecutionModeSelected(string argExecutionMode)
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.ExecutionMode = argExecutionMode;
            HttpContext.Session[id.ToString()] = viewModelObj;
            return Json(new {status=true});
        }
        [HttpPost]
        public ActionResult ExecuteButtonClicked()
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.DelegateCommand_ExecuteTest(viewModelObj.CommandLineList, viewModelObj.TestName, viewModelObj.ExecutionMode);            
            return Json(new { logName = viewModelObj.TestName });
        }
        [HttpPost]
        public ActionResult DelCommandClicked(int argIndex)
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            if (viewModelObj.CommandLineList.Count() > argIndex)
            {
                viewModelObj.CommandLineList.RemoveAt(argIndex);
                HttpContext.Session[id.ToString()] = viewModelObj;
                return Json(new { index = true });
            }
            else
            {
                return Json(new { index = false });
            }
        }
        [HttpPost]
        public ActionResult DelAllCommandClicked()
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            if (viewModelObj.CommandLineList.Count() >0)
            {
                viewModelObj.CommandLineList.Clear();
                HttpContext.Session[id.ToString()] = viewModelObj;
                return Json(new { index = true });
            }
            else
            {
                return Json(new { index = false });
            }
        }
        [HttpPost]
        public ActionResult MoveUpCommandClicked(string option )
        {
            return Json(new { index = true }); 
        }
         [HttpPost]
        public ActionResult LogHyperlinkClicked(string option )
        {
            Guid id = (Guid)HttpContext.Session["Guid"];
            viewModelObj = (SearchViewModel)HttpContext.Session[id.ToString()];
            viewModelObj.DelegateCommand_LogHyperlink();
            return Json(new { index = true }); 
        }
        public SearchViewModel GetMySessionObject( HttpContext current)
        {
            return current != null ? (SearchViewModel)current.Session["__MySessionObject"] : null;
        }
    }
}
