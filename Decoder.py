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
dictionary = {}
english_frequency = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'W', 'D', 'L', 'Y', 'K', 'C', 'U', 'M', 'F', 'G', 'P',
                     'B', 'V', 'J', 'X', 'Q', 'Z']
word_patterns = {}
verbose = False


# HELPING METHODS
def anagram(scrambled):
    upper = False
    if scrambled.isupper():
        upper = True
        scrambled = scrambled.lower()
    anagrams = []
    setup_dictionary()
    length = len(scrambled)

    for word in dictionary:
        if len(word) is length:
            scrambled_list = list(scrambled)

            for character in word:
                if character not in scrambled_list:
                    break
                scrambled_list.remove(character)

            if len(scrambled_list) is 0:
                if upper is True:
                    word = word.upper()
                anagrams.append(word)
    anagrams.sort()

    return anagrams
def blank_mapping():
    # Returns a dictionary value that is a blank cipherletter mapping:
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
            'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
            'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
            'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
def convert_hex(number):
    number = str(number).strip()
    if number == '10':
        return 'A'
    elif number == '11':
        return 'B'
    elif number == '12':
        return 'C'
    elif number == '13':
        return 'D'
    elif number == '14':
        return 'E'
    elif number == '15':
        return 'F'
    elif number == 'A':
        return '10'
    elif number == 'B':
        return '11'
    elif number == 'C':
        return '12'
    elif number == 'D':
        return '13'
    elif number == 'E':
        return '14'
    elif number == 'F':
        return '15'
    else:
        return number
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
        if word.strip().lower() in dictionary:
            matches += 1

    if matches is len(words):
        return True
    else:
        return False
def is_hexadecimal(encoded):
    for character in encoded:
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
    result = ''
    if len(Counter(encoded).most_common(3)) is 2:
        first_most_common = Counter(encoded).most_common(2)[0][0]
        second_most_common = Counter(encoded).most_common(2)[1][0]

        decoded1 = encoded.replace(first_most_common, '.').replace(second_most_common, '-')
        decoded2 = encoded.replace(first_most_common, '-').replace(second_most_common, '.')

        result = '\nMORSE CODE CONVERTER\nOutput 1 : ' + decoded1 + '\nOutput 2: ' + decoded2
    return result
def morse_encoder(encoded):
    decoded = '\nEnglish to Morse: '
    english_to_morse = {z: x for x, z in morse_to_english.items()}

    for x in list(encoded.upper()):
        if x is not ' ':
            decoded = decoded + str(english_to_morse.get(x) + ' ')

    return decoded
def process_arguments():
    parser = argparse.ArgumentParser(description='Attempts to decrypt input in many different encryption types')

    # options
    parser.add_argument('input', help='The information you want to decrypt', )
    parser.add_argument('-f', '--file', help='Text file to decrypt')
    parser.add_argument('-v', help='Prints all returned values', action='store_true')
    parser.add_argument('-b', '--big', help='Use a larger dictionary file instead', action='store_true')

    # ciphers
    parser.add_argument('--affine', help='Affine cipher', action='store_true')
    parser.add_argument('--bacon', help='Bacon cipher', action='store_true')
    parser.add_argument('--base', help='Base cipher', action='store_true')
    parser.add_argument('--caesar', help='Caesar cipher', action='store_true')
    parser.add_argument('--morse', help='Morse cipher', action='store_true')
    parser.add_argument('--null', help='Null cipher', action='store_true')
    parser.add_argument('--polybius', help='Polybius cipher', action='store_true')
    parser.add_argument('--reverse', help='Reverse cipher', action='store_true')
    parser.add_argument('--route', help='Route cipher', action='store_true')
    parser.add_argument('--substitution', help='Substitution cipher', action='store_true')

    # convert
    parser.add_argument('-bin', '--binary', help='Convert binary numbers to other numbers', action='store_true')
    parser.add_argument('-oct', '--octal', help='Convert octal numbers to other numbers', action='store_true')
    parser.add_argument('-dec', '--decimal', help='Convert decimal numbers to other numbers', action='store_true')
    parser.add_argument('-hex', '--hexadecimal', help='Convert hexadecimal numbers to other numbers', action='store_true')
    parser.add_argument('--english-morse', help='Translate to Morse code', action='store_true')


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
def setup_dictionary(): # 1331811MostCommonEnglishWords.txt
    if len(dictionary) is 0:
        with open('1331811MostCommonEnglishWords.txt', 'r') as file:
            for word in file:
                dictionary[word.rstrip()] = ''
