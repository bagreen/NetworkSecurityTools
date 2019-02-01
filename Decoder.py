"""
TODO: ADD ASCII, polyalphabetic, route cipher, two square, four square, enigma, scytale, vigenere

want to automate ways of cracking ciphers on this list
https://en.wikipedia.org/wiki/Classical_cipher

vigenere decoder
https://simonsingh.net/The_Black_Chamber/vigenere_cracking_tool.html

"""

from collections import Counter
import argparse
import base64
import copy
import math
import re
import string

# HELPING DICTIONARIES
letters_to_numbers = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
                      'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
                      'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18,
                      'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
                      'Y': 25, 'Z': 26}
numbers_to_letters = {z: x for x, z in letters_to_numbers.items()}
morse_to_english = {'.-...': '&', '--..--': ',', '....-': '4', '.....': '5',
                    '...---...': 'SOS', '-...': 'B', '-..-': 'X', '.-.': 'R',
                    '.--': 'W', '..---': '2', '.-': 'A', '..': 'I', '..-.': 'F',
                    '.----': '1', '-.-': 'K', '-..': 'D', '-....': '6', '-...-': '=',
                    '.': 'E', '.-..': 'L', '...': 'S', '..-': 'U', '..--..': '?',
                    '---': 'O', '.--.': 'P', '.-.-.-': '.', '--': 'M', '-.': 'N',
                    '....': 'H', '.----.': '\'', '...-': 'V', '--...': '7',
                    '-.-.-.': ';', '-....-': '-', '..--.-': '_', '-.--.-': ')',
                    '-.-.--': '!', '--.': 'G', '--.-': 'Q', '--..': 'Z', '-..-.': '/',
                    '.-.-.': '+', '-.-.': 'C', '---...': ':', '-.--': 'Y', '-': 'T',
                    '.--.-.': '@', '...-..-': '$', '.---': 'J', '-----': '0', '----.': '9',
                    '.-..-.': '\"', '-.--.': '(', '---..': '8', '...--': '3'}
english_dictionary = {}
english_dictionary2 = []
english_frequency = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'W', 'D', 'L', 'Y', 'K', 'C', 'U', 'M', 'F', 'G', 'P',
                     'B', 'V', 'J', 'X', 'Q', 'Z']
word_patterns = {}
verbose = False


# HELPING METHODS
def anagram(letters):
    return 'POLISH'
def blank_mapping():
    # Returns a dictionary value that is a blank cipherletter mapping:
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
            'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
            'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
            'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
def convert_hex(number):
    number = str(number)
    if number is '10':
        return 'A'
    elif number is '11':
        return 'B'
    elif number is '12':
        return 'C'
    elif number is '13':
        return 'D'
    elif number is '14':
        return 'E'
    elif number is '15':
        return 'F'
    elif number is 'A':
        return '10'
    elif number is 'B':
        return '11'
    elif number is 'C':
        return '12'
    elif number is 'D':
        return '13'
    elif number is 'E':
        return '14'
    elif number is 'F':
        return '15'
    else:
        return str(number)
def frequency_analysis(encoded):
    encoded_list = Counter(encoded).most_common(100)
    frequency_list = []

    for frequency in range(0, len(encoded_list)):
        if re.search('[a-zA-Z]', encoded_list[frequency][0]):
            frequency_list.append(encoded_list[frequency][0])

    return frequency_list
def gcd(first_num, second_num):
    while first_num != 0:
        first_num, second_num = second_num % first_num, first_num
    return second_num
def has_letters(encoded):
    return re.search('[a-zA-Z]', encoded) is not None
def is_english(message):
    if message is '':
        return False

    letters = ''
    for char in message:
        try:
            if char.isalpha() or char is ' ':
                letters += char
        except AttributeError:
            return False

    words = letters.split()

    matches = 0
    for word in words:
        if word.strip().upper() in english_dictionary:
            matches += 1

    if matches is len(words):
        return True
    else:
        return False
