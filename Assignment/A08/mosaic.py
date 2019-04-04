"""
Name: Buddy Smith
Assignment: A08
Description: The program takes a photo and creates a mosaic of it using files supplied by the user
Ouput: Files will be save in ./output/name_mosaic.ext
"""
import sys
import os
from PIL import Image, ImageDraw, ImageColor
from math import sqrt
import json


def begin_image_ops(img,dom,size):
    """
    :param img: contains image path of file to be made into mosaic
    :param dom: dominant.json file containing dominant colors
    :param size: size of the sub size image to pasted on to mosaic
    :return:none
    :Output: the mosaic is saved to the directory ./ouput/ + name + '_mosaic' + '.' + ext
    """
    #bg_color = (255,255,255)
    original = Image.open(img,'r')

    width, height = original.size

    original = original.convert('RGBA')
    pixel_values = original.load()
    canvas_ht = int(height) * int(size)
    canvas_width = int(width) * int(size)
    print(output_directory)
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    canvas = canvas.resize((canvas_width,canvas_ht), Image.ANTIALIAS)
    for y in range(height):
        for x in range(width):
            pixel = pixel_values[x,y]
            key = find_match(pixel,dom)
            emoji = input_directory + key
            emoji = Image.open(emoji)
            emoji = emoji.convert('RGBA')
            emoji = emoji.resize((int(sub_image_size),int(sub_image_size)),Image.ANTIALIAS)
            canvas.paste(emoji,(x *int(sub_image_size),y*int(sub_image_size)))
    canvas.save(output_directory)
    canvas.show()

def color_diff(c1,c2):
    """
    Stolen from Griffin
    Returns a percent distant from two rgb colors
    Params:
        c1 [tuple]: rgb color tuple
        c2 [tuple]: rgb color tuple
    Returns:
        percent [float]: value between 0 and 1
    """
    d = sqrt(pow((c2[0]-c1[0]),2)+pow((c2[1]-c1[1]),2)+pow((c2[2]-c1[2]),2))

    return d / sqrt(pow(255,2)+pow(255,2)+pow(255,2))

def find_match(pixel,dom):
    """
    Description: function returns the smallest difference between
                 the pixel and a emoji from dominants.json
    :param pixel: tuple (Red,Green,Blue)
    :param dom: json file containing dominant colors
    :return: returns a key to reference dominant.json emoji
    """
    # Values are always less than 1
    compare = 1.0
    ret_key = ""
    for key, value in dom.items():
        distance = color_diff(pixel,value)

        if(distance<compare):
            compare = distance
            ret_key = key
    return ret_key

def process_args(args):
    """
    Description: Stores contents of sys.argv in a dict
    :param args: sys.argv parameters
    :return: dictionary of args
    """
    kargs = {}
    for args in sys.argv[1:]:
        k, v = args.split('=')
        kargs[k] = v
    return kargs

def get_color_json():
    """
    Opens dominants.json file
    :return: contents of the json file in a dict
    """
    try:
        data = open('./dominants.json','r')
        dom = data.read()
        return json.loads(dom)
    except IOError:
        print("JSON data not found!")
        print("Refer to documentation")
        exit()


if __name__ == '__main__':
    """
    Description: Before running this program, dominants.py must be ran first.
                 Documentation can be found in the file how to run.
    Execution command:
     python3 mosaic.py input_file=commies.jpg input_folder=./emojis/ size=6 output_folder=./output/

    """
    # VARS default to initial value if only image is parsed at terminal
    original_image = ""
    input_directory = "./emojis/"
    sub_image_size = 10
    output_directory = "./output/"

    # Collect dominant values of emojis, processed before hand
    dominant = get_color_json()

    # First conditional is taken if more than the image is parsed, else default values are used for execution
    if(len(sys.argv) > 2):
        kargs = process_args(sys.argv)
        original_image=kargs['input_file']
        input_directory = kargs['input_folder']
        sub_image_size = kargs['size']
        output_directory = kargs['output_folder']
        name,ext = kargs['input_file'].split('.')
        output_directory = output_directory + name + '_mosaic.' + ext
    else:
        print(sys.argv[1])
        name, ext = sys.argv[1].split('.')
        new_name = name + '_mosaic' + '.' + ext
        output_directory += new_name
        original_image = os.path.basename(sys.argv[1])
        print(output_directory)

    begin_image_ops(original_image,dominant,sub_image_size)