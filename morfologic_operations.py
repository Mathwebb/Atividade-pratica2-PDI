from diverse_operators import *
import cv2
import numpy as np


def thresholding(image: Image, treshold: int, modify: bool = False) -> Image:
    if image.mode != 'L':
        image = image.convert('L')
    if not modify:
        image = image.copy()
    for line in range(image.width):
        for column in range(image.height):
            if image.getpixel((line, column)) > treshold:
                image.putpixel((line, column), 255)
            else:
                image.putpixel((line, column), 0)
    return image


def complement(image: Image, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    for line in range(image.width):
        for column in range(image.height):
            if image.mode == 'L':
                image.putpixel((line, column), 255 - image.getpixel((line, column)))
            elif image.mode == 'RGB':
                result_image_channels = ()
                for i in range(len(image.getpixel((line, column)))):
                    result_image_channels += (255 - image.getpixel((line, column))[i],)
                image.putpixel((line, column), result_image_channels)
            elif image.mode == 'RGBA':
                result_image_channels = ()
                for i in range(len(image.getpixel((line, column)))):
                    if i == 3:
                        result_image_channels += (image.getpixel((line, column))[i],)
                    else:
                        result_image_channels += (255 - image.getpixel((line, column))[i],)
                image.putpixel((line, column), result_image_channels)
    return image


def union(image1: Image, image2: Image) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if image1.mode != 'L':
        image1 = image1.convert('L')
    if image2.mode != 'L':
        image2 = image2.convert('L')
    image1 = thresholding(image1, 128)
    image2 = thresholding(image2, 128)
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = thresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = thresholding(image1, 128)
            image_width = image2.width
            image_height = image2.height

    result_image = Image.new(image1.mode, (image_width, image_height), (255,))
    for line in range(image_width):
        for column in range(image_height):
            if image1.getpixel((line, column)) == 255 or image2.getpixel((line, column)) == 255:
                result_image.putpixel((line, column), 255)
            else:
                result_image.putpixel((line, column), 0)
    return result_image


def intersection(image1: Image, image2: Image) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if image1.mode != 'L':
        image1 = image1.convert('L')
    if image2.mode != 'L':
        image2 = image2.convert('L')
    image1 = thresholding(image1, 128)
    image2 = thresholding(image2, 128)
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = thresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = thresholding(image1, 128)
            image_width = image2.width
            image_height = image2.height

    result_image = Image.new('L', (image_width, image_height), (255,))
    for line in range(image_width):
        for column in range(image_height):
            if image1.getpixel((line, column)) == 255 and image2.getpixel((line, column)) == 255:
                result_image.putpixel((line, column), 255)
            else:
                result_image.putpixel((line, column), 0)
    return result_image


def addition(image1: Image, image2: Image, background: str) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if background == 'white':
        image1 = complement(image1)
        image2 = complement(image2)
        result_image = Image.new(image1.mode, (image_width, image_height), (255,))
    else:
        result_image = Image.new(image1.mode, (image_width, image_height), (0,))
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image_width = image2.width
            image_height = image2.height
    if image1.mode != image2.mode:
        image2 = image2.copy()
        image2 = image2.convert(image1.mode)
    for line in range(image_width):
        for column in range(image_height):
            if image1.mode == 'L':
                result_image.putpixel((line, column), image1.getpixel((line, column)) + image2.getpixel((line, column)))
            elif image1.mode == 'RGB':
                result_image_channels = ()
                for i in range(len(image1.getpixel((line, column)))):
                    result_image_channels += (image1.getpixel((line, column))[i] + image2.getpixel((line, column))[i],)
                result_image.putpixel((line, column), result_image_channels)
            elif image1.mode == 'RGBA':
                result_image_channels = ()
                for i in range(len(image1.getpixel((line, column)))):
                    if i == 3:
                        result_image_channels += (image1.getpixel((line, column))[i],)
                    else:
                        result_image_channels += (
                            image1.getpixel((line, column))[i] + image2.getpixel((line, column))[i],)
                result_image.putpixel((line, column), result_image_channels)
    if background == 'white':
        image1 = complement(image1)
        image2 = complement(image2)
        result_image = complement(result_image)
    return result_image


def subtraction(image1: Image, image2: Image, background: str) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if background == 'white':
        image1 = complement(image1)
        image2 = complement(image2)
        result_image = Image.new(image1.mode, (image_width, image_height), (255,))
    else:
        result_image = Image.new(image1.mode, (image_width, image_height), (0,))
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image_width = image2.width
            image_height = image2.height

    image2 = image2.convert(image1.mode)
    for line in range(image_width):
        for column in range(image_height):
            if image1.mode == 'L':
                result_image.putpixel((line, column), image1.getpixel((line, column)) - image2.getpixel((line, column)))
            elif image1.mode == 'RGB':
                result_image_channels = ()
                for i in range(len(image1.getpixel((line, column)))):
                    result_image_channels += (image1.getpixel((line, column))[i] - image2.getpixel((line, column))[i],)
                result_image.putpixel((line, column), result_image_channels)
            elif image1.mode == 'RGBA':
                result_image_channels = ()
                for i in range(len(image1.getpixel((line, column)))):
                    if i == 3:
                        result_image_channels += (image1.getpixel((line, column))[i],)
                    else:
                        result_image_channels += (
                            image1.getpixel((line, column))[i] - image2.getpixel((line, column))[i],)
                result_image.putpixel((line, column), result_image_channels)
    if background == 'white':
        image1 = complement(image1)
        image2 = complement(image2)
        result_image = complement(result_image)
    return result_image


def difference(image1: Image, image2: Image) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if image1.mode != 'L':
        image1 = image1.convert('L')
    if image2.mode != 'L':
        image2 = image2.convert('L')
    image1 = thresholding(image1, 128)
    image2 = thresholding(image2, 128)
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = thresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = thresholding(image1, 128)
            image_width = image2.width
            image_height = image2.height

    result_image = Image.new('L', (image_width, image_height), (255,))
    for line in range(image_width):
        for column in range(image_height):
            result_image.putpixel((line, column), image1.getpixel((line, column)) - image2.getpixel((line, column)))
    return result_image


def dilation(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    image = image.copy()
    if image.mode != 'L':
        image = image.convert('L')
    image = thresholding(image, 128)
    m1 = struc_elem_center[0]
    m2 = len(struc_elem) - struc_elem_center[0] - 1
    n1 = struc_elem_center[1]
    n2 = len(struc_elem[0]) - struc_elem_center[1] - 1
    original_image_matrix = image_to_matrix(image)
    for line in range(image.width):
        for column in range(image.height):
            if original_image_matrix[line][column] == 255:
                for line_elem in range(-m1, m2 + 1):
                    for column_elem in range(-n1, n2 + 1):
                        if struc_elem[m1 + line_elem][n1 + column_elem] == 1:
                            try:
                                image.putpixel((line + line_elem, column + column_elem), 255)
                            except IndexError:
                                pass
    return image


def erosion(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    image = image.copy()
    if image.mode != 'L':
        image = image.convert('L')
    image = thresholding(image, 128)
    m1 = struc_elem_center[0]
    m2 = len(struc_elem) - struc_elem_center[0] - 1
    n1 = struc_elem_center[1]
    n2 = len(struc_elem[0]) - struc_elem_center[1] - 1
    original_image_matrix = image_to_matrix(image)
    for line in range(image.width):
        for column in range(image.height):
            struc_elem_hit = True
            if original_image_matrix[line][column] == 255:
                for line_elem in range(-m1, m2 + 1):
                    for column_elem in range(-n1, n2 + 1):
                        try:
                            if original_image_matrix[line + line_elem][column + column_elem] == 0 and \
                                    struc_elem[m1 + line_elem][n1 + column_elem] == 1:
                                struc_elem_hit = False
                                break
                        except IndexError:
                            pass
                    if not struc_elem_hit:
                        break
                if not struc_elem_hit:
                    image.putpixel((line, column), 0)
    return image


def geodesic_dilation(marker: Image, mask: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    marker = marker.copy()
    mask = mask.copy()
    marker = thresholding(marker, 128)
    mask = thresholding(mask, 128)
    if marker.width != mask.width and marker.height != mask.height:
        if marker.width < marker.width:
            marker = marker.resize(marker.size)
            marker = thresholding(marker, 128)
        else:
            marker = marker.resize(marker.size)
            marker = thresholding(marker, 128)

    if marker.mode != 'L':
        marker = marker.convert('L')
    if mask.mode != 'L':
        mask = mask.convert('L')
    result_image = dilation(marker, struc_elem, struc_elem_center)
    result_image = intersection(result_image, mask)
    return result_image


def opening(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    image = image.copy()
    image = erosion(image, struc_elem, struc_elem_center)
    image = dilation(image, struc_elem, struc_elem_center)
    return image


def closing(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    image = image.copy()
    image = dilation(image, struc_elem, struc_elem_center)
    image = erosion(image, struc_elem, struc_elem_center)
    return image


def fill_holes(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    image = image.copy()
    image_complement = complement(image)
    marker = Image.new('L', image.size)
    result_image = complement_border(image)
    while result_image != marker:
        marker = result_image
        result_image = geodesic_dilation(marker, image_complement, struc_elem, struc_elem_center)
    return complement(result_image)


def create_skeleton(image: Image, struc_elem: list, struc_elem_center: tuple) -> list:
    image = image.copy()
    if image.mode != 'L':
        image = image.convert('L')
    image = thresholding(image, 1)
    empty_image = Image.new('L', image.size)
    empty_image.show()
    result = image
    skeleton = []
    result_difference = empty_image.copy()
    while result != empty_image:
        skeleton.append(result_difference)
        result = erosion(result, struc_elem, struc_elem_center)
        result_difference = difference(result, dilation(result, struc_elem, struc_elem_center))
        result_difference.show()
    return skeleton


def create_skeleton_opencv(image: str):
    # Read the image as a grayscale image
    img = cv2.imread(image, 0)

    # Threshold the image
    ret, img = cv2.threshold(img, 127, 255, 0)

    # Step 1: Create an empty skeleton
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    # Get a Cross Shaped Kernel
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Repeat steps 2-4
    while True:
        # Step 2: Open the image
        open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
        # Step 3: Substract open from the original image
        temp = cv2.subtract(img, open)
        # Step 4: Erode the original image and refine the skeleton
        eroded = cv2.erode(img, element)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
        if cv2.countNonZero(img) == 0:
            break

    # Displaying the final skeleton
    cv2.imwrite("results/trabalho_extra/questao_3/skeleton.jpg", skel)


def reconstruct_image(skeleton: list, struc_elem: list, struc_elem_center: tuple) -> Image:
    skeleton = skeleton.copy()
    image = Image.new('L', skeleton[0].size)
    result = Image.new('L', skeleton[0].size)
    for i in range(len(skeleton)):
        image = union(image, result)
        for j in range(1, i):
            if j == 1:
                result = dilation(skeleton[i], struc_elem, struc_elem_center)
                continue
            result = dilation(result, struc_elem, struc_elem_center)
    return image


def hit_or_miss(image: Image, struc_elem_b1: list, struc_elem_b2: list, struc_elem_b1_center: tuple,
                struc_elem_b2_center: tuple) -> Image:
    image = image.copy()
    if image.mode != 'L':
        image = image.convert('L')
    image = thresholding(image, 128)
    image_complement = image.copy()
    image = complement(image)
    image_b1 = erosion(image, struc_elem_b1, struc_elem_b1_center)
    image_b1.show()
    image_b2 = erosion(image_complement, struc_elem_b2, struc_elem_b2_center)
    image_b2.show()
    result_image = intersection(image_b1, image_b2)
    return result_image