def is_hex(number):
    for character in str(number):
        if character.isalpha() and character not in ['A', 'B', 'C', 'D', 'E', 'F']:
            return False
    return True
def modulo_inverse(first_num, second_num):
    if gcd(first_num, second_num) != 1:
        return None  # No mod inverse if a & m aren't relatively prime.
    u1, u2, u3 = 1, 0, first_num
    v1, v2, v3 = 0, 1, second_num
    while v3 != 0:
        q = u3 // v3  # Note that // is the integer division operator.
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % second_num
def morse_converter(encoded):
    if len(Counter(encoded).most_common(3)) is 2:
        first_most_common = Counter(encoded).most_common(2)[0][0]
        second_most_common = Counter(encoded).most_common(2)[1][0]

        decoded1 = encoded.replace(first_most_common, '.').replace(second_most_common, '-')
        decoded2 = encoded.replace(first_most_common, '-').replace(second_most_common, '.')

        print()
        print('MORSE CODE CONVERTER')
        print('Output 1 :', decoded1)
        print('Output 2 :', decoded2)
def morse_encoder(encoded):
    decoded = ''
    english_to_morse = {z: x for x, z in morse_to_english.items()}

    for x in list(encoded.upper()):
        if x is not ' ':
            decoded = decoded + str(english_to_morse.get(x) + ' ')
    print()
    print('MORSE CODE ENCODER')
    print('English to Morse :', decoded)
def process_arguments():
    parser = argparse.ArgumentParser(description='Attempts to decrypt input in many different encryption types')
    parser.add_argument('input', help='The information you want to decrypt', )
    parser.add_argument('-f', '--file', help='Text file to decrypt')
    parser.add_argument('-v', '--verbose', help='Verbosity prints returned values even if they aren\'t words',
                        action='store_true')
    parser.add_argument('--affine', help='Affine cipher', action='store_true')
    parser.add_argument('--bacon', help='Bacon cipher', action='store_true')
    parser.add_argument('--base', help='Base cipher', action='store_true')
    parser.add_argument('--caesar', help='Caesar cipher', action='store_true')
    parser.add_argument('--morse', help='Morse cipher', action='store_true')
    parser.add_argument('--null', help='Null cipher', action='store_true')
    parser.add_argument('--polybius', help='Polybius cipher', action='store_true')
    parser.add_argument('--reverse', help='Reverse cipher', action='store_true')
    parser.add_argument('--route', help='Route cipher', action='store_true')
    parser.add_argument('--sub', help='Substitution cipher', action='store_true')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')
def rotate(encoded, rotation):
    decoded = ''

    for char in encoded.upper():
        if char.isalpha():
            decoded_letter = letters_to_numbers.get(char) + rotation

            if decoded_letter > 26:
                decoded_letter = decoded_letter - 26
            elif decoded_letter < 1:
                decoded_letter = decoded_letter + 26
            decoded = decoded + numbers_to_letters.get(decoded_letter)
        else:
            decoded = decoded + char
    return decoded
def setup_dictionary():
    if len(english_dictionary) is 0 and verbose is False:
        with open('words', 'r') as file:
            for word in file:
                english_dictionary[word.strip().upper()] = None
def setup_dictionary2():
    if len(english_dictionary2) is 0 and verbose is False:
        with open('words', 'r') as file:
            for word in file:
                english_dictionary2.append(word.rstrip())
def setup_patterns():
    fo = open('dictionary.txt')
    word_list = fo.read().split('\n')
    fo.close()

    for word in word_list:
        # Get the pattern for each string in wordList:
        pattern = word_pattern(word)

        if pattern not in word_patterns:
            word_patterns[pattern] = [word]
        else:
            word_patterns[pattern].append(word)
def word_pattern(word):
    word = word.upper()
    letter_numbers = {}
    pattern = []
    next_num = 0

    for char in word:
        if char not in letter_numbers:
            letter_numbers[char] = str(next_num)
            next_num += 1
        pattern.append(letter_numbers[char])
    return '.'.join(pattern)


