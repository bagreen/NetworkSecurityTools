# want to automate ways of cracking ciphers on this list
# https://en.wikipedia.org/wiki/Classical_cipher

import base64
from collections import Counter
import re
import string


# HELPING DICTIONARIES
alphaNum = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6',
            'G': '7', 'H': '8', 'I': '9', 'J': '10', 'K': '11', 'L': '12',
            'M': '13', 'N': '14', 'O': '15', 'P': '16', 'Q': '17', 'R': '18',
            'S': '19', 'T': '20', 'U': '21', 'V': '22', 'W': '23', 'X': '24',
            'Y': '25', 'Z': '26'}
baconEnglish1 = {'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E',
                 'aabab': 'F', 'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I',
                 'abaab': 'K', 'ababa': 'L', 'ababb': 'M', 'abbaa': 'N', 'abbab': 'O',
                 'abbba': 'P', 'abbbb': 'Q', 'baaaa': 'R', 'baaab': 'S', 'baaba': 'T',
                 'baabb': 'U', 'babaa': 'W', 'babab': 'X', 'babba': 'Y',
                 'babbb': 'Z'}
baconEnglish2 = {'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E',
                 'aabab': 'F', 'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I', 'abaab': 'J',
                 'ababa': 'K', 'ababb': 'L', 'abbaa': 'M', 'abbab': 'N', 'abbba': 'O',
                 'abbbb': 'P', 'baaaa': 'Q', 'baaab': 'R', 'baaba': 'S', 'baabb': 'T',
                 'babaa': 'U', 'babab': 'V', 'babba': 'W', 'babbb': 'X', 'bbaaa': 'Y',
                 'bbaab': 'Z'}
