string = "ice cream is deleiciouis"
string += str(1)
print(string)

# Encode:
# take plaintext and ord() it
# convert password using ord() into unicode
# both of the above should now be integers
# now do plaintext ^ password using the inbuilt ^ xor operator
# convert them both into binary



plaintext = "wow this is plaintext"
# convert plaintext into list
plaintext_list = list(plaintext)
# ord the plaintext to make it unicode
for i in range(len(plaintext_list)):
    plaintext_list[i] = ord(plaintext_list[i])

# ord the password
password = "password"
password_list = list(password)
for i in range(len(password_list)):
    password_list[i] = ord(password_list[i])

# xors this all
# aka it 'encrypts' it
xored_list = []
for i in range(len(plaintext_list)):
    if i == len(password_list):
        password_list += password_list
    xored_list.append(plaintext_list[i] ^ password_list[i])

# none of these should be over 128 (bits)
print(xored_list)

# ascii takes two bytes of data so we assume that you have not inputted any weird stuff as your password
# or as your plaintext
binary = []
for i in range(len(xored_list)):
    # take an int from the xored_list and make it into a string that has a format of 8 bits
    binary.append(f'{xored_list[i]:08b}')

# i can do whatever i want with this now
print(binary)

"""********************"""

# Decode:
# take password and ord() it
# convert ciphertext from binary to unicode
# xor the unicode

password = "password"
password_list = list(password)
for i in range(len(password_list)):
    password_list[i] = ord(password_list[i])

xored_list = []
for i in range(len(binary)):
    # you can actually convert a string directly from binary to a
    # decimal int with python's built in int() function
    xored_list.append(int(binary[i], 2))

print(xored_list)

# unnxoring the message with your password
unxored_list = []
for i in range(len(xored_list)):
    if i == len(password_list):
        password_list += password_list
    unxored_list.append(xored_list[i] ^ password_list[i])

print(unxored_list)

plaintext_list = []
# converting the unxored list into ascii aka human readable format
for i in range(len(unxored_list)):
    plaintext_list.append(chr(unxored_list[i]))

# making this back into a string instead of a list
plaintext = "".join(plaintext_list)
print(plaintext)