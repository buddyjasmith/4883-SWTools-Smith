'''
Buddy Smith
Date: 06/03/2019
Assignment: A04
Desc: The program takes a photo supplied by the user, must be .png type,
      and converts it to an 'ascii-image'. The new photo is saved as
      filename + _asc_art.png. The program must be supplied with 5 arguments,
      python3 image_ascii.py pyramid.png ../a04/output_image/pyramid_ascii.png /usr/share/fonts/alien_mushrooms/alm_____.ttf 4

'''

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_char(color):
    '''
    get_char()-1 parameter
    :param color: a pixel containing r, g, b, and a values
    :return new_char:
    :description: given a list of characters, the character to be returned
                  is calculated by finding the average of r,g,b. This value is
                  divided by 25 to return a char to the gray value division.
    '''

    char = [',', '.', ':', '¿', 'y', '?','a', 'd', '-', '9', '%' ]
    r,g,b,a= color
    new_char =char[int((r + g + b)/3) // 25]
    return new_char

def img_to_ascii(file, out_file, font_path, font_size ):
    '''
    img_to_ascii()-2 parameters
    :param file: the name of the .png file to convert to ascii text
    :param font_size: the size of the font to be output to the new .png image
    :return: none
    '''

    # Check font path exists
    if(os.path.exists(font_path)):
        print("Font Path Successfully found!")
    else:
        print("Incorrect font path given.")
        return

    # check file path exists, else return
    if(os.path.isfile(out_file) ):
        print("Output path successfully found.")
    else:
        print("Incorrect output file path given.  Does not exist.")
        print("Exiting. Try Again.")
        return

    # load font
    font_size = int(font_size)
    fnt = ImageFont.truetype(font_path, font_size)

    # Open image, convert, and load. Collect width and height..
    try:
        img = Image.open(file).convert('RGBA')
    except IOError:
        print("Check for correct file name!")
        return
    width, height = img.size
    img = img.load()

    # create new image same size
    new_img = Image.new('RGB', (width, height), (255,255,255,255))
    canvas = ImageDraw.Draw(new_img)

    print("Beginning Conversion Process")
    for col in range(height):
        if ((col)% (font_size) == 0):
            for row in range(width):
                if ((row) % (font_size) == 0):
                    pixel = img[row, col]
                    r,g,b,a = pixel
                    new_char = get_char(pixel)
                    canvas.text((row, col), new_char, font=fnt, fill=(r,g,b,a))
    new_img.show()
    new_img.save(out_file,'PNG')



if __name__=='__main__':
    '''
    If the correct number of arguments is given, 5, img_to_ascii is called with
    parameters of the file to be converted, the font size for output, and the path
    of the font to be used. 
    Such as:
        python3 image_ascii.py pyramid.png ../a04/output_image/pyramid_ascii.png /usr/share/fonts/alien_mushrooms/alm_____.ttf 4
    Note: Anything above a font size 4 looks terrible.  
    Input file (image to process)
    Output file name (path and name of where to save it)
    True type font (a path and name to a true type font)
    Font size (integer of what font size they want)

    '''
    if(len(sys.argv) == 5):
        img_to_ascii(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])
    else:
        print("Too few Arguments passed")
