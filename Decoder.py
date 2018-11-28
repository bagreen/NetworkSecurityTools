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
import re

# HELPING DICTIONARIES
letters_to_numbers = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6',
                      'G': '7', 'H': '8', 'I': '9', 'J': '10', 'K': '11', 'L': '12',
                      'M': '13', 'N': '14', 'O': '15', 'P': '16', 'Q': '17', 'R': '18',
                      'S': '19', 'T': '20', 'U': '21', 'V': '22', 'W': '23', 'X': '24',
                      'Y': '25', 'Z': '26'}
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
english_dictionary = []
english_frequency = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'W', 'D', 'L', 'Y', 'K', 'C', 'U', 'M', 'F', 'G', 'P',
                     'B', 'V', 'J', 'X', 'Q', 'Z']


# HELPING METHODS
def dictionary():
    with open('anglo-saxon-surnames', 'r') as handle:
        for line in handle:
            english_dictionary.append(line.strip().upper())
    english_dictionary.sort(key=lambda item: (len(item), item))
def frequency_analysis(encoded):
    encoded_list = Counter(encoded).most_common(100)
    frequency_list = []

    for frequency in range(0, len(encoded_list)):
        if re.search('[a-zA-Z]', encoded_list[frequency][0]):
            frequency_list.append(encoded_list[frequency][0])

    return frequency_list
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
    parser.add_argument('-i', '--input', help='The information you want to decrypt', default='')

    try:
        return list(vars(parser.parse_args()).values())
    except IOError:
        parser.error('Error')
def rotate(encoded, rotation):
    decoded = ''
    num_alpha = {z: x for x, z in letters_to_numbers.items()}

    for char in encoded:
        if char.isalpha() is True:
            decoded_letter = int(letters_to_numbers.get(char)) + rotation

            if decoded_letter > 26:
                decoded_letter = decoded_letter - 26
            elif decoded_letter < 1:
                decoded_letter = decoded_letter + 26
            decoded = decoded + num_alpha.get(str(decoded_letter))
        else:
            decoded = decoded + char
    return decoded
def word_check(word):
    return word in english_dictionary


# DECODERS
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
                print('Encoding 1, Cipher 1 :', decoded11)

                if 'I' in decoded11:
                    print('Encoding 1, Cipher 1 :', decoded11.replace('I', 'J'))
                if 'U' in decoded11:
                    print('Encoding 1, Cipher 1 :', decoded11.replace('U', 'V'))
            if len(decoded21) > 0:
                print('Encoding 1, Cipher 2 :', decoded21)
            if len(decoded12) > 0:
                print('Encoding 2, Cipher 1 :', decoded12)

                if 'I' in decoded12:
                    print('Encoding 2, Cipher 1 :', decoded12.replace('I', 'J'))
                if 'U' in decoded12:
                    print('Encoding 2, Cipher 1 :', decoded12.replace('U', 'V'))
            if len(decoded22) > 0:
                print('Encoding 2, Cipher 2 :', decoded22)
def base(encoded):
    # base16/hexadecimal
    try:
        decoded = base64.b16decode(encoded)
        print()
        print('BASE16')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
    except base64.binascii.Error:
        pass

    # base32
    try:
        decoded = base64.b32decode(encoded)
        print()
        print('BASE32')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
    except base64.binascii.Error:
        pass

    # base64/radix64
    try:
        decoded = base64.b64decode(encoded, validate=True)
        print()
        print('BASE64')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
    except base64.binascii.Error:
        pass

    # base85/ascii85
    try:
        decoded = base64.a85decode(encoded)
        print()
        print('BASE85')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
    except (base64.binascii.Error, ValueError):
        pass
def caesar(encoded):
    if re.search('[a-zA-Z]', encoded):
        print()
        print('CAESAR')
        for rotation in range(1, 25):
            print('Rotated', rotation * -1, ':', rotate(encoded.upper(), rotation * -1))
def monoalphabetic(encoded):
    # Need to figure out how to do this better...
    encoded = encoded.lower()

    frequency_list = frequency_analysis(encoded)

    for letter in range(0, 25):
        encoded = encoded.replace(frequency_list[letter], english_frequency[letter])
    print()
    print('MONOALPHABETIC')
    print('Decoded :', encoded)
def morse(encoded):
    decoded = ''

    for letter in encoded.split():
        if letter in morse_to_english:
            decoded = decoded + str(morse_to_english.get(letter))
    if len(decoded) > 0:
        print()
        print('MORSE CODE')
        print('Morse to English :', decoded)
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

            if len(decoded) > 0:
                print()
                if number is 2:
                    print('BINARY')
                elif number is 8:
                    print('OCTAL')
                elif number is 16:
                    print('HEXADECIMAL')
                print('Decoded :', decoded)
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

    if len(first_characters) > 1 or len(last_characters) > 1 or len(capital_letters) > 1:
        print()
        print('NULL')
        if len(first_characters) > 1:
            print('First characters :', first_characters)
        if len(last_characters) > 1:
            print('Last characters :', last_characters)
        if len(capital_letters) > 1:
            print('Capital letters :', capital_letters)
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
    polybius_output = ''

    for x in polybius_array:
        second_number = x[1]
        second_number = int(second_number)

        if x[0] == '1':
            polybius_output = polybius_output + row1[second_number - 1]
        elif x[0] == '2':
            polybius_output = polybius_output + row2[second_number - 1]
        elif x[0] == '3':
            polybius_output = polybius_output + row3[second_number - 1]
        elif x[0] == '4':
            polybius_output = polybius_output + row4[second_number - 1]
        elif x[0] == '5':
            polybius_output = polybius_output + row5[second_number - 1]
    print()
    print('POLYBIUS')
    print('Translation :', polybius_output)
def rail(encoded):
    if len(encoded) > 2:
        print()
        print('RAIL')
        rail_input = encoded.upper()

        for x in range(2, len(encoded)):
            rail_input = rail_input + encoded
            decoded = ''

            for y in range(0, len(encoded)):
                decoded = decoded + rail_input[x * y]
            print('Shift', x - 1, ': ', decoded)


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
encoded_text = process_arguments()[0]

if encoded_text is '':
    encoded_text = input()

print('Input :', encoded_text)

bacon(encoded_text)
base(encoded_text)
caesar(encoded_text)
morse(encoded_text)
morse_converter(encoded_text)
morse_encoder(encoded_text)
null(encoded_text)
number_base(encoded_text)
polybius(encoded_text)
rail(encoded_text)