def setup_patterns():
    if len(word_patterns) is 0 and verbose is False:
        setup_dictionary()
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
def base_16(encoded):
    result = ''
    try:
        decoded = base64.b16decode(encoded).decode('utf-8')
        if is_english(decoded) or verbose:
            if len(result) > 0:
                result += '\n'
            result += 'Decoded: %s' % str(decoded)
    except base64.binascii.Error:
        pass
    return result
def caesar(encoded):
    result = ''

    if has_letters(encoded):
        for rotation in range(-25, 0):
            decoded = rotate(encoded, rotation)

            if is_english(decoded) or verbose is True:
                if rotation >= -9:
                    result += '\nRotated %s : %s' % (rotation, decoded)
                else:
                    result += '\nRotated %s: %s' % (rotation, decoded)

    return result
def number_conversions(encoded, original_base, bases):
    result = ''

    if len(encoded) is 0:
        return ''

    elif original_base is 16:
        encoded.upper()

        if is_hexadecimal(encoded) is False:
            return ''

    elif original_base in [32, 64, 85]:
        try:
            if original_base is 32:
                return number_conversions(base64.b32decode(encoded).decode('utf-8'), 10, bases)
            elif original_base is 64:
                return number_conversions(base64.b64decode(encoded, validate=True).decode('utf-8'), 10, bases)
            elif original_base is 85:
                return number_conversions(base64.a85decode(encoded).decode('utf-8'), 10, bases)

        except (base64.binascii.Error, UnicodeDecodeError, ValueError):
            pass

    for base in bases:
        decoded = ''
        if base is 2:
            if len(result) > 0:
                decoded += '\n'
                
            decoded += 'Binary: '

            try:
                for number in encoded.split():
                    decoded += '{0:08b}'.format(int(number, original_base)) + ' '

                result += decoded
            except ValueError:
                result += ''
        elif base is 8:
            if len(result) > 0:
                result += '\n'
                
            decoded += 'Octal: '

            try:
                for number in encoded.split():
                    decoded += format(int(number, original_base), 'o') + ' '
                result += decoded
            except ValueError:
                result += ''
        elif base is 10:
            if len(result) > 0:
                result += '\n'
                
            decoded += 'Decimal: '

            try:
                for number in encoded.split():
                    decoded += str(int(number, original_base)) + ' '
                result += decoded
            except ValueError:
                result += ''
        elif base is 16:
            if len(result) > 0:
                result += '\n'
                
            decoded += 'Hexadecimal: '

            try:
                for number in encoded.split():
                    decoded += format(int(number, original_base), 'x') + ' '
                result += decoded
            except ValueError:
                result += ''
        elif base is 'text':
            decoded = ''

            if len(result) > 0:
                decoded += '\n'
                
            decoded += 'Text: '

            if original_base is not 10:
                result += decoded + number_conversions(number_conversions(encoded, original_base, [10]), 10, ['text'])
                continue

            elif is_english(encoded):
                result += decoded + encoded
                continue

            else:
                encoded_list = encoded.split()

                try:
                    for character in encoded_list:
                        decoded += chr(int(character))

                    if len(decoded) is not 0 and (is_english(decoded) or verbose):
                        if len(result) > 0:
                            decoded += '\n'

                        result += decoded

                except (OverflowError, ValueError):
                    continue

        else:
            if len(result) > 0:
                result += '\n'

            try:
                for number in encoded.split():
                    result += str(int(number, original_base)) + ' '
                result += decoded
            except ValueError:
                result += ''

    return result
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
        result = '\nReversed: ' + decoded

    return result
def route(encoded):
    result = ''

    if len(encoded) > 2:
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

    if decoded.isalpha() is False:
        return ''
    else:
        return '\nSUBSTITUTION\nDecoded: ' + decoded
