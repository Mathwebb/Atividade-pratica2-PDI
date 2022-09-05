from ctypes import resize
from math import floor
from PIL import Image
from spatial_filtering import *


def tresholding(image: Image, treshold: int, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    if image.mode != 'L':
        image = image.convert('L')
    for line in range(image.width):
        for column in range(image.height):
            if image.getpixel((line, column)) > treshold:
                image.putpixel((line, column), 255)
            else:
                image.putpixel((line, column), 0)
    return image


def union(image1: Image, image2: Image) -> Image: 
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = tresholding(image2, 128)
            new_width = image1.width
            new_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = tresholding(image1, 128)
            new_width = image2.width
            new_height = image2.height
            
        result_image = Image.new('L', (new_width, new_height), (255,))
        for line in range(new_width):
            for column in range(new_height):
                if image1.getpixel((line, column)) == 255 or image2.getpixel((line, column)) == 255:
                    result_image.putpixel((line, column), 255)
                else:
                    result_image.putpixel((line, column), 0)
        return result_image

    result_image = Image.new('L', (image1.width, image1.height), (255,))
    for line in range(image1.width):
        for column in range(image1.height):
            if image1.getpixel((line, column)) == 255 or image2.getpixel((line, column)) == 255:
                result_image.putpixel((line, column), 255)
            else:
                result_image.putpixel((line, column), 0)
    return result_image


def intersection(image1: Image, image2: Image) -> Image:
    if image1.width != image2.width and image1.height != image2.height:
        if image1.width < image2.width:
            image2 = image2.resize(image1.size)
            image2 = tresholding(image2, 128)
            new_width = image1.width
            new_height = image1.height
        else:
            image1 = image1.resize(image2.size)
            image1 = tresholding(image1, 128)
            new_width = image2.width
            new_height = image2.height
            
        result_image = Image.new('L', (new_width, new_height), (255,))
        for line in range(new_width):
            for column in range(image1.height):
                if image1.getpixel((line, column)) == 255 and image2.getpixel((line, column)) == 255:
                    result_image.putpixel((line, column), 255)
                else:
                    result_image.putpixel((line, column), 0)
        return result_image

    result_image = Image.new('L', (image1.width, image1.height), (255,))
    for line in range(image1.width):
        for column in range(image1.height):
            if image1.getpixel((line, column)) == 255 and image2.getpixel((line, column)) == 255:
                result_image.putpixel((line, column), 255)
            else:
                result_image.putpixel((line, column), 0)
    return result_image


def difference(image1: Image, image2: Image) -> Image:
    if image1.mode == 'L':
        if image1.width != image2.width and image1.height != image2.height:
            if image1.width < image2.width:
                image2 = image2.resize(image1.size)
                image2 = tresholding(image2, 128)
                new_width = image1.width
                new_height = image1.height
            else:
                image1 = image1.resize(image2.size)
                image1 = tresholding(image1, 128)
                new_width = image2.width
                new_height = image2.height
                
            result_image = Image.new('L', (new_width, new_height), (255,))
            for line in range(new_width):
                for column in range(new_height):
                    result_image.putpixel((line, column), image1.getpixel((line, column)) - image2.getpixel((line, column)))
            return result_image
        
        result_image = Image.new('L', (image1.width, image1.height), (255,))
        for line in range(image1.width):
            for column in range(image1.height):
                result_image.putpixel((line, column), image1.getpixel((line, column)) - image2.getpixel((line, column)))
        return result_image
    else:
        # if image1.width != image2.width and image1.height != image2.height:
        #     if image1.width < image2.width:
        #         image2 = image2.resize(image1.size)
        #         image2 = tresholding(image2, 128)
        #         new_width = image1.width
        #         new_height = image1.height
        #     else:
        #         image1 = image1.resize(image2.size)
        #         image1 = tresholding(image1, 128)
        #         new_width = image2.width
        #         new_height = image2.height
                
        #     result_image = Image.new(image1.mode, (new_width, new_height), (255,))
        #     image2.convert(image1.mode)
        #     result_image_channels = ()
        #     for line in range(new_width):
        #         for column in range(new_height):
        #             [result_image_channels.append(image1.getpixel((line, column))[i] - image2.getpixel((line, column))[i]) for i in range(len(image1.getpixel((line, column))))]
                    
        #     return result_image
        
        # result_image = Image.new(image1.mode, (image1.width, image1.height), (255,))
        # image2.convert(image1.mode)
        # result_image_channels = ()
        # for line in range(image1.width):
        #     for column in range(image1.height):
        #         [result_image_channels.append(image1.getpixel((line, column))[i] - image2.getpixel((line, column))[i]) for i in range(len(image1.getpixel((line, column))))]
        # return result_image
        pass



def complement(image: Image, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    for line in range(image.width):
        for column in range(image.height):
            image.putpixel((line, column), 255 - image.getpixel((line, column)))
    return image


def dilation(image: Image, struc_elem: list, struc_elem_center: tuple, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    m1 = struc_elem_center[0]
    m2 = len(struc_elem)-struc_elem_center[0]-1
    n1 = struc_elem_center[1]
    n2 = len(struc_elem[0])-struc_elem_center[1]-1
    original_image_matrix = image_to_matrix(image)
    for line in range(m1, image.width-m2):
        for column in range(n1, image.height-n2):
            if original_image_matrix[line][column] == 255:
                for line_elem in range(-m1, m2+1):
                    for column_elem in range(-n1, n2+1):
                        if struc_elem[m1+line_elem][n1+column_elem] == 1:
                            image.putpixel((line+line_elem, column+column_elem), 255)
    return image


def erosion(image: Image, struc_elem: list, struc_elem_center: tuple, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    m1 = struc_elem_center[0]
    m2 = len(struc_elem)-struc_elem_center[0]-1
    n1 = struc_elem_center[1]
    n2 = len(struc_elem[0])-struc_elem_center[1]-1
    original_image_matrix = image_to_matrix(image)
    for line in range(m1, image.width-m2):
        for column in range(n1, image.height-n2):
            struc_elem_hit = True
            if original_image_matrix[line][column] == 255:
                for line_elem in range(-m1, m2+1):
                    for column_elem in range(-n1, n2+1):
                        if original_image_matrix[line+line_elem][column+column_elem] == 0 and struc_elem[m1+line_elem][n1+column_elem] == 1:
                            struc_elem_hit = False
                            break
                    if not struc_elem_hit:
                        break
                if not struc_elem_hit:
                        image.putpixel((line, column), 0)
    return image


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


if __name__ == "__main__":
    # with Image.open("imgs/lena_gray.bmp", "r") as image1:
    #     image1 = tresholding(image1, 128)
    #     image1.save("results/questao_3/lena_gray_binary.bmp")
    #     with Image.open("imgs/lena_ruido.bmp", "r") as image2:
    #         image2 = tresholding(image2, 128)
    #         image2.save("results/questao_3/lena_ruido_binary.bmp")

    #         result = union(image1, image2)
    #         result.save("results/questao_3/lena_uniao.bmp")
            
    #         result = intersection(image1, image2)
    #         result.save("results/questao_3/lena_intersecao.bmp")
            
    #         result = difference(image1, image2)
    #         result.save("results/questao_3/lena_diferenca.bmp")
    
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

