namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    static class Extensions
    {
        internal static string ParseOutputFile(this string[] args)
        {
            string paramStr = string.Concat(string.Join(" ", args), "-END");
            Match getParam = Regex.Match(paramStr.ToLower(), @"-fileto(.+?)(-).+");
            string fileName = string.Empty;
            if (getParam.Success && getParam.Groups.Count.Equals(3))
                fileName = getParam.Groups[1].Value.Trim();
            if (!string.IsNullOrEmpty(fileName) && !fileName.Contains('.'))
                throw new Exception(string.Format("No filename specified in -fileTo argument:: {0}", fileName));
            return fileName;
        }
        internal static int ParseDisplaysSupported(this string[] args)
        {
            string paramStr = string.Concat(string.Join(" ", args), "-END");
            Match getParam = Regex.Match(paramStr.ToLower(), @"-maxdisp(.+?)(-).+");
            if (getParam.Success && getParam.Groups.Count.Equals(3))
                return Convert.ToInt32(getParam.Groups[1].Value.Trim());
            return 0;
        }
        internal static bool ParseHelpRequest(this string[] args)
        {
            return string.Join(" ", args).Contains("-help");
        }
        internal static List<string> ParseDisplayList(this string[] args)
        {
            List<string> displayList = null;
            string paramStr = string.Concat(string.Join(" ", args), "-END");
            Match getParam = Regex.Match(paramStr.ToLower(), @"-displays(.+?)(-).+");
            if (getParam.Success && getParam.Groups.Count.Equals(3))
                displayList = getParam.Groups[1].Value.Trim().Split(new[] { '+', ',', '-' }, StringSplitOptions.RemoveEmptyEntries).ToList();
            return displayList;
        }
    }
}