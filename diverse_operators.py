from PIL import Image
from spatial_filtering import *

def extract_region(image: Image, color: tuple, background_color: int = 255) -> Image:
    result = Image.new(image.mode, image.size)
    original_image_matrix = image_to_matrix(image)
    for line in range(image.size[0]):
        for column in range(image.size[1]):
            if original_image_matrix[line][column] == color:
                result.putpixel((line, column), color)
            else:
                if image.mode == 'L':
                    result.putpixel((line, column), background_color)
                elif image.mode == 'RGB':
                    result.putpixel((line, column), (background_color, background_color, background_color))
                elif image.mode == 'RGBA':
                    result.putpixel((line, column), (background_color, background_color, background_color, background_color))
    return result


def color_region(image: Image, color: tuple, region_color: tuple) -> Image:
    image = image.copy()
    if len(color) == 4 and len(region_color) == 4:
        result = Image.new('RGBA', image.size)
        image = image.convert('RGBA')
    if len(color) == 3 and len(region_color) == 3:
        result = Image.new('RGB', image.size)
        image = image.convert('RGB')
    if len(color) == 1 and len(region_color) == 1:
        result = Image.new('L', image.size)
        image = image.convert('L')
    original_image_matrix = image_to_matrix(image)
    for line in range(image.size[0]):
        for column in range(image.size[1]):
            if original_image_matrix[line][column] == region_color:
                result.putpixel((line, column), color)
            else:
                result.putpixel((line, column), original_image_matrix[line][column])
    return result


def complement_border(image: Image) -> Image:
    image = image.copy()
    original_image_matrix = image_to_matrix(image)
    for line in range(image.size[0]):
        for column in range(image.size[1]):
            if line == 0 or line == image.size[0] - 1 or column == 0 or column == image.size[1] - 1:
                if image.mode == 'L':
                    image.putpixel((line, column), 255 - original_image_matrix[line][column])
            else:
                if image.mode == 'L':
                    image.putpixel((line, column), 0)
    return image
    
