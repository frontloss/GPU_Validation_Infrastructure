using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.IO;
using System.Reflection;
using System.Diagnostics;

namespace Intel.VPG.Display.Automation
{
  public static  class DataProvider
    {
      private static List<ParseAttribute> _featureData = default(List<ParseAttribute>);
      private static Dictionary<InterfaceType,string> _interfaceMapper=default(Dictionary<InterfaceType,string>);
      public static List<String> GetFeatureList()
      {
          string DLL_SOURCE = "Intel.VPG.Display.Automation.AccessAPI.dll";
          var dllPath = GetCurrentDirectory();
         
              dllPath=Path.Combine(dllPath,DLL_SOURCE);
          List<string> featureData = new List<string>();
         // string dllPath = Path.Combine(Directory.GetCurrentDirectory(), DLL_SOURCE);          
          Assembly assembly = Assembly.LoadFile(dllPath);
          var totalClass = assembly.GetTypes().Where(dI => dI.IsClass);
          int count = totalClass.Count();
          foreach (Type curType in totalClass)
          {
              MethodInfo method = curType.GetMethod("Parse");
              if (method != null)
              {
                  Attribute[] attributes = Attribute.GetCustomAttributes(method, typeof(ParseAttribute), true);
                  if (attributes.Count() > 0 && !featureData.Contains(curType.Name))
                  {
                      featureData.Add(curType.Name);
                  }
              }
          }
          return featureData;
      }
      public static List<string> GetInterfaceList(string argFeatureName)
      {
          _featureData = new List<ParseAttribute>();
          _interfaceMapper = new Dictionary<InterfaceType, string>();
          string DLL_SOURCE = "Intel.VPG.Display.Automation.AccessAPI.dll";
          var dllPath = GetCurrentDirectory();
              dllPath = Path.Combine(dllPath, DLL_SOURCE);
         // string dllPath = Path.Combine(Directory.GetCurrentDirectory(), "Intel.VPG.Display.Automation.AccessAPI.dll");
          Assembly assembly = Assembly.LoadFile(dllPath);
          var totalClass = assembly.GetTypes().Where(dI => dI.IsClass);
          int count = totalClass.Count();
          Type curType = totalClass.Where(dI => dI.Name == argFeatureName).FirstOrDefault();
          MethodInfo method = curType.GetMethod("Parse");
          if (method != null)
          {
              Attribute[] attributes = Attribute.GetCustomAttributes(method, typeof(ParseAttribute), true);
              foreach (Attribute curAttribute in attributes)
              {
                  ParseAttribute curParseAttribute = curAttribute as ParseAttribute;
                  _featureData.Add(curParseAttribute);
                  updateInterfaceMapper(curParseAttribute.InterfaceName);                
              }
          }
          List<string> interfaceName = new List<string>();
          interfaceName = _interfaceMapper.Where(di => di.Key != InterfaceType.None).Select(dI => dI.Value).ToList();
          return interfaceName;
      }
      public static List<string> GetParameterList(string argInterfaceSelected)
      {
          List<string> parameterData = new List<string>();
        InterfaceType interfaceSelected=_interfaceMapper.Where(dI => dI.Value == argInterfaceSelected).Select(dI => dI.Key).FirstOrDefault();
          foreach (ParseAttribute curParseAttribute in _featureData)
          {
              if (curParseAttribute.InterfaceName == interfaceSelected && curParseAttribute.InterfaceData != null)
              {
                  parameterData = curParseAttribute.InterfaceData.ToList();
              }
          }
          return parameterData;
      }

      public static List<string> AddUiElement(string argParamName)
      {
          List<string> enumValue = default(List<string>);
          string DLL_SOURCE = "Intel.VPG.Display.Automation.ConstantsLibrary.dll";
          var dllPath = GetCurrentDirectory();
        
              dllPath = Path.Combine(dllPath, DLL_SOURCE);
               // string dllPath = Path.Combine(Directory.GetCurrentDirectory(), "Intel.VPG.Display.Automation.ConstantsLibrary.dll");
                Assembly assembly = Assembly.LoadFile(dllPath);
                var totalEnum = assembly.GetTypes().Where(dI => dI.IsEnum);
                int enumCount = totalEnum.Count();
                Type matchType = totalEnum.Where(dI => dI.Name == argParamName).Select(dI => dI).FirstOrDefault();
                if (matchType == null)
                {
                    return enumValue;
                }
                else
                {
                    Type curTye = totalEnum.Where(dI => dI.Name == argParamName).FirstOrDefault();
                   var enumValues = Enum.GetValues(curTye);
                   enumValue = new List<string>();
                   foreach (var curEnumValue in enumValues)
                   {
                       enumValue.Add(curEnumValue.ToString());
                   }
                   return enumValue;
                }              
        }
      public static string GenerateCommandLine(Dictionary<string, string> argParameterData, string argFeatureSelected, string argInterfaceSelected)
      {
          InterfaceType interfaceSelected = _interfaceMapper.Where(dI => dI.Value == argInterfaceSelected).Select(dI => dI.Key).FirstOrDefault();
              String commandLine = "Execute.exe" + " " + argFeatureSelected + " " + argInterfaceSelected + " ";
              ParseAttribute curParseAttribute = _featureData.Where(dI => dI.InterfaceName == interfaceSelected).FirstOrDefault();
              string[] attributeList = curParseAttribute.InterfaceData;
              if (attributeList != null)
              {
                  int paramCount = attributeList.Length;
                  for (int i = 0; i < paramCount; i++)
                  {
                      commandLine = commandLine + argParameterData.ElementAt(i).Value;
                      if (attributeList.ElementAt(i).Split(':').Count() > 2)
                      {

                          string delimeter = attributeList.ElementAt(i).Split(':').Last().Trim();
                          if (String.Compare(delimeter, "sp", true) == 0)
                          {
                              delimeter = " ";
                          }
                          commandLine = commandLine + delimeter;
                      }
                  }
              }
              return commandLine;          
      }

