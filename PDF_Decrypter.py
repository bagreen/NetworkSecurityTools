import subprocess

name = 'test.pdf'

with open('englishDictionary', 'r') as handle:
    for line in handle:
        p = subprocess.Popen(['qpdf', '--password=' + line.strip(), '--decrypt', name, 'cracked.pdf'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        output, error = p.communicate()

        if p.returncode == 0:
            print('Password :', line)
            subprocess.run(['rm', 'cracked.pdf'])
            break
