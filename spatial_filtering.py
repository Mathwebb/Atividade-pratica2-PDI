from PIL import Image
from math import ceil, floor


def image_to_matrix(image: Image) -> list:
    image_matrix = []
    for line in range(image.width):
        image_matrix.append([image.getpixel((line, 0))])
        for column in range(1, image.height):
            image_matrix[line].append(image.getpixel((line, column)))
    return image_matrix


def matrix_to_image(matrix: list) -> Image:
    image = Image.new('L', (len(matrix), len(matrix[0])))
    for line in range(len(matrix)):
        for column in range(len(matrix[line])):
            image.putpixel((line, column), matrix[line][column])
    return image


def create_empty_matrix(m, n) -> list:
    image_matrix = []
    for line in range(m):
        image_matrix.append([])
        for column in range(n):
            image_matrix[line].append(0)
    return image_matrix


def arithmetic_mean_filter(image: Image, m: int, n: int, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    original_image_matrix = image.load()
    m1 = floor(m/2)
    n1 = floor(n/2)
    for line in range(image.width):
        for column in range(image.height):
            central_pixel = 0
            for mask_line in range(-m1, m1+1):
                for mask_column in range(-n1, n1+1):
                    try:
                        central_pixel += original_image_matrix[line+mask_line, column+mask_column]
                    except IndexError:
                        pass
            image.putpixel((line, column), central_pixel//(m*n))
    return image

def weighted_arithmetic_mean_filter(image: Image, mask: list, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    original_image_matrix = image_to_matrix(image)
    m1 = floor(len(mask)/2)
    n1 = floor(len(mask[0])/2)
    sum_mask = 0
    for line in range(len(mask)):
        for column in range(len(mask[line])):
            sum_mask += mask[line][column]
    for line in range(image.width):
        for column in range(image.height):
            central_pixel = 0
            for mask_line in range(-m1, m1+1):
                for mask_column in range(-n1, n1+1):
                    try:
                        central_pixel += original_image_matrix[line+mask_line][column+mask_column] * mask[mask_line+m1][mask_column+n1]
                    except IndexError:
                        pass
            image.putpixel((line, column), central_pixel//sum_mask)
    return image


def median_filter(image: Image, m: int, n: int, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    original_image_matrix = image_to_matrix(image)
    m1 = floor(m/2)
    n1 = floor(n/2)
    for line in range(image.width):
        for column in range(image.height):
            image_pixels = []
            for mask_line in range(-m1, m1+1):
                for mask_column in range(-n1, n1+1):
                    try:
                        image_pixels.append(original_image_matrix[line+mask_line][column+mask_column])
                    except IndexError:
                        pass
            image_pixels.sort()
            image.putpixel((line, column), image_pixels[len(image_pixels)//2])
    return image
    

def apply_linear_filter(image: Image, mask: list) -> list:
    original_image_matrix = image_to_matrix(image)
    filtered_image_matrix = create_empty_matrix(image.width, image.height)
    n1 = floor(len(mask)/2)
    m1 = floor(len(mask[0])/2)
    for line in range(image.width):
        for column in range(image.height):
            central_pixel = 0
            for mask_line in range(-m1, m1+1):
                for mask_column in range(-n1, n1+1):
                    try:
                        central_pixel += original_image_matrix[line+mask_line][column+mask_column] *\
                                         mask[mask_column+n1][mask_line+m1]
                    except IndexError:
                        pass
            if central_pixel > 255:
                central_pixel = 255
            if central_pixel < -255:
                central_pixel = -255
            filtered_image_matrix[line][column] = central_pixel
    return filtered_image_matrix


def laplacian_filter(image: Image, center_value: int = -8, modify: bool = False, adjusted_laplacian: bool = False) -> Image:
    if not modify:
        image = image.copy()
    if center_value == -8:
        laplacian_mask = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
    elif center_value == 8:
        laplacian_mask = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    elif center_value == -4:
        laplacian_mask = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
    elif center_value == 4:
        laplacian_mask = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
    else:
        return None

    laplacian_image = image.copy()
    laplacian_image_matrix = apply_linear_filter(image, laplacian_mask)
    if adjusted_laplacian:
        for line in range(len(laplacian_image_matrix)):
            for column in range(len(laplacian_image_matrix[line])):
                pixel = laplacian_image_matrix[line][column]
                if pixel == 0:
                    laplacian_image.putpixel((line, column), 127)
                elif pixel < 0:
                    pixel *= -1
                    if pixel % 2 == 0:
                        laplacian_image.putpixel((line, column), 127 - pixel // 2)
                    else:
                        laplacian_image.putpixel((line, column), 127 - (pixel - 1) // 2)
                else:
                    if pixel % 2 == 0:
                        laplacian_image.putpixel((line, column), pixel // 2 + 127)
                    else:
                        laplacian_image.putpixel((line, column), (pixel - 1) // 2 + 127)
    else:
        laplacian_image = matrix_to_image(laplacian_image_matrix)
    for line in range(image.width):
        for column in range(image.height):
            if center_value < 0:
                image.putpixel((line, column), image.getpixel((line, column)) - laplacian_image_matrix[line][column])
            else:
                image.putpixel((line, column), image.getpixel((line, column)) + laplacian_image_matrix[line][column])

    return image, laplacian_image


def unsharp_masking(image: Image, n: int, m: int, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    original_image_matrix = image_to_matrix(image)
    blurred_image = arithmetic_mean_filter(image, n, m)
    blurred_image_matrix = image_to_matrix(blurred_image)

    for line in range(image.width):
        for column in range(image.height):
            image.putpixel((line, column), original_image_matrix[line][column] + 
            (original_image_matrix[line][column] - blurred_image_matrix[line][column]))
    return image


def high_boost(image: Image, m: int, n: int, k: float, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    original_image_matrix = image_to_matrix(image)
    blurred_image = arithmetic_mean_filter(image, n, m)
    blurred_image_matrix = image_to_matrix(blurred_image)

    for line in range(image.width):
        for column in range(image.height):
            image.putpixel((line, column), original_image_matrix[line][column] + int(k * 
            (original_image_matrix[line][column] - blurred_image_matrix[line][column])))
    return image


def prewitt_border_detection(image: Image, horizontal: bool = True) -> Image:
    if horizontal:
        prewitt_mask = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    else:
        prewitt_mask = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    prewitt_image = apply_linear_filter(image, prewitt_mask)
    return matrix_to_image(prewitt_image)



def sobel_border_detection(image: Image, horizontal: bool = True):
    if horizontal:
        sobel_mask = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    else:
        sobel_mask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_image = apply_linear_filter(image, sobel_mask)
    return matrix_to_image(sobel_image)
