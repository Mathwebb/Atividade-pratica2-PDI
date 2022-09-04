from ctypes import resize
from PIL import Image


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


def complement(image: Image, modify: bool = False) -> Image:
    if not modify:
        image = image.copy()
    for line in range(image.width):
        for column in range(image.height):
            image.putpixel((line, column), 255 - image.getpixel((line, column)))
    return image


def dilation(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    pass


def erosion(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    pass


def opening(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    pass


def closing(image: Image, struc_elem: list, struc_elem_center: tuple) -> Image:
    pass


if __name__ == "__main__":
    with Image.open("imgs/lena_gray.bmp", "r") as image1:
        image1 = tresholding(image1, 128)
        image1.save("results/questao_3/lena_gray_binary.bmp")
        with Image.open("imgs/lena_ruido.bmp", "r") as image2:
            image2 = tresholding(image2, 128)
            image2.save("results/questao_3/lena_ruido_binary.bmp")

            result = union(image1, image2)
            result.save("results/questao_3/lena_uniao.bmp")
            
            result = intersection(image1, image2)
            result.save("results/questao_3/lena_intersecao.bmp")
            
            result = difference(image1, image2)
            result.save("results/questao_3/lena_diferenca.bmp")
    
    with Image.open("imgs/qPreto.png") as image1:
        image1 = image1.convert('L')
        image1 = complement(image1)
        with Image.open("imgs/tPreto.png") as image2:
            image2 = image2.convert('L')
            image2 = complement(image2)

            result = union(image1, image2)
            result.save("results/questao_3/qPreto_tPreto_uniao.png")
            result.show()
            
            result = intersection(image1, image2)
            result.save("results/questao_3/qPreto_tPreto_intersecao.png")
            result.show()
            
            result = difference(image1, image2)
            result.save("results/questao_3/qPreto_tPreto_diferenca.png")
            result.show()

