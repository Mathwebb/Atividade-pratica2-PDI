from PIL import Image
from spatial_filtering import *


def tresholding(image: Image, treshold: int, modify: bool = False) -> Image:
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


def union(image1: Image, image2: Image) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if image1.mode != 'L':
        image1 = image1.convert('L')
    if image2.mode != 'L':
        image2 = image2.convert('L')
    image1 = tresholding(image1, 128)
    image2 = tresholding(image2, 128)
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = tresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = tresholding(image1, 128)
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
    image1 = tresholding(image1, 128)
    image2 = tresholding(image2, 128)
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = tresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = tresholding(image1, 128)
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


def addition(image1: Image, image2: Image) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = tresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = tresholding(image1, 128)
            image_width = image2.width
            image_height = image2.height

    if image1.mode != image2.mode:
        image2 = image2.copy()
        image2 = image2.convert(image1.mode)
    for line in range(image_width):
        for column in range(image_height):
            if image1.mode == 'L':
                image1.putpixel((line, column), image1.getpixel((line, column)) + image2.getpixel((line, column)))
            elif image1.mode == 'RGB':
                image1_channels = ()
                for i in range(len(image1.getpixel((line, column)))):
                    image1_channels += (image1.getpixel((line, column))[i] + image2.getpixel((line, column))[i],)
                image1.putpixel((line, column), image1_channels)
            elif image1.mode == 'RGBA':
                image1_channels = ()
                for i in range(len(image1.getpixel((line, column)))):
                    if i == 3:
                        image1_channels += (image1.getpixel((line, column))[i],)
                    else:
                        image1_channels += (image1.getpixel((line, column))[i] + image2.getpixel((line, column))[i],)
                image1.putpixel((line, column), image1_channels)
    return image1


def difference(image1: Image, image2: Image) -> Image:
    image_width = image1.width
    image_height = image1.height
    image1 = image1.copy()
    image2 = image2.copy()
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = tresholding(image2, 128)
            image_width = image1.width
            image_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = tresholding(image1, 128)
            image_width = image2.width
            image_height = image2.height

    result_image = Image.new(image1.mode, (image_width, image_height), (255,))
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
                        result_image_channels += (image1.getpixel((line, column))[i] - image2.getpixel((line, column))[i],)
                result_image.putpixel((line, column), result_image_channels)
    return result_image


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


def dilation(image: Image, struc_elem: list, struc_elem_center: tuple, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    m1 = struc_elem_center[0]
    m2 = len(struc_elem)-struc_elem_center[0]-1
    n1 = struc_elem_center[1]
    n2 = len(struc_elem[0])-struc_elem_center[1]-1
    original_image_matrix = image_to_matrix(image)
    for line in range(image.width):
        for column in range(image.height):
            if original_image_matrix[line][column] == 255:
                for line_elem in range(-m1, m2+1):
                    for column_elem in range(-n1, n2+1):
                        if struc_elem[m1+line_elem][n1+column_elem] == 1:
                            try:
                                image.putpixel((line+line_elem, column+column_elem), 255)
                            except IndexError:
                                pass
    return image


def erosion(image: Image, struc_elem: list, struc_elem_center: tuple, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    m1 = struc_elem_center[0]
    m2 = len(struc_elem)-struc_elem_center[0]-1
    n1 = struc_elem_center[1]
    n2 = len(struc_elem[0])-struc_elem_center[1]-1
    original_image_matrix = image_to_matrix(image)
    for line in range(image.width):
        for column in range(image.height):
            struc_elem_hit = True
            if original_image_matrix[line][column] == 255:
                for line_elem in range(-m1, m2+1):
                    for column_elem in range(-n1, n2+1):
                        try:
                            if original_image_matrix[line+line_elem][column+column_elem] == 0 and struc_elem[m1+line_elem][n1+column_elem] == 1:
                                struc_elem_hit = False
                                break
                        except IndexError:
                            pass
                    if not struc_elem_hit:
                        break
                if not struc_elem_hit:
                        image.putpixel((line, column), 0)
    return image


def geodesic_dilation(marker: Image, mask: Image,struc_elem: list, struc_elem_center: tuple) -> Image:
    marker = marker.copy()
    mask = mask.copy()
    marker = tresholding(marker, 128)
    mask = tresholding(mask, 128)
    if marker.width != mask.width and marker.height != mask.height:
        if marker.width < image_height.width:
            image_height = image_height.resize(marker.size)
            image_height = tresholding(image_height, 128)
        else:
            marker = marker.resize(image_height.size)
            marker = tresholding(marker, 128)
    
    if marker.mode != 'L':
        marker = marker.convert('L')
    if mask.mode != 'L':
        mask = mask.convert('L')
    result_image = dilation(marker, struc_elem, struc_elem_center)
    result_image = intersection(result_image, mask)
    i = 0
    while result_image != marker:
        i += 1
        marker = result_image
        result_image = dilation(marker, struc_elem, struc_elem_center)
        result_image = intersection(result_image, mask)
    return difference(marker, mask)


def opening(image: Image, struc_elem: list, struc_elem_center: tuple, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    image = erosion(image, struc_elem, struc_elem_center, True)
    image = dilation(image, struc_elem, struc_elem_center, True)
    return image


def closing(image: Image, struc_elem: list, struc_elem_center: tuple, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    image = dilation(image, struc_elem, struc_elem_center, True)
    image = erosion(image, struc_elem, struc_elem_center, True)
    return image


def fill_holes(image: Image, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    
    return image


def create_skeleton(image: Image, modify: bool = False) -> Image:
    pass

def reconstruct_image(skeleton: Image, modify: bool = False) -> Image:
    pass


if __name__ == "__main__":    
    with Image.open("imgs/imagem_abertura.png") as image1:
        image1 = image1.convert('L')
        image1 = complement(image1)

        result = opening(image1, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], (1, 1))
        result = complement(result)
        result.save("results/questao_3/qPreto_tPreto_abertura.png")
    
    with Image.open("imgs/imagem_fechamento.png") as image1:
        image1 = image1.convert('L')
        image1 = complement(image1)

        result = closing(image1, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], (1, 1))
        result = complement(result)
        result.save("results/questao_3/qPreto_tPreto_fechamento.png")

