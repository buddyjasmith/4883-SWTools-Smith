"""
Name: Buddy Smith
Course: Software Tools
Date: 3.16.2019
Description: The program is passed two values:
            :param[1]: path to image to find like image
            :param[2]: collection of images to compare to param[1]
Example:
    python3 match.py [image_path] [image_collection_path]
"""

import sys
import cv2
import numpy as np
from skimage.measure import compare_ssim as ssim
import os, os.path
from termcolor import colored

def mse(image_a, image_b):
    """
    Description: 2 images must have the same dimensions, if calling
                the function directly.
    :param image_a: target_image
    :param image_b: possible match
    :return: sum of the squared difference between the two images
    """

    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    return err


def compare_images(image_a, image_b):
    """
    :Description: if images are not same dimensions, will pass in exception
    :param image_a: target image
    :param image_b: possible image
    :return: returns the structual similarity index and mse value
    """
    # try except in event of size mismatch
    try:
        m = mse(image_a, image_b)
        s = ssim(image_a, image_b)
    except ValueError:
        # in event size is mismatched
        m = sys.maxsize
        s = -1
        pass
    return m, s


def main(image_path, collection_path):
    """
    :description: an image is passed in to find a the most
                  similiar image residing in the collection_path.
                  both images will be output to the user.
                  PRESS ANY KEY to exit.
    :param image_path: path of target image, image to find like of
    :param collection_path: path of folders for consideration
    :return: none
    """
    # Collect the parse image and convert to grayscale
    target = cv2.imread(image_path,1)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    # Extract file name from image_path
    extracted_file_name = os.path.basename(image_path)
    directory = [f for f in os.listdir(collection_path) if os.path.isfile(os.path.join(collection_path, f))]

    # Create default values for comparisons
    match_title, match_m, match_s = "", sys.float_info.max, -1

    for file in directory:
        if (str(file) != extracted_file_name ):
            # collect current image and grayscale it
            poss_im = cv2.imread(collection_path + str(file))
            poss_img_g = cv2.cvtColor(poss_im, cv2.COLOR_BGR2GRAY)
            # compare images' gray versions and set to closest if the current candidate is more similar
            m,s = compare_images(target, poss_img_g)
            if((s > match_s) and (m < match_m)):
                print(colored("Possible Matches: %s" % str(file),'red'))
                match_title,match_s,match_m = str(file), s, m

    print(colored("The closest image to %s is %s" % (extracted_file_name,match_title),'blue'))
    match_title = collection_path + match_title
    match_title = cv2.imread(match_title, 1)
    new_target = cv2.imread(image_path, 1)

    # Display both images for manual comparison
    cv2.imshow("Target", new_target)
    cv2.imshow("Match", match_title)
    # Press any key to exit!
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    """
    Checks if sys.argv length is 3 before beginning.
    """
    if(len(sys.argv)==3):
        main(sys.argv[1], sys.argv[2])
    else:
        print("Incorrect Number of Arguments Parsed.  Try Again!")

