namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Reflection;
    using System.Collections.Generic;

    public static class AssemblyLoader
    {
        public static TestBase Load(this TestBase argContext, string argTestName)
        {
            Type type = null;
            Assembly assembly = TryGetTestClass(argTestName, out type);
            if (null == assembly)
            {
                assembly = assembly.Locate(argTestName);
                if (assembly == null)
                    return null;
            }
            if (null == type)
                type = type.Locate(assembly, argTestName);
            return Activator.CreateInstance(type) as TestBase;
        }
        public static void EnableReference<V>(this TestBase argContext, V argValue, ComponentType argType)
        {
            MethodInfo targetMethod = (from method in typeof(TestBase).GetMethods(BindingFlags.Instance | BindingFlags.NonPublic)
                                       where method.HasComponentType(argType)
                                       select method).SingleOrDefault();
            if (null != targetMethod)
                ((Action<V>)Delegate.CreateDelegate(typeof(Action<V>), argContext, targetMethod))(argValue);
        }
        public static int GetSkipToMethodIndex(this TestBase argContext)
        {
            int val = -1;
            FieldInfo field = GetBaseType(argContext.GetType()).GetFields(BindingFlags.Instance | BindingFlags.NonPublic).Where(fI => fI.Name.Equals("_newInvokeMethodIdx")).FirstOrDefault();
            if (null != field)
                val = Convert.ToInt32(field.GetValue(argContext));
            return val;
        }
        public static void ResetSkipMethodIndex(this TestBase argContext)
        {
            FieldInfo field = argContext.GetFieldInfo();
            if (null != field)
                field.SetValue(argContext, -1);
        }
        private static FieldInfo GetFieldInfo(this TestBase argContext)
        {
            return GetBaseType(argContext.GetType()).GetFields(BindingFlags.Instance | BindingFlags.NonPublic).Where(fI => fI.Name.Equals("_newInvokeMethodIdx")).FirstOrDefault();
        }
        public static List<MethodInfo> LoadMethods(this TestBase argContext)
        {
            return (from method in argContext.GetType().GetMethods()
                    where method.IsDefined(typeof(TestAttribute), false)
                    orderby method.GetMemberValue<int>("Order")
                    select method).ToList();
        }
        public static bool HasAttribute(this TestBase argContext, TestType argType)
        {
            return ((TestAttribute[])argContext.GetType().GetCustomAttributes<TestAttribute>(false))
                .ToList()
                .Exists(tA => tA.Type == argType);
        }
        public static V GetMemberValue<V>(this MethodInfo argMethodContext, string argMemberName)
        {
            CustomAttributeData cAttribData = argMethodContext.GetCustomAttributesData().FirstOrDefault();
            if (null != cAttribData)
            {
                CustomAttributeTypedArgument mValue = (from nData in cAttribData.NamedArguments
                                                       where nData.MemberName.Contains(argMemberName)
                                                       select nData.TypedValue).FirstOrDefault();
                if (null != mValue && null != mValue.Value)
                    return (V)mValue.Value;
            }
            return default(V);
        }

        private static Type GetBaseType(Type argContext)
        {
            Type baseType = argContext.BaseType;
            if (null != baseType && !baseType.Name.Equals(typeof(TestBase).Name))
                return GetBaseType(baseType);
            return baseType;
        }
        private static bool HasComponentType(this MethodBase argContext, ComponentType argType)
        {
            return ((FrameworkAttribute[])argContext.GetCustomAttributes(typeof(FrameworkAttribute), false))
                .ToList()
                .Exists(fA => fA.Type == argType);
        }
        public static List<TestType> GetAllTestTypeAttribute(this TestBase argContext)
        {
            List<TestType> _listTestType = new List<TestType>();
            if (argContext == null)
                return _listTestType;
            foreach (TestAttribute eachTestAttribute in argContext.GetType().GetCustomAttributes<TestAttribute>(false).ToList())
            {
                _listTestType.Add(eachTestAttribute.Type);
            }
            return _listTestType;
        }
        private static Assembly TryGetTestClass(string argTestName, out Type argType)
        {
            Assembly assembly = null;
            argType = null;
            string assemblyPattern = argTestName;
            int idx = argTestName.IndexOf("_");
            if (!idx.Equals(-1))
            {
                assemblyPattern = string.Concat(argTestName.Substring(0, idx), "*.dll");

                string[] assemblyList = Directory.GetFiles(Directory.GetCurrentDirectory(), assemblyPattern);
                foreach (string name in assemblyList)
                {
                    assembly = Assembly.Load(name.Substring(name.LastIndexOf("\\") + 1).Replace(".dll", string.Empty));
                    argType = assembly.GetTypes().SingleOrDefault(t => t.Name.ToLower().Equals(argTestName.ToLower()));
                    if (null != argType)
                        return assembly;
                }
            }
            return assembly;
        }
    }
}