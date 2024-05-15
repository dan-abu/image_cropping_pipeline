import sys
from PIL import Image
import numpy as np

# 1.) Load image in the script
# 2.) Randomly crop the image ensuring the samples don't overlap
# 3.) Crop the image and show the user the samples
# 4.) Allow the user to resize the cropped images and show the new images

#1.) Load image in the script
def load_image():
    print('This programme will allow you to cut three random samples from an image.\nThe image in question will appear in another application shortly.')
    with Image.open('surgical_robot.jpeg') as im:
        im.show()
        print(f'The image\'s details are as follows.\nImage format: {im.format}.\nImage size: {im.size}.')

# 2.) Generate coordinates to randomly crop the image ensuring the samples don't overlap
# Gets the second minimum coords
def min_coord(a):
    if a == 0:
        numb = 1
    else:
        numb = a + 1
    return numb

# Calculating the area of the first cropped shape
def calc_area(polygon):
    if polygon[0] > polygon [2]:
        width = polygon[0] - polygon[2]
    else:
        width = polygon[2] - polygon[0]
    
    if polygon[1] > polygon[3]:
        length = polygon[1] - polygon[3]
    else:
        length = polygon[3] - polygon[1]
    
    area = width * length
    return area

# Getting the first shape that will be cropped
def first_shape():
    space = 361000
    while space > 360000:
        shape = np.random.randint([0,0], [1271,847])
        shape2 = np.random.randint([min_coord(shape[0]), min_coord(shape[1])], [1272, 848])
        shape3 = np.append(shape, shape2)
        space = int(calc_area(shape3))
    
    shape3 = np.array([shape3])
    return shape3

# Getting first min x-coord in other shapes to be cropped
def other_x_min_coord(polygons):
    missable_coords = []
    for polygon in polygons:
        missable = range(polygon[0], polygon[2])
        for num in missable:
            missable_coords.append(num)
    missable_coords.sort()
    missable_coords = set(missable_coords)
    a = range(1271)
    others = []
    for num in a:
        if num in missable_coords:
            pass
        else:
            others.append(num)
    return others

# Getting first min y-coord in other shapes to be cropped
def other_y_min_coord(polygons):
    missable_coords = []
    for polygon in polygons:
        missable = range(polygon[0], polygon[2])
        for num in missable:
            missable_coords.append(num)
    missable_coords.sort()
    missable_coords = set(missable_coords)
    a = range(847)
    others = []
    for num in a:
        if num in missable_coords:
            pass
        else:
            others.append(num)
    return others

# Getting first max x-coord in other shapes to be cropped
def other_x_max_coord(polygons, x_coord):
    x_coords = []

    for polygon in polygons:
        x_coords.append(polygon[0])
        x_coords.append(polygon[2])
    
    x_coords.append(x_coord)
    x_coords.sort()

    if x_coord == x_coords[-1]:
        x_max_coord = x_coord
    else:
        x_max_coord = x_coords[x_coords.index(x_coord) + 1]
    
    width = np.random.randint(x_coord+1, x_max_coord+2)

    return width

# Getting first max y-coord in other shapes to be cropped
def other_y_max_coord(polygons, y_coord):
    y_coords = []

    for polygon in polygons:
        y_coords.append(polygon[0])
        y_coords.append(polygon[2])
    
    y_coords.append(y_coord)
    y_coords.sort()

    if y_coord == y_coords[-1]:
        y_max_coord = y_coord
    else:
        y_max_coord = y_coords[y_coords.index(y_coord) + 1]
    
    height = np.random.randint(y_coord+1, y_max_coord+2)

    return height

# Getting other shapes that will be cropped
def other_shapes():
    shapes = first_shape()

    space2 = 361000
    width = -2
    height = -3
    while space2 > 360000:
        left = np.random.choice(other_x_min_coord(shapes))
        top = np.random.choice(other_y_min_coord(shapes))
        while width <= left:
            width = other_x_max_coord(shapes, left)
        while height <= top:
            height = other_y_max_coord(shapes, top)
        new_shape = np.array([left,top,width,height])
        space2 = int(calc_area(new_shape))
    
    new_shape = np.array([new_shape])
    return new_shape

# 3.) Crop the image and show the user the samples
# 4.) Allow the user to resize the cropped images and show the new images
def resize_request():
    decision = input('Do you want to resize the cropped image? (Y/N): ')
    if decision == 'Y':
        goal = 2
        retries = 3

        for i in range(retries):
            try:
                new_size = input('Maximum size is 2000 x 1500. Kindly enter the size you want the cropped image in the format 0,0: ')
                sizes = []
                new_size = new_size.split(',')
                dig_check = ''.join(new_size)
                for num in new_size:
                    sizes.append(int(num))
                sizes = tuple(sizes)
                if len(new_size) != goal:
                    raise IndexError('Kindly enter two numbers (first up to 2000 and second up to 1500) separated by commas and two numbers separated by commas only.')
                if dig_check.isdigit() is False or not dig_check:
                    raise ValueError('Kindly enter four numbers separated by commas and four numbers separated by commas only.')
                else:
                    break
            except IndexError as e:
                print(e)
                if i < retries - 1:
                    continue
                else:
                    print('Restart this programme and follow the instructions more carefully when you re-run it.')
                    sys.exit()
            except ValueError as e2:
                print(e2)
                if i < retries - 1:
                    continue
                else:
                    print('Restart this programme and follow the instructions more carefully when you re-run it.')
                    sys.exit()
        
        return sizes
    else:
        return 'Cropped image will not be resized'

def crop_image(polygons):
    with Image.open('surgical_robot.jpeg') as im:
        for polygon in polygons:
            box = tuple(polygon)
            sample = im.crop(box)
            change = resize_request()
            print(change)
            if change is tuple:
                new_sample = sample.resize(change)
                new_sample.show()
            else:
                sample.show()
                continue

if __name__ == "__main__":
    #1.) Load image in the script
    load_image()

    # 2.) Generate coordinates to randomly crop the image ensuring the samples don't overlap
    first_shape()
    shapes = np.concatenate((first_shape(), other_shapes()))
    shapes = np.concatenate((shapes, other_shapes()))

    # 3.) Crop the image and show the user the samples
    # 4.) Allow the user to resize the cropped images and show the new images
    crop_image(shapes)
    print('All images have been displayed.')