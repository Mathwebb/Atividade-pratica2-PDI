import string
from PIL import Image


def image_to_matrix(image: Image) -> list:
    image_matrix = []
    for line in range(image.height):
        image_matrix.append([image.getpixel((0, line))])
        for column in range(1, image.width):
            image_matrix[line].append(image.getpixel((line, column)))
    return image_matrix


def matrix_to_image(matrix: list, image: Image) -> Image:
    image = image.copy()
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


def create_empty_mask(m: int, n: int, default_value: int = 1) -> list:
    mask = []
    for line in range(m):
        mask.append([])
        for column in range(n):
            mask[line].append(default_value)
    return mask


def arithmetic_mean_filter(image: Image, m: int, n: int, modify: bool = False) -> Image:
    original_image_matrix = image_to_matrix(image)
    blurred_image_matrix = create_empty_matrix(image.height, image.width)
    m1 = (m/2).__floor__()
    n1 = (n/2).__floor__()
    for line in range(image.height):
        for column in range(image.width):
            central_pixel = 0
            for mask_line in range(-m1, m1+1):
                for mask_column in range(-n1, n1+1):
                    try:
                        central_pixel += original_image_matrix[line+mask_line][column+mask_column]
                    except IndexError:
                        pass
            if modify:
                image.putpixel((line, column), int(central_pixel/(m*n)))
            blurred_image_matrix[line][column] = int(central_pixel/(m*n))
    return matrix_to_image(blurred_image_matrix, image)


def apply_linear_filter(image: Image, mask: list) -> list:
    original_image_matrix = image_to_matrix(image)
    filtered_image_matrix = create_empty_matrix(image.height, image.width)
    m1 = (len(mask)/2).__floor__()
    n1 = (len(mask[0])/2).__floor__()
    for line in range(image.height):
        for column in range(image.width):
            central_pixel = 0
            for mask_line in range(-m1, m1+1):
                for mask_column in range(-n1, n1+1):
                    try:
                        central_pixel += original_image_matrix[line+mask_line][column+mask_column] *\
                                         mask[mask_line+m1][mask_column+n1]
                    except IndexError:
                        pass
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
                        laplacian_image.putpixel((line, column), 127 - int(pixel / 2))
                    else:
                        laplacian_image.putpixel((line, column), 127 - int((pixel - 1) / 2))
                else:
                    if pixel % 2 == 0:
                        laplacian_image.putpixel((line, column), int(pixel / 2) + 127)
                    else:
                        laplacian_image.putpixel((line, column), int((pixel - 1) / 2) + 127)
    else:
        laplacian_image = matrix_to_image(laplacian_image_matrix, image)
    for line in range(image.height):
        for column in range(image.width):
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

    for line in range(image.height):
        for column in range(image.width):
            image.putpixel((line, column), original_image_matrix[line][column] + 
            (original_image_matrix[line][column] - blurred_image_matrix[line][column]))
    return image


def high_boost(image: Image, m: int, n: int, k: float, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    original_image_matrix = image_to_matrix(image)
    blurred_image = arithmetic_mean_filter(image, n, m)
    blurred_image_matrix = image_to_matrix(blurred_image)

    for line in range(image.height):
        for column in range(image.width):
            image.putpixel((line, column), original_image_matrix[line][column] + int(k * 
            (original_image_matrix[line][column] - blurred_image_matrix[line][column])))
    return image


def prewitt_border_detection(image: Image, horizontal: bool = True) -> Image:
    if horizontal:
        prewitt_mask = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    else:
        prewitt_mask = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    prewitt_image = apply_linear_filter(image, prewitt_mask)
    return matrix_to_image(prewitt_image, image)



def sobel_border_detection(image: Image, horizontal: bool = True):
    if horizontal:
        sobel_mask = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    else:
        sobel_mask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_image = apply_linear_filter(image, sobel_mask)
    return matrix_to_image(sobel_image, image)


if __name__ == '__main__':
    with Image.open('imgs/lena_gray.bmp', 'r') as lena_gray:
        result, laplacian_image = laplacian_filter(lena_gray, -8, adjusted_laplacian=False)
        # laplacian_image.show()
        laplacian_image.save('results/lena_laplacian_result.bmp')
        # result.show()
        result.save('results/lena_laplacian.bmp')

        result = high_boost(lena_gray, 3, 3, 10)
        result.save('results/lena_gray_high_boost.bmp')
        # result.show()

        result = unsharp_masking(lena_gray, 3, 5)
        result.save('results/lena_gray_unsharp.bmp')
        # result.show()

        # result = prewitt_border_detection(lena_gray, horizontal=True)
        # result.save('results/lena_prewitt_horizontal.bmp')
        # result = prewitt_border_detection(lena_gray, horizontal=False)
        # result.save('results/lena_prewitt_vertical.bmp')
        # result.show()

        # result = sobel_border_detection(lena_gray, horizontal=True)
        # result.save('results/lena_sobel_horizontal.bmp')
        # result = sobel_border_detection(lena_gray, horizontal=False)
        # result.save('results/lena_sobel_vertical.bmp')
        # result.show()
