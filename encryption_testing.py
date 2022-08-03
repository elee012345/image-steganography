
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
print(binary)



# Decode:
# take password and ord() it
# convert ciphertext from binary to unicode
# xor the unicode

password = "password"
password_list = list(password)
for i in range(len(password_list)):
    password_list[i] = ord(password_list[i])

unxored_list = []
xored_list = []
for i in range(len(plaintext_list)):
    if i == len(password_list):
        password_list += password_list
    unxored_list.append(plaintext_list[i] ^ password_list[i])



#     
#     testvar = "whee this is a test"
#     testvar2 = testvar.encode('utf-8')
#     print(testvar2)
#     testvar3 = testvar2.hex()
#     print(testvar3)
#     testvar4 = bytes.fromhex(testvar3)
#     print(testvar4)
#     
#     
#     testvar = "whee this is a test"
#     print(testvar)
#     testlist = list(testvar)
#     print(testlist)
#     for i in range(len(testlist)):
#         testlist[i] = ord(testlist[i])
#     testvar2 = "".join(testlist)
#     print(testvar2)
#     testvar3 = testvar2.hex()
#     print(testvar3)
#     testvar4 = bytes.fromhex(testvar3)
#     print(testvar4)
#     
#     