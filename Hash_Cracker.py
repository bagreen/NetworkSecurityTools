import argparse, hashlib, time
CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', '{', ']', '}', '\\', '|', ';', ':', '\'', '\"', ',', '<', '.', '>', '/', '?']
MD5 = False
SHA1 = False
SHA224 = False
SHA256 = False
SHA384 = False
SHA512 = False

#processes flags
def process_arguments():
    parser = argparse.ArgumentParser(description='Decrypts hashes')

    parser.add_argument('-md5', help='md5 hashes', action='store_true')
    parser.add_argument('-sha1', help='sha1 hashes', action='store_true')
    parser.add_argument('-sha224', help='sha224 hashes', action='store_true')
    parser.add_argument('-sha256', help='sha256 hashes', action='store_true')
    parser.add_argument('-sha384', help='sha384 hashes', action='store_true')
    parser.add_argument('-sha512', help='sha512 hashes', action='store_true')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')

# checks hash against whatever hash is specified as an argument, SHA256 default
def get_hash(decrypted):
    decrypted_hash = ''

    if MD5 is True:
        decrypted_hash = hashlib.md5(decrypted.encode('utf-8')).hexdigest()
    elif SHA1 is True:
        decrypted_hash = hashlib.sha1(decrypted.encode('utf-8')).hexdigest()
    elif SHA224 is True:
        decrypted_hash = hashlib.sha224(decrypted.encode('utf-8')).hexdigest()
    elif SHA256 is True:
        decrypted_hash = hashlib.sha256(decrypted.encode('utf-8')).hexdigest()
    elif SHA384 is True:
        decrypted_hash = hashlib.sha384(decrypted.encode('utf-8')).hexdigest()
    elif SHA512 is True:
        decrypted_hash = hashlib.sha512(decrypted.encode('utf-8')).hexdigest()
    else:
        decrypted_hash = hashlib.sha256(decrypted.encode('utf-8')).hexdigest()
    return decrypted_hash.upper()


# brute forces hash
def decrypt(encrypted_hash):
    first_letter = CHARS[0]
    last_letter = CHARS[-1]
    decrypted = first_letter
    decrypted_hash = ''

    # runs until match is found
    while encrypted_hash != decrypted_hash:
        print('\r' + decrypted, end='')
        length = len(decrypted)
        last_char = decrypted[-1:]
        new_decryption = ''

        if last_char != last_letter:
            decrypted = decrypted[:-1] + CHARS[CHARS.index(last_char) + 1]

        else:
            pivot = False

            for i in range(length):
                if decrypted[length - 1 - i] == last_letter:
                    new_decryption += first_letter
                else:
                    new_decryption = decrypted[:length - 1 - i] + CHARS[CHARS.index(decrypted[length - 1 - i]) + 1] + new_decryption
                    pivot = True
                    break
            if pivot == False:
                new_decryption += first_letter

            decrypted = new_decryption

        decrypted_hash = get_hash(decrypted)
    print('\rFound ' + '\"' + decrypted + '\"')

def main():
    arguments = process_arguments()
    global MD5, SHA1, SHA224, SHA256, SHA384, SHA512
    MD5 = arguments.md5
    SHA1 = arguments.sha1
    SHA224 = arguments.sha224
    SHA256 = arguments.sha256
    SHA384 = arguments.sha384
    SHA512 = arguments.sha512

    start_time = time.time()
    encrypted_hash = '9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08'

    decrypt(encrypted_hash.upper())

    print('%s seconds' % (time.time() - start_time))

if __name__ == '__main__':
    main()
