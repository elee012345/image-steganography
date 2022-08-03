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

    # length of the binary list (all the characters) times 8
    # multiply by 8 becausue 8 bits per character
    # need one pixel for each bit
    needed_pixels = len(binary) * 8
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

    # we are going to modify the lsb of the r, g, and b values
    # not going to modify transparency
    rgb_counter = 0

    # looping through each byte
    for i in range(len(binary)):
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
            
            # reset rgb counter if needed
            # this is modular arithmetic
            rgb_counter = rgb_counter % 3

            # increment the pixel we're on
            # move down a row if we're at the end of a column
            if image_width - 1 == x:
                y += 1
                x = 0
            else:
                x += 1

    # save the image with the image name and extension
    new_image.save(new_image_name, str(new_image_name.split(".")[1].upper()))

        

    
        

encrypt_image()