      public static void updateInterfaceMapper(InterfaceType interfaceType)
      {
          switch (interfaceType)
          {
              case InterfaceType.IGet: _interfaceMapper.Add(InterfaceType.IGet, "Get"); break;
              case InterfaceType.IGetAll: _interfaceMapper.Add(InterfaceType.IGetAll, "GetAll"); break;
              case InterfaceType.IGetAllMethod: _interfaceMapper.Add(InterfaceType.IGetAllMethod, "GetAll"); break;
              case InterfaceType.IGetMethod: _interfaceMapper.Add(InterfaceType.IGetMethod, "Get"); break;
              case InterfaceType.ISet: _interfaceMapper.Add(InterfaceType.ISet, "Set"); break;
              case InterfaceType.ISetMethod: _interfaceMapper.Add(InterfaceType.ISetMethod, "Set"); break;
              case InterfaceType.ISetAllMethod: _interfaceMapper.Add(InterfaceType.ISetAllMethod, "SetAll"); break;
              case InterfaceType.ISetNoArgs: _interfaceMapper.Add(InterfaceType.ISetNoArgs, "SetNoArgs"); break;
              case InterfaceType.None: break;
              default: break;
          }
      }
     
      public static string ExecuteTest(List<string> argCommandLine, string argTestName,string argExecutionMode)
      {
          //create a batch file 
          string message="";
        
              string batchFileName = argTestName.Split('.').First().Trim();
              //string Dir = string.Format(Directory.GetCurrentDirectory());

              var Dir = GetCurrentDirectory();              
              string path = Path.Combine(Dir, batchFileName + ".bat"); //"test.bat"
              GetCurrentDirectory();

              string batchFileNameFlag = "BatchFileName" + batchFileName;
              if (!File.Exists(path))
              {
                  var batchFile = File.Create(path);
                  batchFile.Close();
              }
              int count = 0;
              if (File.Exists(path))
              {
                  using (StreamWriter w = new StreamWriter(path))
                  {
                      w.WriteLine("del *.xml");
                      w.WriteLine("del *.flg");
                      w.WriteLine("ECHO > RunningBatch.flg");
                      w.WriteLine("ECHO > {0}.flg", batchFileNameFlag);
                      while (count < argCommandLine.Count)
                      {
                          if (count + 1 == argCommandLine.Count)
                          {
                              w.WriteLine("ECHO > RunningLastTestInBatch.flg");
                          }
                          w.WriteLine(argCommandLine.ElementAt(count).ToString().Split(':').Last().Trim());
                          count++;
                      }
                      w.WriteLine("del *.flg");
                      w.Close();
                  }
                  if (argExecutionMode=="Batch")
                  {
                      message = "* Batch file created. Run " + batchFileName + ".bat in admin mode. Test results will be updated to " + batchFileName + ".html";
                
                  }
                  else if (argExecutionMode=="Local")
                  {
                     message= RunBatchCode(argTestName);
                  }
                  else
                  {
                      message="* Selected the Execution Mode";
                  }
          }
              return message;
      }
      private static string RunBatchCode(string argTestName)
      {
          #region batch code
          String batchFileName = argTestName.Trim();
          if (!batchFileName.EndsWith(".bat", true, null))
          {
              batchFileName = string.Concat(batchFileName, ".bat");
          }
          var Dir = GetCurrentDirectory();
         
          //create a batch file
          Process p = null;
          p = new Process();
          p.StartInfo.WorkingDirectory = Dir.ToString();
          p.StartInfo.FileName = batchFileName;
          p.StartInfo.CreateNoWindow = false;
          if (File.Exists(Path.Combine(Dir.ToString(), batchFileName)))
          {
              p.Start();
              p.WaitForExit();
              return string.Format("* Check the log: {0}",String.Concat(batchFileName.Split('.').First(),".html"));
          }
          else
          {
            return  string.Format("* {0} does not exist in {1}", batchFileName, Dir.ToString());
          }
          #endregion
      }
      public static string GetCurrentDirectory()
      {
          var Dir = System.AppDomain.CurrentDomain.BaseDirectory;
          string path = Dir.ToString();
          if (!Dir.ToString().EndsWith("Bin\\",StringComparison.CurrentCultureIgnoreCase))
          {
              DirectoryInfo info = Directory.GetParent(Dir);
              info = Directory.GetParent(info.FullName);
              info = Directory.GetParent(info.FullName);
              info = Directory.GetParent(info.FullName);
              path = Path.Combine(info.FullName, "Bin");
          }
        return path;
      }
     
    }
}
