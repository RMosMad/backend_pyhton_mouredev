import math

def reverse_cipher(message: str) -> str:
    result = ''
    i = len(message) - 1
    while i >= 0:
        result = result + message[i]
        i -= 1
    return result


def caesar_cipher(message: str, key: int, mode) -> str:
    """
        The Caesar cipher works by substituting each letter of a message
        with a new letter after shifting the alphabet over
        :param message: Message to encrypt/decrypt
        :param key: Key
        :param mode: encrypt/decrypt
    """

    # Every possible symbol that can be encrypted:
    SYMBOLS = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz1234567890 !?.'

    translated = ''

    for symbol in message:
        # Note: Only symbols in the `SYMBOLS` string can be encrypted/decrypted.
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)

            # Perform encryption/decryption:
            if mode == 'encrypt':
                translatedIndex = symbolIndex + key
            elif mode == 'decrypt':
                translatedIndex = symbolIndex - key

            # Handle wrap-around, if needed:
            if translatedIndex >= len(SYMBOLS):
                translatedIndex = translatedIndex - len(SYMBOLS)
            elif translatedIndex < 0:
                translatedIndex = translatedIndex + len(SYMBOLS)

            translated = translated + SYMBOLS[translatedIndex]
        else:
            # Append the symbol without encrypting/decrypting:
            translated = translated + symbol

    return translated


def transposition_cipher(message: str, key: str, mode: str) -> str:
    """
    Given a plain-text message and a numeric key, cipher/de-cipher the given text using Columnar Transposition Cipher
    The Columnar Transposition Cipher is a form of transposition cipher just like Rail Fence Cipher
    . Columnar Transposition involves writing the plaintext out in rows, and then reading the ciphertext off in columns one by one.
    
    Encryption
        In a transposition cipher, the order of the alphabets is re-arranged to obtain the cipher-text.
        
        1- The message is written out in rows of a fixed length, and then read out again column by column, and the columns are chosen in some scrambled order.
        2- Width of the rows and the permutation of the columns are usually defined by a keyword.
        3- For example, the word HACK is of length 4 (so the rows are of length 4), and the permutation is defined by the alphabetical order of the letters in the keyword. In this case, the order would be “3 1 2 4”.
        4- Any spare spaces are filled with nulls or left blank or placed by a character (Example: _).
        5- Finally, the message is read off in columns, in the order specified by the keyword.

    Decryption
        1- To decipher it, the recipient has to work out the column lengths by dividing the message length by the key length.
        2- Then, write the message out in columns again, then re-order the columns by reforming the key word.
    """

    cipher = ""
    decrypted_cipher = ""

    # track key indices
    k_indx = 0

    message_indx = 0
    message_len = float(len(message))
    message_lst = list(message)
    # convert key into list and sort
    # alphabetically so we can access
    # each character by its alphabetical position.
    key_lst = sorted(list(key))

    # calculate column of the matrix
    col = len(key)

    # calculate maximum row of the matrix
    row = int(math.ceil(message_len / col))

    if mode == 'encrypt':
        # add the padding character '_' in empty
        # the empty cell of the matix
        fill_null = int((row * col) - message_len)
        message_lst.extend('_' * fill_null)

        # create Matrix and insert message and
        # padding characters row-wise
        matrix = [
            message_lst[i: i + col] for i in range(0, len(message_lst), col)
        ]

        # read matrix column-wise using key
        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])
            cipher += ''.join(
                [
                    row[curr_idx] for row in matrix
                ]
            )
            k_indx += 1

        return cipher
    elif mode == 'decrypt':
        # create an empty matrix to
        # store deciphered message
        dec_cipher = []
        for _ in range(row):
            dec_cipher += [[None] * col]

        # Arrange the matrix column wise according
        # to permutation order by adding into new matrix
        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])

            for j in range(row):
                dec_cipher[j][curr_idx] = message_lst[message_indx]
                message_indx += 1
            k_indx += 1

        # convert decrypted message matrix into a string
        try:
            decrypted_cipher = ''.join(sum(dec_cipher, []))
        except TypeError:
            raise TypeError("This program cannot handle repeating words.")

        null_count = decrypted_cipher.count('_')

        if null_count > 0:
            return decrypted_cipher[: -null_count]

        return decrypted_cipher

# if __name__ == '__main__':
#     mensaje = input('Mensaje a cifrar: ')

#     print(f'Mensaje cifrado: {caesar_cipher(mensaje, 3, "decrypt")}')







