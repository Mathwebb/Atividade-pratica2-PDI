import string
from PIL import Image


def laplacian(image: Image, mask_type: string) -> Image:
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

    image_matrix = []
    for i in range(image.height):
        image_matrix.append([image.getpixel((0, i))])
        for j in range(1, image.width):
            image_matrix[i].append(image.getpixel((j, i)))

    for i in range(1, image.height-1):
        for j in range(1, image.width-1):
            central_pixel = laplacian_mask[1][1] * image_matrix[i][j] + laplacian_mask[2][1] * image_matrix[i+1][j] + \
                            laplacian_mask[1][0] * image_matrix[i][j-1] + laplacian_mask[0][1] * image_matrix[i-1][j] +\
                            laplacian_mask[1][2] * image_matrix[i][j+1]
            image.putpixel((i, j), central_pixel)
    return image


def unsharp_masking(image: Image, mask_values, k: float) -> Image:
    pass


def highboost():
    pass


def prewitt_border_detection():
    pass


def sobel_border_detection():
    pass


if __name__ == '__main__':
    with Image.open('imgs/lena_gray.bmp', 'r') as lena_gray:
        laplacian(lena_gray, 'cruz')
        lena_gray.show()