# DECODERS
def affine(encoded):
    result = ''
    found = False

    for key in range(26 ** 2):
        key_a = key // 26
        key_b = key % 26

        if gcd(key_a, 26) != 1:
            continue

        if key_a < 0 or key_b > 25:
            continue

        decoded = ''
        mod_inverse_a = modulo_inverse(key_a, 26)

        for char in encoded.upper():
            if char.isalpha():
                char_index = letters_to_numbers.get(char) - 1  # ?
                decoded += str(numbers_to_letters.get((char_index - key_b) * mod_inverse_a % 26))
            else:
                decoded += char

        if (decoded != encoded.upper() and is_english(decoded)) or verbose:
            if found is False:
                found = True
                result += '\nAFFINE'
                # print()
                # print('AFFINE')
            # print('Key %s: %s' % (key, decoded))
            result += '\nKey %s: %s' % (key, decoded)

    return result
def bacon(encoded):
    result = ''

    bacon_to_english_1 = {'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E',
                          'aabab': 'F', 'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I',
                          'abaab': 'K', 'ababa': 'L', 'ababb': 'M', 'abbaa': 'N', 'abbab': 'O',
                          'abbba': 'P', 'abbbb': 'Q', 'baaaa': 'R', 'baaab': 'S', 'baaba': 'T',
                          'baabb': 'U', 'babaa': 'W', 'babab': 'X', 'babba': 'Y',
                          'babbb': 'Z'}
    bacon_to_english_2 = {'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E',
                          'aabab': 'F', 'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I', 'abaab': 'J',
                          'ababa': 'K', 'ababb': 'L', 'abbaa': 'M', 'abbab': 'N', 'abbba': 'O',
                          'abbbb': 'P', 'baaaa': 'Q', 'baaab': 'R', 'baaba': 'S', 'baabb': 'T',
                          'babaa': 'U', 'babab': 'V', 'babba': 'W', 'babbb': 'X', 'bbaaa': 'Y',
                          'bbaab': 'Z'}

    if len(Counter(encoded).most_common(3)) in (1, 2):
        first_most_common = Counter(encoded).most_common(2)[0][0]

        if len(Counter(encoded).most_common(3)) is 1:
            replaced1 = encoded.replace(first_most_common, 'a')
            replaced2 = encoded.replace(first_most_common, 'b')
        else:
            second_most_common = Counter(encoded).most_common(2)[1][0]

            options = [['c', 'd'], ['e', 'f'], ['g', 'h']]
            replacement_1 = ''

            replaced = []
            for option in options:
                if (option[0], option[1]) not in (first_most_common, second_most_common):
                    replacement_1 = encoded.replace(first_most_common, option[0]).replace(second_most_common, option[1])
                    replaced.append(option[0])
                    replaced.append(option[1])
                    break

            replaced1 = replacement_1.replace(replaced[0], 'a').replace(replaced[1], 'b')
            replaced2 = replacement_1.replace(replaced[0], 'b').replace(replaced[1], 'a')

        encoded1 = re.findall('.....', replaced1)
        encoded2 = re.findall('.....', replaced2)

        decoded11 = ''
        decoded12 = ''
        decoded21 = ''
        decoded22 = ''

        for letter in encoded1:
            if letter in bacon_to_english_1:
                decoded11 = decoded11 + str(bacon_to_english_1.get(letter))
            if letter in bacon_to_english_2:
                decoded21 = decoded21 + str(bacon_to_english_2.get(letter))

        for letter in encoded2:
            if letter in bacon_to_english_1:
                decoded12 = decoded12 + str(bacon_to_english_1.get(letter))
            if letter in bacon_to_english_2:
                decoded22 = decoded22 + str(bacon_to_english_2.get(letter))

        if len(decoded11) > 0 or len(decoded12) > 0 or len(decoded21) > 0 or len(decoded22) > 0:
            # print()
            # print('BACON')
            result += '\nBACON'
            if len(decoded11) > 0:
                result += '\nEncoding 1, Cipher 1: %s' % decoded11
                #                print('Encoding 1, Cipher 1:', decoded11)

                if 'I' in decoded11:
                    # print('Encoding 1, Cipher 1:', decoded11.replace('I', 'J'))
                    result += '\nEncoding 1, Cipher 1: %s' % decoded11.replace('I', 'J')
                if 'U' in decoded11:
                    # print('Encoding 1, Cipher 1:', decoded11.replace('U', 'V'))
                    result += '\nEncoding 1, Cipher 1: %s' % decoded11.replace('U', 'V')
            if len(decoded21) > 0:
                # print('Encoding 1, Cipher 2:', decoded21)
                result += '\nEncoding 1, Cipher 2: %s' % decoded21
            if len(decoded12) > 0:
                result += '\nEncoding 2, Cipher 1: %s' % decoded12
                #                print('Encoding 2, Cipher 1:', decoded12)

                if 'I' in decoded12:
                    # print('Encoding 2, Cipher 1:', decoded12.replace('I', 'J'))
                    result += '\nEncoding 2, Cipher 1: %s' % decoded12.replace('I', 'J')
                if 'U' in decoded12:
                    result += '\nEncoding 2, Cipher 1: %s' % decoded12.replace('U', 'V')
            #                    print('Encoding 2, Cipher 1:', decoded12.replace('U', 'V'))
            if len(decoded22) > 0:
                result += '\nEncoding 2, Cipher 2: %s' % decoded22
    #                print('Encoding 2, Cipher 2:', decoded22)
    return result
