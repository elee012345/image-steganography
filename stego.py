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

    # for the sake of testing i am hard coding the password and plaintext for now
    plaintext = "jklasdfjklasdf this is text hi yeet idk josadjfkl sadf words are awesome"
    password = "this is a very very strong password yay"

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
    print(list(new_image.getdata()))

    x, y = 0, 0
    for i in range(needed_pixels):
        # increment the pixel we're on
        # move down a row if we're at the end of a column
        if image_width - 1 == x:
            y += 1
            x = 0
        else:
            x += 1

    
        

encrypt_image()
