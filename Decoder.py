"""
TODO: ADD polyalphabetic, route cipher, two square, four square, enigma, scytale, vigenere
TODO: FIX monoalphabetic, frequency_analysis

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
english_frequency = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'W', 'D', 'L', 'Y', 'K', 'C', 'U', 'M', 'F', 'G', 'P',
                     'B', 'V', 'J', 'X', 'Q', 'Z']
word_patterns = {}


# HELPING METHODS
def blank_mapping():
    # Returns a dictionary value that is a blank cipherletter mapping:
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
           'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
           'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
           'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
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
    parser.add_argument('-i', '--input', help='The information or file you want to decrypt', default='')
    parser.add_argument('-v', '--verbose', help='Verbosity prints returned values even if they aren\'t words', action='store_true')

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
    with open('1331811MostCommonEnglishWords.txt', 'r') as file:
        for word in file:
            english_dictionary[word.strip().upper()] = None
def setup_patterns():
    fo = open('dictionary.txt')
    wordList = fo.read().split('\n')
    fo.close()

    for word in wordList:
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
                print()
                print('AFFINE')
            print('Key %s: %s' % (key, decoded))

            # decoded = rotate(encoded.upper(), rotation)
            # if is_english(decoded) or verbose is True:
            #     if found is False:
            #         found = True
            #         print()
            #         print('AFFINE')
            #     print('Rotated %s: %s' % (rotation, decoded))
def bacon(encoded):
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

    if len(Counter(encoded).most_common(3)) is 2:
        first_most_common = Counter(encoded).most_common(2)[0][0]
        second_most_common = Counter(encoded).most_common(2)[1][0]

        replaced1 = encoded.replace(first_most_common, 'a').replace(second_most_common, 'b')
        replaced2 = encoded.replace(first_most_common, 'b').replace(second_most_common, 'a')

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
            print()
            print('BACON')

            if len(decoded11) > 0:
                print('Encoding 1, Cipher 1:', decoded11)

                if 'I' in decoded11:
                    print('Encoding 1, Cipher 1:', decoded11.replace('I', 'J'))
                if 'U' in decoded11:
                    print('Encoding 1, Cipher 1:', decoded11.replace('U', 'V'))
            if len(decoded21) > 0:
                print('Encoding 1, Cipher 2:', decoded21)
            if len(decoded12) > 0:
                print('Encoding 2, Cipher 1:', decoded12)

                if 'I' in decoded12:
                    print('Encoding 2, Cipher 1:', decoded12.replace('I', 'J'))
                if 'U' in decoded12:
                    print('Encoding 2, Cipher 1:', decoded12.replace('U', 'V'))
            if len(decoded22) > 0:
                print('Encoding 2, Cipher 2:', decoded22)
def base(encoded):
    # base16/hexadecimal
    try:
        decoded = base64.b16decode(encoded)
        if is_english(decoded) or verbose:
            print()
            print('BASE16')
            print('Decoded:', str(decoded)[2:len(decoded) + 2])
    except base64.binascii.Error:
        pass

    # base32
    try:
        decoded = base64.b32decode(encoded)
        if is_english(decoded) or verbose:
            print()
            print('BASE32')
            print('Decoded:', str(decoded)[2:len(decoded) + 2])
    except base64.binascii.Error:
        pass

    # base64/radix64
    try:
        decoded = base64.b64decode(encoded, validate=True)
        if is_english(decoded) or verbose:
            print()
            print('BASE64')
            print('Decoded:', str(decoded)[2:len(decoded) + 2])
    except base64.binascii.Error:
        pass

    # base85/ascii85
    try:
        decoded = base64.a85decode(encoded)
        if is_english(decoded) or verbose:
            print()
            print('BASE85')
            print('Decoded:', str(decoded)[2:len(decoded) + 2])
    except (base64.binascii.Error, ValueError):
        pass
def caesar(encoded):
    found = False
    for rotation in range(-1, -26, -1):
        decoded = rotate(encoded, rotation)
        if is_english(decoded) or verbose is True:
            if found is False:
                found = True
                print()
                print('CAESAR')
            print('Rotated %s: %s' % (rotation, decoded))
def morse(encoded):
    decoded = ''

    for letter in encoded.split():
        if letter in morse_to_english:
            decoded = decoded + str(morse_to_english.get(letter))
    if len(decoded) > 0 and (is_english(decoded) or verbose):
        print()
        print('MORSE CODE')
        print('Morse to English:', decoded)
def number_base(encoded):
    bases = [2, 8, 16]

    for number in bases:
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
                print()
                if number is 2:
                    print('BINARY')
                elif number is 8:
                    print('OCTAL')
                elif number is 16:
                    print('HEXADECIMAL')
                print('Decoded:', decoded)
        except (OverflowError, ValueError):
            pass
def null(encoded):
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
    # if len(first_characters) > 1 or len(last_characters) > 1 or len(capital_letters) > 1:
        print()
        print('NULL')
        if len(first_characters) > 0:
            print('First characters:', first_characters)
        if len(last_characters) > 0:
            print('Last characters:', last_characters)
        if len(capital_letters) > 0:
            print('Capital letters:', capital_letters)
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
    decoded = ''

    for i in range(len(encoded) - 1, -1, -1):
        decoded = decoded + encoded[i]

    if is_english(decoded) or verbose:
        print()
        print('REVERSE')
        print('Reversed :', decoded)
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
    loopAgain = True
    while loopAgain:
        loopAgain = False
        solvedLetters = []
        for cipherletter in string.ascii_uppercase:
            if len(intersected_map[cipherletter]) == 1:
                solvedLetters.append(intersected_map[cipherletter][0])
        for cipherletter in string.ascii_uppercase:
            for s in solvedLetters:
                if len(intersected_map[cipherletter]) != 1 and s in intersected_map[cipherletter]:
                    intersected_map[cipherletter].remove(s)
                    if len(intersected_map[cipherletter]) == 1:
                        loopAgain = True

    # now we have complete mapping, so let's decrypt
    key = ['x'] * 26
    for cipherletter in string.ascii_uppercase:
        if len(intersected_map[cipherletter]) == 1:
            # If there's only one letter, add it to the key.
            keyIndex = string.ascii_uppercase.find(intersected_map[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            partially_decoded = partially_decoded.replace(cipherletter.lower(), '_')
            partially_decoded = partially_decoded.replace(cipherletter.upper(), '_')
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
    print()
    print('SUBSTITUTION')
    print('Decoded:', decoded)
def transposition(encoded):
    if len(encoded) > 2:
        found = False

        for key in range(2, len(encoded)):
            columns = int(math.ceil(len(encoded) / float(key)))
            rows = key
            boxes = (columns * rows) - len(encoded)
            decoded_list = [''] * columns

            column = 0
            row = 0

            for symbol in encoded:
                decoded_list[column] += symbol
                column += 1

                if (column == columns) or (column == columns - 1 and row >= rows - boxes):
                    column = 0
                    row += 1
            decoded = ''.join(decoded_list)

            if is_english(decoded) or verbose:
                if found is False:
                    found = True
                    print()
                    print("TRANSPOSITION")
                print('Shift %s: %s' % (key, decoded))
'''
# vigenere
def vigenere(encoded):
    print('VIGENERE')

    for word in englishDictionary:
        key = re.sub('[\W_]+', '', word)
        if key[:len(encoded)] not in keyList:
            while len(key) < len(encoded):
                key = key + key
            keyLetters = list(key.upper())
            keyNumbers = []

            for x in keyLetters:
                keyNumbers.append(alphaNum.get(x))
            vigenereOutput = ''

            for z in list(encoded):
                try:
                    keyNum = int(keyNumbers[0])
                except IndexError:
                    pass
                keyNum = keyNum - 1
                inbetween = int(alphaNum.get(z)) - keyNum
                del keyNumbers[0]

                if inbetween < 1:
                    inbetween = 26 + inbetween
                vigenereOutput = vigenereOutput + numAlpha.get(str(inbetween))

            if vigenereOutput in englishDictionary:
                print('OUTPUT:', vigenereOutput)
                print('KEY:', key[:len(encoded)])
                print()

                # solutions.update({:len(encoded):vigenereOutput})
    if len(keyList) > 0:
        for keyEntry in len(keyList):
            print()
            print()
            print()
            for k, v in d.items():
                print(k, v)
            # print('Key:', keyList[keyEntry])
            # print('Text:', textList[keyEntry])
    print()
'''


arguments = process_arguments()
encoded_text = arguments.input
verbose = arguments.verbose

setup_dictionary()
setup_patterns()

# encoded_text = process_arguments()[0]
# encoded_text = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
# verbose = process_arguments()[1]
# verbose = True

print('(Press Ctrl+D to quit at anytime)')
if encoded_text is '':
    print('Please enter your encoded message')
    encoded_text = input()

print('Input:', encoded_text)

# print('Is your input a word/words?')
#
# print(is_english(encoded_text))

affine(encoded_text)
bacon(encoded_text)
base(encoded_text)
caesar(encoded_text)
morse(encoded_text)
morse_converter(encoded_text)
morse_encoder(encoded_text)
null(encoded_text)
number_base(encoded_text)
polybius(encoded_text)
reverse(encoded_text)
substitution(encoded_text)
transposition(encoded_text)
