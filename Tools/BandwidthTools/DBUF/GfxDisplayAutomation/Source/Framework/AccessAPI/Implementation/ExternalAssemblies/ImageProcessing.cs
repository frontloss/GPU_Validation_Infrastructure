namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Xml.Serialization;
    using System.IO;

    public class ImageProcessing : FunctionalBase, ISetMethod, IParse, IGetMethod
    {
        public object GetMethod(object argMessage)
        {
            ImageProcessingParams imageProcessParams = argMessage as ImageProcessingParams;

            if (imageProcessParams.ImageProcessingOption == ImageProcessOptions.GetPixelInfo)
            {
                string sourceFile = imageProcessParams.SourceImage;
                if (File.Exists(sourceFile))
                {
                    PixelColorInfo pixelInfo = new PixelColorInfo();
                    System.Drawing.Bitmap img1 = new System.Drawing.Bitmap(sourceFile);
                    System.Drawing.Color img1_ref = img1.GetPixel(imageProcessParams.pixelPosition.x, imageProcessParams.pixelPosition.y);

                    pixelInfo.Red = img1_ref.R;
                    pixelInfo.Green = img1_ref.G;
                    pixelInfo.Blue = img1_ref.B;
                    pixelInfo.Alpha = img1_ref.A;

                    imageProcessParams.pixelColorInfo = pixelInfo;
                }
                else
                {
                    if (!File.Exists(sourceFile))
                        Log.Fail("File {0} does not  exist", sourceFile);
                }
            }
            return imageProcessParams;
        }

        public bool SetMethod(object argMessage)
        {
            bool status = true;
            ImageProcessingParams imageProcessParams = argMessage as ImageProcessingParams;

            if (imageProcessParams.ImageProcessingOption == ImageProcessOptions.CompareImages)
            {
                status = CheckCorruption(imageProcessParams.SourceImage, imageProcessParams.TargetImage);
            }

            return status;
        }

        private bool CheckCorruption(string sourceFile, string targetFile)
        {
            int corruption = 0;
            int Rtol = 5, Gtol = 5, Btol = 5;
            bool status = true;
            double deviationAccepted = 3;

            
            if (File.Exists(sourceFile) && File.Exists(targetFile))
            {
                System.Drawing.Bitmap img1 = new System.Drawing.Bitmap(targetFile);
                System.Drawing.Bitmap img2 = new System.Drawing.Bitmap(sourceFile);

                for (int j = 0; j < img1.Height; j++)
                {
                    for (int i = 0; i < img1.Width; i++)
                    {
                        System.Drawing.Color img1_ref = img1.GetPixel(i, j);
                        System.Drawing.Color img2_ref = img2.GetPixel(i, j);

                        if (Math.Abs(img1_ref.R - img2_ref.R) > Rtol || Math.Abs(img1_ref.G - img2_ref.G) > Gtol || Math.Abs(img1_ref.B - img2_ref.B) > Btol)
                        {
                            corruption++;
                        }
                    }
                }
                Log.Message("Number of pixels Corrupted  for {0} are {1}", targetFile, corruption);

                double ratio = 0;
                ratio = ((double)corruption / (img1.Width * img1.Height)) * 100;

                if (corruption == 0)
                    Log.Message("No corruption for " + targetFile);
                else if (deviationAccepted > ratio)
                {
                    Log.Alert("Thin corruption of {0}% for {1} ", ratio, targetFile);
                }
                else
                {
                    status = false;
                    Log.Fail("Thick corruption of {0}% for {1} ", ratio, targetFile);
                }
            }
            else
            {
                status = false;
                if(!File.Exists(sourceFile))
                Log.Fail("source file {0} does not  exist", sourceFile);
                if (!File.Exists(targetFile))
                    Log.Fail(" target file {0} does not exist",targetFile);
            }

            return status;
        }

        public void Parse(string[] args)
        {
            ImageProcessingParams imageProcessParams = new ImageProcessingParams();
            ImageProcessOptions optionSelected;
            if (args.Length == 4 && args[0].ToLower().Contains("set") && Enum.TryParse<ImageProcessOptions>(args[1], true, out optionSelected))
            {
                imageProcessParams.ImageProcessingOption = optionSelected;
                imageProcessParams.SourceImage = args[2];
                imageProcessParams.TargetImage = args[3];

                SetMethod(imageProcessParams);
            }
            else if (args.Length == 2 && args[0].ToLower().Contains("get"))
            {

            }
            else
                this.HelpText();
        }      
     
        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe ImageProcessing set/get ImageProcessOptions FileName1 <FileName2> <pixelInfo>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe ImageProcessing set CompareImages sourceFileName TargetFileName");
            Log.Message(sb.ToString());
        }
    }
}