def base(encoded):
    result = ''
    bases = [2, 8, 16]

    for number in bases:
        if len(result) > 0:
            result += '\n'

        encoded_list = []

        if ' ' not in encoded:
            if number is 2:
                encoded_list = re.findall('........', encoded)
            if number is 8:
                encoded_list = re.findall('...', encoded)
            if number is 16:
                encoded_list = re.findall('..', encoded)
        else:
            encoded_list = encoded.split()
        decoded = ''

        try:
            for character in encoded_list:
                character = int(character, number)
                decoded = decoded + chr(character)

            if len(decoded) > 0 and (is_english(decoded) or verbose):
                if number is 2:
                    result += '\nBINARY'
                elif number is 8:
                    result += '\nOCTAL'
                elif number is 16:
                    result += '\nHEXADECIMAL'
                result += '\nDecoded: ' + decoded
        except (OverflowError, ValueError):
            pass

    # base16/hexadecimal
    try:
        decoded = base64.b16decode(encoded).decode('utf-8')
        if is_english(decoded) or verbose:
            if len(result) > 0:
                result += '\n'
            result += '\nBASE16\nDecoded: %s' % str(decoded)
    except base64.binascii.Error:
        pass

    # base32
    try:
        decoded = base64.b32decode(encoded).decode('utf-8')
        if is_english(decoded) or verbose:
            if len(result) > 0:
                result += '\n'
            result += '\nBASE32\nDecoded: %s' % str(decoded)
    except (base64.binascii.Error, UnicodeDecodeError):
        pass

    # base64/radix64
    try:
        decoded = base64.b64decode(encoded, validate=True).decode('utf-8')
        if is_english(decoded) or verbose:
            if len(result) > 0:
                result += '\n'
            result += '\nBASE64\nDecoded: %s' % str(decoded)
    except (base64.binascii.Error, UnicodeDecodeError):
        pass

    # base85/ascii85
    try:
        decoded = base64.a85decode(encoded).decode('utf-8')
        if is_english(decoded) or verbose:
            if len(result) > 0:
                result += '\n'
            result += '\nBASE85\nDecoded: %s' % str(decoded)
    except (base64.binascii.Error, ValueError):
        pass

    return result
def caesar(encoded):
    result = ''
    found = False

    if has_letters(encoded):
        for rotation in range(-25, 0):
            decoded = rotate(encoded, rotation)

            if is_english(decoded) or verbose is True:
                if found is False:
                    found = True
                    result += '\nCAESAR'

                if rotation >= -9:
                    result += '\nRotated %s : %s' % (rotation, decoded)
                else:
                    result += '\nRotated %s: %s' % (rotation, decoded)

    return result
