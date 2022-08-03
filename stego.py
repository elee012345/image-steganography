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
    print(new_image.getpixel((x, y)))

    # looping through each byte
    for i in range(len(binary)):

        # we are going to modify the lsb of the r, g, and b values
        # not going to modify transparency
        rgb_counter = 0

        # looping through each bit in the byte
        for j in range(8):
            # binary value of the r/g/b part of the pixel
            bin_value = new_image.getpixel((x, y))[rgb_counter]

            # checking lsb against binary bit
            # if they differ then we have to modify that pixel value
            if bin_value % 2 != binary[i][j]:
                # if its greater than 0 and doesn't match the lsb then we can 
                # substract 1 from its value
                if bin_value == 255 or bin_value != 0:
                    new_image.putpixel((x, y), bin_value - 1)
                # if its 0 we can't subtract, so we add instead
                elif bin_value == 0:
                    new_image.putpixel((x, y), bin_value + 1)

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

        # after we have placed 8 bits, we now need to add in the 9th part in the 
        # last part of the 3rd pixel
      
        bin_value = new_image.getpixel((x, y))[rgb_counter]

        
        # this tells us whether or not to keep reading
        # 1 is to keep reading, 0 is to stop
        if i == len(binary) - 1:
            keep_reading = 0
        else:
            keep_reading = 1
        
        if bin_value % 2 != keep_reading:
            # if its greater than 0 and doesn't match the lsb then we can 
            # substract 1 from its value
            if bin_value == 255 or bin_value != 0:
                new_image.putpixel((x, y), bin_value - 1)
            # if its 0 we can't subtract, so we add instead
            elif bin_value == 0:
                new_image.putpixel((x, y), bin_value + 1)
        
        

    # save the image with the image name and extension
    new_image.save(new_image_name, str(new_image_name.split(".")[1].upper()))




def decrypt_image():

    #image = input("What is the name of the image you want to decrypt?")
    #password = input("What is your password?")

    image = "newimg.png"
    password = "this is a very very strong password yay"

    
    
        

encrypt_image()