def unsure(encoded):
    result = ''

    encoded_lines = encoded.splitlines()
    columns = []
    column_indices = []

    for column in range(0, len(encoded_lines[0])):
        if has_letters(encoded_lines[0][column]):
            column_indices.append(column)

    for column_index in column_indices:
        column = []

        for line in encoded_lines:
            try:
                column.append(line[column_index])
            except IndexError:
                column.append(' ')
        columns.append(column)

    top_letters = ''.join(encoded_lines[0].split())
    anagrams = anagram(top_letters)

    for word in anagrams:
        sorted_columns = []

        for character in word:
            for column in columns:
                if column[0] is character:
                    sorted_columns.append(column)

        decoded = '\n' + word + ': '

        for entry in range(1, len(sorted_columns[0])):
            for column in sorted_columns:
                decoded += column[entry]
        result += decoded
    return result
def vigenere(encoded):
    print()



def printing(result, cipher, single):
    if len(result) is not 0:
        if single is False:
            print('\n' + cipher.upper() + '\n' + result)
        else:
            print(result)
    elif len(result) is 0 and single is True:
        print(cipher + ' cipher was not able to decrypt the ciphertext')
def handle_arguments(arguments):
    if arguments.binary is True:
        printing(number_conversions(arguments.input, 2, [8, 10, 16, 'text']), 'Binary', False)
        
    if arguments.octal is True:
        printing(number_conversions(arguments.input, 8, [2, 10, 16, 'text']), 'Octal', False)
    
    if arguments.decimal is True:
        printing(number_conversions(arguments.input, 10, [2, 8, 16, 'text']), 'Decimal', False)

    if arguments.hexadecimal is True:
        printing(number_conversions(arguments.input, 16, [2, 8, 10, 'text']), 'Hexadecimal', False)

    if arguments.affine is True:
        printing(affine(arguments.input), 'Affine', True)
    
    if arguments.bacon is True:
        printing(bacon(arguments.input), 'Bacon', True)
    
    if arguments.base is True:
        printing(number_conversions(arguments.input, 2, [8, 10, 16, 'text']), 'Binary', False)
        printing(number_conversions(arguments.input, 8, [2, 10, 16, 'text']), 'Octal', False)
        printing(number_conversions(arguments.input, 10, [2, 8, 16, 'text']), 'Decimal', False)
        printing(number_conversions(arguments.input, 16, [2, 8, 10, 'text']), 'Hexadecimal', False)
    
    if arguments.caesar is True:
        printing(caesar(arguments.input), 'Caesar', True)
    
    if arguments.morse is True:
        printing(morse(arguments.input), 'Morse', True)
    
    if arguments.null is True:
        printing(null(arguments.input), 'Null', True)
    
    if arguments.polybius is True:
        printing(affine(arguments.input), 'Polybius', True)
    
    if arguments.reverse is True:
        printing(reverse(arguments.input), 'Reverse', True)
    
    if arguments.route is True:
        printing(route(arguments.input), 'Route', True)
    
    if arguments.substitution is True:
        printing(substitution(arguments.input), 'Substitution', True)
    
    if True not in vars(arguments).values():
        # printing(affine(arguments.input), 'Affine', False)
        printing(bacon(arguments.input), 'Bacon', False)
        printing(number_conversions(arguments.input, 10, [2, 8, 10, 16, 'text']), 'base', False)
        printing(caesar(arguments.input), 'Caesar', False)
        printing(morse(arguments.input), 'Morse', False)
        printing(morse_encoder(arguments.input), 'Morse Encoder', False)
        printing(morse_converter(arguments.input), 'Morse Converter', False)
        printing(null(arguments.input), 'Null', False)
        printing(reverse(arguments.input), 'Reverse', False)
        printing(route(arguments.input), 'Route', False)
        printing(substitution(arguments.input), 'Substitution', False)
def main():
    arguments = process_arguments()
    global verbose
    verbose = arguments.v
    setup_dictionary()
    setup_patterns()
    print('Input:', arguments.input)

    handle_arguments(arguments)

if __name__ == '__main__':
    main()
