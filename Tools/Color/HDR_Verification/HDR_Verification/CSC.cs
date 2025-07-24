using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HDR_Verification
{
    class CSC
    {
        static double[,] uBT2020RGBtoYUVCoeff ={ {0.2627,0.6780,0.0593},
                                                  {-0.13963,-0.36036,0.5},
                                                  {0.5 ,-0.45978,-0.04021}
                                                };

        public static uint[] uBPC = { 0, 0, 0, 0 };


        public static uint GetValue(uint value, int start, int end)
        {
            uint retvalue = value << (31 - end);
            retvalue >>= (31 - end + start);
            return retvalue;
        }

        public static double Convert_CSC_RegFormat_to_Coeff(uint cscCoeff)
        {
            double outVal = 0.0, scale_factor = 0.0;

            uint sign, exponent;
            int mantissa;

            uint positionOfPointFromRight = 0;


            sign = GetValue(cscCoeff, 15, 15);
            exponent = GetValue(cscCoeff, 12, 14);
            mantissa = (int)GetValue(cscCoeff, 3, 11);

            switch (exponent)
            {
                case 6:
                    positionOfPointFromRight = 7; break;
                case 7:
                    positionOfPointFromRight = 8; break;
                case 0:
                    positionOfPointFromRight = 9; break;
                case 1:
                    positionOfPointFromRight = 10; break;
                case 2:
                    positionOfPointFromRight = 11; break;
                case 3:
                    positionOfPointFromRight = 12; break;

            }

            scale_factor = Math.Pow(2, (double)positionOfPointFromRight);

            outVal = (double)mantissa / scale_factor;

            if (sign == 1)
                outVal = outVal * -1;

            return outVal;
        }

        public static uint Convert_CSC_Coeff_to_RegFormat(double coeff)
        {
            uint outVal = 0;

            uint sign = 0, exponent = 0, shift_factor = 0;
            int mantissa;

            if (coeff < 0)
                sign = 1;

            // range check
            if (coeff > 3.99)
                coeff = 3.9921875; // 11.1111111b -> 511/128 
            if (coeff < -4.00)
                coeff = -3.9921875;

            coeff = Math.Abs(coeff);

            if (coeff < 0.125)    //0.000bbbbbbbbb 
            {
                exponent = 3;
                shift_factor = 12;
            }
            else if (coeff < 0.25) //0.00bbbbbbbbb
            {
                exponent = 2;
                shift_factor = 11;
            }
            else if (coeff < 0.5)  //0.0bbbbbbbbb
            {
                exponent = 1;
                shift_factor = 10;
            }
            else if (coeff < 1.0)   // 0.bbbbbbbbb
            {
                exponent = 0;
                shift_factor = 9;
            }
            else if (coeff < 2.0)    //b.bbbbbbbb
            {
                exponent = 7;
                shift_factor = 8;
            }
            else if (coeff >= 2.0)
            {
                exponent = 6;
                shift_factor = 7;
            }


            mantissa = (int)Math.Round(coeff * (1 << (int)shift_factor));

            outVal = sign << 15;
            outVal = outVal | (exponent << 12);
            outVal = outVal | (uint)(mantissa << 3);

            return outVal;
        }

        public static void GetExpectedCSCCoeffValue(uint id)
        {

            double[,] CSCMatrix = new double[3, 3];

            double mul_factorY = 0.0, mul_factorUV = 0.0;

            uint CSCPostOffY = 0;

            if (uBPC[id] == 8)
            { mul_factorY = 219.0 / 255.0; mul_factorUV = 224.0 / 255.0; CSCPostOffY = 16; }
            else if (uBPC[id] == 10)
            { mul_factorY = 876.0 / 1023.0; mul_factorUV = 896.0 / 1023.0; CSCPostOffY = 64; }
            else if (uBPC[id] == 12)
            { mul_factorY = 2904.0 / 4095.0; mul_factorUV = 3584.0 / 4096.0; CSCPostOffY = 256; }

            //Console.WriteLine("Expected CSC Coeff");
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    if (i == 0)
                        CSCMatrix[i, j] = uBT2020RGBtoYUVCoeff[i, j] * mul_factorY;
                    else
                        CSCMatrix[i, j] = uBT2020RGBtoYUVCoeff[i, j] * mul_factorUV;

                    Convert_CSC_Coeff_to_RegFormat(CSCMatrix[i, j]);

                    //Console.WriteLine(CSCMatrix[i,j]);
                }
            }




        }
    }
}
