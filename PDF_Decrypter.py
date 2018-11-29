import argparse
import subprocess


def process_arguments():
    parser = argparse.ArgumentParser(description='Decrypts PDFs using qpdf')
    parser.add_argument('pdf', help='Name of PDF to decrypt')
    parser.add_argument('-o', '--output',
                        help='Name of output file of PDF without password, by default it is \'cracked.pdf\'')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')


arguments = process_arguments()

output_file = ''

if arguments.o is not None:
    output_file = arguments.o
else:
    output_file = 'cracked.pdf'

with open('1000MostCommonPasswords.txt', 'r') as handle:
    for line in handle:
        p = subprocess.Popen(['qpdf', '--password=' + line.strip(), '--decrypt', arguments.pdf, output_file],
                             stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.communicate()

        if p.returncode == 0:
            print('Password :', line)
            subprocess.run(['rm', 'cracked.pdf'])
            break
