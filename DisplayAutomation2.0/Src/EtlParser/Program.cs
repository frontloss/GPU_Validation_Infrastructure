/**
* @file		Program.cs
* @brief	Implements the main function for the tool
*
* @author	Rohit Kumar
*/

using System;

namespace EtlParser
{
    class Program
    {
        /// <summary>
        /// Entry point for EtlParser. Takes full path of ETL file as input and generates multiple json reports based on ETL data.
        /// <example>EtlParser.exe GfxTrace.etl</example>
        /// </summary>
        /// <param name="args">Default command line arguments</param>
        static void Main(string[] args)
        {
            // Make sure ETL file path is provided in command line
            if (args.Length < 1)
            {
                Console.WriteLine("No ETL file provided");
                return;
            }

            String inputFile = args[0];
            // Make sure given ETL file is valid
            if (!System.IO.File.Exists(inputFile))
            {
                Console.WriteLine("Input file: {0} not found.", inputFile);
                return;
            }

            ParserConfig config;
            if (args.Length > 1)
            {
                config = new ParserConfig(Convert.ToUInt64(args[1]));
            }
            else
            {
                config = new ParserConfig(0xFFFF);
            }
            // Create master handler and process the input file
            MasterHandler masterHandler = new MasterHandler(config);
            masterHandler.Process(inputFile);
        }
    }
}