def decimal_conversions(encoded, bases):
    decoding = []
    for number in bases:
        encoded_number = int(encoded)
        power = 0
        decoded = ''

        while encoded_number >= number ** power:
            power += 1

        while power >= 0:
            if encoded_number >= number ** power:
                times = encoded_number // (number ** power)
                decoded += convert_hex(times)
                encoded_number -= times * (number ** power)
            else:
                decoded += '0'
            power -= 1

        decoding.append(decoded)
    return decoding
def hex_conversions(encoded, bases):
    if is_hex(encoded) is False:
        return

    encoded_string = ''

    for i in range(len(encoded) - 1, -1, -1):
        encoded_string = encoded_string + encoded[i]

    result = 0
    times = 0

    for character in encoded_string:
        result = result + (int(convert_hex(character)) * (16 ** times))
        times += 1

    print(decimal_conversions(result, bases))
def morse(encoded):
    result = ''
    decoded = ''

    for letter in encoded.split():
        if letter in morse_to_english:
            decoded = decoded + str(morse_to_english.get(letter))
    if len(decoded) > 0 and (is_english(decoded) or verbose):
        result = '\nMORSE CODE\nMorse to English: ' + decoded

    return result
def null(encoded):
    result = ''

    if has_letters(encoded):
        # first letter of each word
        first_characters = ''
        for x in encoded.split():
            first_characters += x[0]

        # last letter of each word
        last_characters = ''
        for x in encoded.split():
            last_characters += x[len(x) - 1]

        # capitalized letters of string
        capital_letters = ''.join([c for c in encoded if c.isupper()])

        if is_english(first_characters) or is_english(last_characters) or is_english(capital_letters) or verbose:
            if len(first_characters) > 1 or len(last_characters) > 1 or len(capital_letters) > 1:
                result += '\nNULL'
                if len(first_characters) > 1 or verbose:
                    result += '\nFirst characters: ' + first_characters
                if len(last_characters) > 1 or verbose:
                    result += '\nLast characters : ' + last_characters
                if len(capital_letters) > 1 or verbose:
                    result += '\nCapital letters : ' + capital_letters

    return result
def polybius(encoded):
    check = list(encoded)
    try:
        for x in check:
            if int(x) > 5:
                return
    except ValueError:
        return
    row1 = 'ABCDE'
    row2 = 'FGHIK'
    row3 = 'LMNOP'
    row4 = 'QRSTU'
    row5 = 'VWXYZ'

    encoded = encoded.replace(' ', '')
    polybius_array = re.findall('..', encoded)
    decoded = ''

    for x in polybius_array:
        second_number = x[1]
        second_number = int(second_number)

        if x[0] == '1':
            decoded = decoded + row1[second_number - 1]
        elif x[0] == '2':
            decoded = decoded + row2[second_number - 1]
        elif x[0] == '3':
            decoded = decoded + row3[second_number - 1]
        elif x[0] == '4':
            decoded = decoded + row4[second_number - 1]
        elif x[0] == '5':
            decoded = decoded + row5[second_number - 1]

    if is_english(decoded) or verbose:
        print()
        print('POLYBIUS')
        print('Translation:', decoded)
def reverse(encoded):
    # reverses text input
    result = ''
    decoded = ''

    for i in range(len(encoded) - 1, -1, -1):
        decoded = decoded + encoded[i]

    if is_english(decoded) or verbose:
        result = '\nREVERSE\nReversed: ' + decoded

    return result
def route(encoded):
    result = ''

    if len(encoded) > 2:
        found = False

        for key in range(2, len(encoded)):
            columns = int(math.ceil(len(encoded) / float(key)))
            rows = key
            boxes = (columns * rows) - len(encoded)
            decoded_list = [''] * columns

            column = 0
            row = 0

            for character in encoded:
                decoded_list[column] += character
                column += 1

                if (column == columns) or (column == columns - 1 and row >= rows - boxes):
                    column = 0
                    row += 1
            decoded = ''.join(decoded_list)

            if is_english(decoded) or verbose:
                if found is False:
                    found = True
                    result = '\nROUTE'
                if key < 10:
                    result += '\nShift  %s: %s' % (key, decoded)
                else:
                    result += '\nShift %s: %s' % (key, decoded)

    return result
