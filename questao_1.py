import string
from PIL import Image


def image_to_matrix(image: Image) -> list:
    image_matrix = []
    for i in range(image.height):
        image_matrix.append([image.getpixel((0, i))])
        for j in range(1, image.width):
            image_matrix[i].append(image.getpixel((j, i)))
    return image_matrix


def matrix_to_image(matrix: list, image: Image) -> Image:
    image = image.copy()
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            image.putpixel((x, y), matrix[x][y])
    return image


def create_empty_matrix(n, m) -> list:
    image_matrix = []
    for i in range(m):
        image_matrix.append([])
        for j in range(n):
            image_matrix[i].append(0)
    return image_matrix


def apply_filter(image: Image, mask: list) -> list:
    pass


def laplacian(image: Image, mask_type: string) -> Image:
    image = image.copy()
    laplacian_mask = []
    if mask_type == 'cruz':
        for i in range(3):
            laplacian_mask.append([0] * 3)
        laplacian_mask[0][1], laplacian_mask[1][0], laplacian_mask[2][1], laplacian_mask[1][2] = [1, 1, 1, 1]
        laplacian_mask[1][1] = -4
    elif mask_type == 'diagonal':
        for i in range(3):
            laplacian_mask.append([0] * 3)
        laplacian_mask[0][1], laplacian_mask[1][0], laplacian_mask[2][1], laplacian_mask[1][2] = [1, 1, 1, 1]
        laplacian_mask[0][0], laplacian_mask[0][2], laplacian_mask[2][0], laplacian_mask[2][2] = [1, 1, 1, 1]
        laplacian_mask[1][1] = -8

    image_matrix = image_to_matrix(image)
    for y in range(1, image.height-1):
        for x in range(1, image.width-1):
            central_pixel = laplacian_mask[1][1] * image_matrix[x][y] + laplacian_mask[2][1] * image_matrix[x+1][y] + \
                            laplacian_mask[1][0] * image_matrix[x][y-1] + laplacian_mask[0][1] * image_matrix[x-1][y] +\
                            laplacian_mask[1][2] * image_matrix[x][y+1]
            # if central_pixel < 0
            image.putpixel((x, y), central_pixel)
    return image


def unsharp_masking(image: Image, n: int, m: int, k: float) -> Image:
    image = image.copy()
    original_image_matrix = image_to_matrix(image)
    blurred_image_matrix = create_empty_matrix(image.height, image.width)
    n1 = (n/2).__floor__()
    m1 = (m/2).__floor__()
    for y in range(image.height):
        for x in range(image.width):
            central_pixel = 0
            for y1 in range(-n1, n1+1):
                for x1 in range(-m1, m1+1):
                    try:
                        central_pixel += original_image_matrix[x+x1][y+y1]
                    except IndexError:
                        pass
            blurred_image_matrix[y][x] = int(central_pixel/(m*n))

    result = create_empty_matrix(image.height, image.height)
    for y in range(image.height):
        for x in range(image.width):
            result[x][y] = blurred_image_matrix[x][y] - original_image_matrix[x][y]
            # image.putpixel((x, y), original_image_matrix[x][y] + k * (blurred_image_matrix[x][y] - original_image_matrix[x][y]))
    image.show()
    matrix_to_image(blurred_image_matrix, image).show()
    matrix_to_image(result, image).show()
    return image


def highboost():
    pass


def prewitt_border_detection():
    pass


def sobel_border_detection():
    pass


if __name__ == '__main__':
    # with Image.open('imgs/lena_gray.bmp', 'r') as lena_gray:
    #     laplacian(lena_gray, 'cruz')
    #     lena_gray.show()
    with Image.open('imgs/lena_gray.bmp', 'r') as lena_gray:
        result = unsharp_masking(lena_gray, 5, 5, 3)
        result.save('results/lena_gray.bmp')
        result.show()