morseEnglish = {'.-...': '&', '--..--': ',', '....-': '4', '.....': '5',
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

englishDictionary = []

with open('anglo-saxon-surnames', 'r') as handle:
    for line in handle:
        englishDictionary.append(line.strip().upper())
englishDictionary.sort(key=lambda item: (len(item), item))


# HELPING METHODS
def frequency_analysis(encoded):
    encoded_list = Counter(encoded.upper()).most_common(100)
    frequency_list = []

    for frequency in range(0, len(encoded_list)):
        if has_letters(encoded_list[frequency][0]) is True:
            frequency_list.append(encoded_list[frequency][0])

    return frequency_list
def has_letters(encoded):
    return any(char.isalpha() for char in encoded)
def has_numbers(encoded):
    return any(char.isdigit() for char in encoded)
def has_symbols(encoded):
    return any(char in set(string.punctuation.replace("_", "")) for char in encoded)
def morse_converter(encoded):
    if len(Counter(encoded).most_common(3)) is 2:
        first_most_common = Counter(encoded).most_common(2)[0][0]
        second_most_common = Counter(encoded).most_common(2)[1][0]

        decoded1 = encoded.replace(first_most_common, '.').replace(second_most_common, '-')
        decoded2 = encoded.replace(first_most_common, '-').replace(second_most_common, '.')

        print('MORSE CODE CONVERTER')
        print('Output 1 :', decoded1)
        print('Output 2 :', decoded2)
        print()
def morse_encoder(encoded):
    decoded = ''
    english_to_morse = {z: x for x, z in morseEnglish.items()}

    for x in list(encoded.upper()):
        if x is not ' ':
            decoded = decoded + str(english_to_morse.get(x) + ' ')
    print('MORSE CODE ENCODER')
    print('English to Morse :', decoded)
    print()
def rotate(encoded, rotation):
    decoded = ''
    num_alpha = {z: x for x, z in alphaNum.items()}

    for character in list(encoded):
        if character is ' ':
            decoded = decoded + ' '
        else:
            decoded_letter = int(alphaNum.get(character)) + rotation

            if decoded_letter > 26:
                decoded_letter = decoded_letter - 26
            elif decoded_letter < 1:
                decoded_letter = decoded_letter + 26
            decoded = decoded + num_alpha.get(str(decoded_letter))
    return decoded
def word_check(word):
    return word in englishDictionary


# DECODERS
# BASES
def base16_decoder(encoded):  # base16/hexadecimal

    try:
        decoded = base64.b16decode(encoded)
        print('BASE16')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
        print()
    except base64.binascii.Error:
        pass
def base32_decoder(encoded):
    try:
        decoded = base64.b32decode(encoded)
        print('BASE32')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
        print()
    except base64.binascii.Error:
        pass
def base64_decoder(encoded):  # base64/radix64
    try:
        decoded = base64.b64decode(encoded, validate=True)
        print('BASE64')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
        print()
    except base64.binascii.Error:
        pass
def base85_decoder(encoded):  # base85/ascii85
    try:
        decoded = base64.a85decode(encoded)
        print('BASE85')
        print('Decoded :', str(decoded)[2:len(decoded) + 2])
        print()
    except base64.binascii.Error or ValueError:
        pass


# NUMBER BASE
def binary(encoded):
    encoded_list = encoded.split()
    decoded = ''

    try:
        for character in encoded_list:
            character = int(character, 2)
            decoded = decoded + chr(character)

        print('BINARY')
        print('Decoded :', decoded)
        print()
    except ValueError:
        pass
def octal(encoded):
    encoded_list = encoded.split()
    decoded = ''

    try:
        for character in encoded_list:
            character = int(character, 8)
            decoded = decoded + chr(character)

        print('OCTAL')
        print('Decoded :', decoded)
        print()
    except OverflowError:
        pass
    except ValueError:
        pass
def hexadecimal(encoded):
    encoded_list = encoded.split()
    decoded = ''

    try:
        for character in encoded_list:
            character = int(character, 16)
            decoded = decoded + chr(character)

        print('HEXADECIMAL')
        print('Decoded :', decoded)
        print()
    except OverflowError:
        pass
    except ValueError:
        pass


# OTHERS
def bacon(encoded):
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
            if letter in baconEnglish1:
                decoded11 = decoded11 + str(baconEnglish1.get(letter))
            if letter in baconEnglish2:
                decoded21 = decoded21 + str(baconEnglish2.get(letter))

        for letter in encoded2:
            if letter in baconEnglish1:
                decoded12 = decoded12 + str(baconEnglish1.get(letter))
            if letter in baconEnglish2:
                decoded22 = decoded22 + str(baconEnglish2.get(letter))

        if len(decoded11) > 0 or len(decoded12) > 0 or len(decoded21) > 0 or len(decoded22) > 0:
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
            print()
def caesar(encoded):
    print('CAESAR')
    for rotation in range(1, 25):
        print('Rotated', rotation * -1, ':', rotate(encoded.upper(), rotation * -1))
    print()
def morse_decoder(encoded):
    decoded = ''

    for letter in encoded.split():
        if letter in morseEnglish:
            decoded = decoded + str(morseEnglish.get(letter))
    if len(decoded) > 0:
        print('MORSE CODE')
        print('Morse to English :', decoded)
        print()
def null(encoded):
    # first letter of each word
    first_letters = ''
    for x in encoded.split():
        first_letters += x[0]

    # last letter of each word
    last_letters = ''
    for x in encoded.split():
        last_letters += x[len(x) - 1]

    # capitalized letters of string
    capital_letters = ''.join([c for c in encoded if c.isupper()])

    if len(first_letters) > 1 or len(last_letters) > 1 or len(capital_letters) > 1:
        print('NULL')
        if len(first_letters) > 1:
            print('First letters :', first_letters)
        if len(last_letters) > 1:
            print('Last letters :', last_letters)
        if len(capital_letters) > 1:
            print('Capital letters :', capital_letters)
        print()
def polybius(encoded):
    check = list(encoded)
    for x in check:
        if int(x) > 5:
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
    print('POLYBIUS')
    print('Translation :', polybius_output)
    print()
def rail(encoded):
    if len(encoded) > 2:
        print('RAIL')
        rail_input = encoded.upper()

        for x in range(2, len(encoded)):
            rail_input = rail_input + encoded
            decoded = ''

            for y in range(0, len(encoded)):
                decoded = decoded + rail_input[x * y]
            print('Shift', x - 1, ': ', decoded)
        print()
def rot13(encoded):
    print('ROT13')
    print('Rotated -13 :', rotate(encoded.upper(), -13))
    print()


def monoalphabetic(encoded):
    encoded_list = encoded.split()
    smallest_word = encoded_list[0]
    encoding = ''

    for word in encoded_list:
        if len(word) < len(smallest_word):
            smallest_word = word

    for word in englishDictionary:
        if len(word) is len(smallest_word):
            encoding = 'test'


# polyalphabetic
# route cipher?  https://en.wikipedia.org/wiki/Transposition_cipher
# two square
# four square
# enigma
# scytale

'''
# vigenere
def vigenere(encoded):
    print('VIGENERE')
    key = ''
    solutions = {}
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

encodedText = 'Hereupon Legrand arose, with a grave and stately air, and brought me the beetle from a glass case in which it was enclosed. It was a beautiful scarabaeus, and, at that time, unknown to naturalists—of course a great prize in a scientific point of view. There were two round black spots near one extremity of the back, and a long one near the other. The scales were exceedingly hard and glossy, with all the appearance of burnished gold. The weight of the insect was very remarkable, and, taking all things into consideration, I could hardly blame Jupiter for his opinion respecting it.'
print('Input:', encodedText)
print()

print(frequency_analysis(encodedText))

# for value in englishDictionary:
#     print(value)

# print(word_check(encodedText))

# if has_letters(encodedText) is True and has_numbers(encodedText) is False and has_symbols(encodedText) is False:
#     rot13(encodedText)
#     caesar(encodedText)
#     null(encodedText)
#     rail(encodedText)
#     morse_encoder(encodedText)
#     # vigenere(encodedText)
# elif has_numbers(encodedText) is True and has_letters(encodedText) is False and has_symbols(encodedText) is False:
#     polybius(encodedText)
#
# base16_decoder(encodedText)
# base32_decoder(encodedText)
# base64_decoder(encodedText)
# base85_decoder(encodedText)
# binary(encodedText)
# octal(encodedText)
# hexadecimal(encodedText)
# bacon(encodedText)
# morse_decoder(encodedText)
# morse_converter(encodedText)