def substitution(encoded):
    intersected_map = blank_mapping()
    partially_decoded = encoded
    word_list = re.compile('[^A-Z\s]').sub('', encoded.upper()).split()

    for word in word_list:
        # Get a new word mapping for each encoded word:
        word_map = blank_mapping()

        word_pat = word_pattern(word)
        if word_pat not in word_patterns:
            continue  # This word was not in our dictionary, so continue.

        # Add the letters of each candidate to the mapping:
        for candidate in word_patterns[word_pat]:
            for i in range(len(word)):
                if candidate[i] not in word_map[word[i]]:
                    word_map[word[i]].append(candidate[i])

        # intersects
        intersect_map = blank_mapping()
        for letter in string.ascii_uppercase:
            if not intersected_map[letter]:
                intersect_map[letter] = copy.deepcopy(word_map[letter])
            elif not word_map[letter]:
                intersect_map[letter] = copy.deepcopy(intersected_map[letter])
            else:
                for mappedLetter in intersected_map[letter]:
                    if mappedLetter in word_map[letter]:
                        intersect_map[letter].append(mappedLetter)
        intersected_map = intersect_map

    # removes solved letters from map
    loop_again = True
    while loop_again:
        loop_again = False
        solved_letters = []
        for cipher_letter in string.ascii_uppercase:
            if len(intersected_map[cipher_letter]) == 1:
                solved_letters.append(intersected_map[cipher_letter][0])
        for cipher_letter in string.ascii_uppercase:
            for s in solved_letters:
                if len(intersected_map[cipher_letter]) != 1 and s in intersected_map[cipher_letter]:
                    intersected_map[cipher_letter].remove(s)
                    if len(intersected_map[cipher_letter]) == 1:
                        loop_again = True

    # now we have complete mapping, so let's decrypt
    key = ['x'] * 26
    for cipher_letter in string.ascii_uppercase:
        if len(intersected_map[cipher_letter]) == 1:
            # If there's only one letter, add it to the key.
            key_index = string.ascii_uppercase.find(intersected_map[cipher_letter][0])
            key[key_index] = cipher_letter
        else:
            partially_decoded = partially_decoded.replace(cipher_letter.lower(), '_')
            partially_decoded = partially_decoded.replace(cipher_letter.upper(), '_')
    key = ''.join(key)

    # decode message
    decoded = ''
    for char in partially_decoded:
        if char.upper() in key:
            # Encrypt/decrypt the symbol:
            index = key.find(char.upper())
            if char.isupper():
                decoded += string.ascii_uppercase[index].upper()
            else:
                decoded += string.ascii_uppercase[index].lower()
        else:
            decoded += char

    return '\nSUBSTITUTION\nDecoded: ' + decoded
def unsure(encoded):
    print(encoded)
    print()
    result = ''

    encoded_lines = encoded.splitlines()
    columns = []
    column_indices = []

    for column in range(0, len(encoded_lines[0])):
        if has_letters(encoded_lines[0][column]):
            column_indices.append(column)
        #matrix.append(line.split())

    for column_index in column_indices:
        column = []

        for line in encoded_lines:
            try:
                column.append(line[column_index])
            except IndexError:
                column.append(' ')
        columns.append(column)

    top_letters = encoded_lines[0].split()
    word = anagram(top_letters)

    sorted_columns = []

    for character in word:
        for column in columns:
            if column[0] is character:
                sorted_columns.append(column)

    decoded = word + '\n'

    for entry in range(1, len(sorted_columns[0])):
        for column in sorted_columns:
            decoded += column[entry]
    print(decoded)


