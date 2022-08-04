from PIL import Image

def encrypt_text(plaintext, password):
        
    # convert plaintext into list
    plaintext_list = list(plaintext)
    # ord the plaintext to make it unicode/ascii
    for i in range(len(plaintext_list)):
        plaintext_list[i] = ord(plaintext_list[i])

    # ord the password (make it into unicode/ascii)
    password_list = list(password)
    for i in range(len(password_list)):
        password_list[i] = ord(password_list[i])

    # xor this all
    # aka it 'encrypts' it
    # for more detail just look up what xor does lol
    xored_list = []
    for i in range(len(plaintext_list)):
        # extends password length if its not long enough
        if i == len(password_list):
            password_list += password_list
        xored_list.append(plaintext_list[i] ^ password_list[i])

    # none of these should be over 128 (bits)
    #print(xored_list)

    # ascii takes two bytes of data so we assume that you have not inputted any weird stuff as your password
    # or as your plaintext
    binary = []
    for i in range(len(xored_list)):
        # take an int from the xored_list and make it into a string that has a format of 8 bits
        binary.append(f'{xored_list[i]:08b}')

    # i can do whatever i want with this now
    #print(binary)

    return binary

# takes binary as the binary list with string elements that hold
# a bytes in string form
def decrypt_text(binary, password):
    password_list = list(password)
    for i in range(len(password_list)):
        password_list[i] = ord(password_list[i])

    xored_list = []
    for i in range(len(binary)):
        # you can actually convert a string directly from binary to a
        # decimal int with python's built in int() function
        xored_list.append(int(binary[i], 2))

    #print(xored_list)

    # unnxoring the message with your password
    unxored_list = []
    for i in range(len(xored_list)):
        if i == len(password_list):
            password_list += password_list
        unxored_list.append(xored_list[i] ^ password_list[i])

    #print(unxored_list)

    plaintext_list = []
    # converting the unxored list into ascii aka human readable format
    for i in range(len(unxored_list)):
        plaintext_list.append(chr(unxored_list[i]))

    # making this back into a string instead of a list
    plaintext = "".join(plaintext_list)
    #print(plaintext)

    return plaintext


def encrypt_image():
    #image = input("Enter the name of the image you wish to modify")

    # already have an image in mind
    image = "test image.png"

    # i don't want to make a new variable shush
    image = Image.open(image, 'r')
    

    #plaintext = input("What message do you wish to embed?")
    #password = input("What password do you want to use?")
    #new_image_name = input("What do you want the encrypted image to be called?")

    # for the sake of testing i am hard coding the password and plaintext for now
    plaintext = "jklasdfjklasdf this is text hi yeet idk josadjfkl sadf words are awesome"
    password = "this is a very very strong password yay"
    new_image_name = "newimg.png"

    binary = encrypt_text(plaintext, password)

    print(binary)

    # now we have to put our encrypted text into this new image
    new_image = image.copy()

    image_width = new_image.size[0]
    image_height = new_image.size[1]

    # length of the binary list (all the characters) times 8=9
    # multiply by 8 becausue 8 bits per character + 1 because of the 
    # lsb that tells us whether or not to keep reading
    # need one pixel for three bits (it has r, g, and b values)
    # so then we divide by 3
    # we will always divide evenly so we floor divide to get a nice clean int
    needed_pixels = len(binary) * 9 // 3
    if image_width * image_height < needed_pixels:
        # this will probably not happen unless you have a tiny image 
        # or really big message
        print("your image is too small for your message")
        # pretty sure one of these ends the program but i haven't tested it
        exit()
        quit()
    
    # is r, g, b, and a for alpha transparency
    #print(list(new_image.getdata()))

    

    x, y = 0, 0
    # is r, g, b, and a for alpha transparency
    #print(new_image.getpixel((x, y)))

    # looping through each byte
    for i in range(len(binary)):

        # to go through all 8 bits needed
        bit_counter = 0

        # binary value of the r/g/b part of the pixel
        r = new_image.getpixel((x, y))[0]
        g = new_image.getpixel((x, y))[1]
        b = new_image.getpixel((x, y))[2]
        a = new_image.getpixel((x, y))[3] # we never change this
        values = [r, g, b, a]
        #print("values are", values)
        while bit_counter < 7:
            for k in range(3):
                #print("on pixel", x, ",", y, "and bit", bit_counter)
                # checking lsb against binary bit
                # if they differ then we have to modify that pixel value
                # i is the byte, bit_counter is the bit, and k is the r/g/b
                #print("bit to match is", binary[i][bit_counter])
                #print("value is", values[k])
                if values[k] % 2 != int( binary[i][bit_counter] ):
                    # if its greater than 0 and doesn't match the lsb then we can 
                    # substract 1 from its value
                    if values[k] > 0:
                        values[k] -= 1
                    # if its 0 obviously we can't subtract so we add instead
                    else:
                        values[k] += 1
                # increment the bit that we're adding to the image
                bit_counter += 1
                # stop when we have written all 8 bits
                if bit_counter == 8:

                    # this tells us whether or not to keep reading
                    # 1 is to keep reading, 0 is to stop
                    if i == len(binary) - 1:
                        keep_reading = 0
                    else:
                        keep_reading = 1
                    
                    if values[2] % 2 != keep_reading:
                        # if its greater than 0 and doesn't match the lsb then we can 
                        # substract 1 from its value
                        if values[2] > 0:
                            values[2] -= 1
                        # if its 0 we can't subtract, so we add instead
                        else:
                            values[2] += 1
                    break
            #print("final values are", values)
            new_image.putpixel((x, y), tuple(values))
            
            # increment the pixel we're on
            # move down a row if we're at the end of a column
            if image_width - 1 == x:
                y += 1
                x = 0
            else:
                x += 1


    # save the image with the image name and extension
    new_image.save(new_image_name, str(new_image_name.split(".")[1].upper()))




def decrypt_image():

    #image = input("What is the name of the image you want to decrypt?")
    #password = input("What is your password?")

    image_name = "newimg.png"
    password = "this is a very very strong password yay"

    image = Image.open(image_name, 'r')

    print( list(image.getdata()) )
    #print( list(image.getdata())[0] )
    #print( list(image.getdata())[1] )
    #print( list(image.getdata())[2] )

    byte_list = []
    x, y = 0, 0
    rgb_counter = 0
    image_width = image.size[0]
    while True:
        byte = ""
        for i in range(8):
            # get the current pixel's r/g/b and then find the lsb, append it to the byte string
            byte += str( image.getpixel((x, y))[rgb_counter] % 2 )


            rgb_counter += 1
            # reset rgb counter if needed
            # this is modular arithmetic
            rgb_counter = rgb_counter % 3

            # increment the pixel we're on
            # move down a row if we're at the end of a column
            # we can only do this if we're done with our current pixel though
            if rgb_counter == 2:
                if image_width - 1 == x:
                    y += 1
                    x = 0
                else:
                    x += 1
        
        byte_list.append(byte)

        if image.getpixel((x, y))[rgb_counter] % 2 == 0:
            break
    
    print(decrypt_text(byte_list, password))

        

encrypt_image()

decrypt_image()