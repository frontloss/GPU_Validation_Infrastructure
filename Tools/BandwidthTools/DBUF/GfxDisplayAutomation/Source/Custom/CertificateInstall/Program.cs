using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;

namespace CertificateInstall
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length.Equals(0) || args.Length > 1)
                Console.WriteLine("Please provide path of the .cat file.");
            else
            {
                //Create new X509 store called teststore from the local certificate store.
                X509Store store = new X509Store(StoreName.TrustedPublisher, StoreLocation.LocalMachine);
                store.Open(OpenFlags.ReadWrite);

                //Create certificates from certificate files.
                //You must put in a valid path to three certificates in the following constructors.
                X509Certificate2 certificate1 = new X509Certificate2(args[0].ToString());

                //Add certificates to the store.
                store.Add(certificate1);

                X509Certificate2Collection storecollection = (X509Certificate2Collection)store.Certificates;
                Console.WriteLine("Store name: {0}", store.Name);
                Console.WriteLine("Store location: {0}", store.Location);
                foreach (X509Certificate2 x509 in storecollection)
                {
                    Console.WriteLine("certificate name: {0}", x509.Subject);
                }

                store.Close();
            }
        }
    }
}
