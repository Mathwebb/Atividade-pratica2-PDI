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


def apply_filter(image: Image, mask: list, interest_pixel: tuple) -> list:
    pass


def laplacian(image: Image, mask_type: string, modify: bool = False) -> Image:
    if not modify:
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
        for i in range(3):
            for j in range(3):
                if j == 0 and i == 0:
                    laplacian_mask[i][j] = -8
                else:
                    laplacian_mask[i][j] = 1

    image_matrix = image_to_matrix(image)
    for y in range(1, image.height - 1):
        for x in range(1, image.width - 1):
            central_pixel = 0
            for y1 in range(-1, 2):
                for x1 in range(-1, 2):
                    central_pixel += laplacian_mask[x1][y1] * image_matrix[x-x1][y-y1]
            image.putpixel((y, x), central_pixel)
            # if central_pixel < 0:
            #     central_pixel *= -1
            #     if central_pixel % 2 == 0:
            #         resultado = int(central_pixel / 2)
            #         image.putpixel((y, x), resultado)
            #     else:
            #         resultado = int((central_pixel - 1) / 2)
            #         image.putpixel((y, x), resultado)
            # else:
            #     if central_pixel % 2 == 0:
            #         resultado = int(central_pixel / 2) + 127
            #         image.putpixel((y, x), resultado)
            #     else:
            #         resultado = int((central_pixel - 1) / 2) + 127
            #         image.putpixel((y, x), resultado)
    return image


def unsharp_masking(image: Image, n: int, m: int, k: float, modify: bool = False) -> Image:
    if not modify:
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

    for y in range(image.height):
        for x in range(image.width):
            image.putpixel((x, y), original_image_matrix[y][x] + int(k * original_image_matrix[y][x] -
                                                                     blurred_image_matrix[x][y]))
    return image


def highboost():
    pass


def prewitt_border_detection():
    pass


def sobel_border_detection():
    pass


if __name__ == '__main__':
    # with Image.open('imgs/lena_gray.bmp', 'r') as lena_gray:
        # result = laplacian(lena_gray, 'diagonal')
        # result.show()
        # result.save('results/lena_diag.bmp')
    with Image.open('imgs/lena_gray.bmp', 'r') as lena_gray:
        result = unsharp_masking(lena_gray, 5, 5, 1)
        result.save('results/lena_gray_sharpen.bmp')
        result.show()