# # vigenere
# def vigenere(encoded):
#     print('VIGENERE')
#
#     for word in englishDictionary:
#         key = re.sub('[\W_]+', '', word)
#         if key[:len(encoded)] not in keyList:
#             while len(key) < len(encoded):
#                 key = key + key
#             keyLetters = list(key.upper())
#             keyNumbers = []
#
#             for x in keyLetters:
#                 keyNumbers.append(alphaNum.get(x))
#             vigenereOutput = ''
#
#             for z in list(encoded):
#                 try:
#                     keyNum = int(keyNumbers[0])
#                 except IndexError:
#                     pass
#                 keyNum = keyNum - 1
#                 inbetween = int(alphaNum.get(z)) - keyNum
#                 del keyNumbers[0]
#
#                 if inbetween < 1:
#                     inbetween = 26 + inbetween
#                 vigenereOutput = vigenereOutput + numAlpha.get(str(inbetween))
#
#             if vigenereOutput in englishDictionary:
#                 print('OUTPUT:', vigenereOutput)
#                 print('KEY:', key[:len(encoded)])
#                 print()
#
#                 # solutions.update({:len(encoded):vigenereOutput})
#     if len(keyList) > 0:
#         for keyEntry in len(keyList):
#             print()
#             print()
#             print()
#             for k, v in d.items():
#                 print(k, v)
#             # print('Key:', keyList[keyEntry])
#             # print('Text:', textList[keyEntry])
#     print()
#
# def printing(answer):
#

def printing(result, cipher):
    # print(result)
    if len(result) is 0 and len(cipher) is not 0:
        print(cipher, 'cipher was not able to decrypt the ciphertext')
    elif len(result) is not 0:
        print(result)


def main():
    input = 'H I L O P S\n' \
            'l u e h t r\n' \
            'o t a h t y\n' \
            't n a w u t\n' \
            's y r t o i\n' \
            ': p t t h s\n' \
            '. o g / / o\n' \
            '1 r / l g O\n' \
            '    x R y'

    setup_dictionary2()
    # arguments = process_arguments()
    # argument = False

    # global verbose
    # verbose = arguments.verbose

    # print('Input:', arguments.input)
    #
    #
    #
    # if arguments.affine is True:
    #     setup_dictionary()
    #     printing(affine(arguments.input), 'Affine')
    #     argument = True
    # if arguments.bacon is True:
    #     setup_dictionary()
    #     printing(bacon(arguments.input), 'Bacon')
    #     argument = True
    # if arguments.base is True:
    #     setup_dictionary()
    #     printing(base(arguments.input), 'Base')
    #     argument = True
    # if arguments.caesar is True:
    #     setup_dictionary()
    #     printing(caesar(arguments.input), 'Caesar')
    #     argument = True
    # if arguments.morse is True:
    #     setup_dictionary()
    #     printing(morse(arguments.input), 'Morse')
    #     argument = True
    # if arguments.null is True:
    #     setup_dictionary()
    #     printing(null(arguments.input), 'Null')
    #     argument = True
    # if arguments.polybius is True:
    #     setup_dictionary()
    #     printing(affine(arguments.input), 'Polybius')
    #     argument = True
    # if arguments.reverse is True:
    #     setup_dictionary()
    #     printing(reverse(arguments.input), 'Reverse')
    #     argument = True
    # if arguments.route is True:
    #     setup_dictionary()
    #     printing(route(arguments.input), 'Route')
    #     argument = True
    # if arguments.sub is True:
    #     setup_dictionary()
    #     setup_patterns()
    #     printing(substitution(arguments.input), 'Substitution')
    #     argument = True
    # if argument is False:
    #     setup_dictionary()
    #     setup_patterns()
    #
    #     # printing(affine(arguments.input), '')
    #     printing(bacon(arguments.input), '')
    #     printing(base(arguments.input), '')
    #     printing(caesar(arguments.input), '')
    #     printing(morse(arguments.input), '')
    #     printing(null(arguments.input), '')
    #     printing(reverse(arguments.input), '')
    #     printing(route(arguments.input), '')
    #     printing(substitution(arguments.input), '')


if __name__ == '__main__':
    main()
