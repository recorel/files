using System;
using System.IO;

namespace EncryptionRoutineCeasar
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 3)
            {
                Console.WriteLine($"Usage prog input_file output_file shift");
                return;
            }

            var inputFile = args[0];
            var outputFile = args[1];
            int shift = 0;

            Int32.TryParse(args[2], out shift);


            FileStream fs = File.OpenRead(inputFile);
            BinaryReader reader = new BinaryReader(fs);


            long length = fs.Length;
            byte[] bytes = new byte[length];

            reader.Read(bytes, 0, bytes.Length);
            byte[] dBytes = new byte[fs.Length];

            for (int i = 0; i < dBytes.Length; i++)
            {
                dBytes[i] = (byte)(((uint)bytes[i] - (uint)shift) & 0xFF);
            }

            dBytes[0] = 0x4d; // M
            dBytes[1] = 0x44; // D
            dBytes[2] = 0x4d; // M
            dBytes[3] = 0x50; // P


            BinaryWriter binWriter = new BinaryWriter(File.Open(outputFile, FileMode.Create));
            binWriter.Write(dBytes);

            Console.WriteLine($"Input file: {args[0]}");
            Console.WriteLine($"Output file: {args[1]}");
            Console.WriteLine($"Shift: {args[2]}");
        }
    }
}
