from tarfile import ExtractError
from turtle import color
from spatial_filtering import *
from morfologic_operations import *
from diverse_operators import *


def questao_1():  
    with Image.open("imgs/operadores_morfologicos/triang_branco.png") as image1:
        pass
        with Image.open("imgs/operadores_morfologicos/losango_branco.png") as image2:
            result = difference(image1, image2)
            result.show()
            result = union(image1, image2)
            result.show()
            result = intersection(image1, image2)
            result.show()


def questao_2():
    pass


def questao_3():
    pass


def questao_4():
    with Image.open("imgs/operadores_morfologicos/losango_branco.png") as image:
        result = dilation(image, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], (2, 2))
        result = difference(result, image)
        result.show()


def questao_5():
    # with Image.open("imgs/quadro.png") as image:
    #     result = extract_region(image, (0, 0, 0, 255))
    #     result = complement(result)
    #     result = closing(result, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], (2, 2))
    #     result.show()
    #     image = complement(image)
    #     image = addition(image, result)
    #     image = complement(image)
    #     image.save("results/questao_5/resultado_a.png")
    #     image.show()
    
    # with Image.open("imgs/quadro.png") as image:
    #     result = extract_region(image, (0, 0, 0, 255))
    #     result = complement(result)
    #     image = complement(image)
    #     image = difference(image, result)
    #     image = complement(image)
    #     image.save("results/questao_5/resultado_b.png")
    #     image.show()

    # with Image.open("results/questao_5/resultado_b.png") as image:
    #     result = extract_region(image, (0, 255, 0, 255))
    #     result = complement(result)
    #     result = result.convert('L')
    #     result = tresholding(result, 1)
    #     image_bin = extract_region(image, (0, 255, 0, 255))
    #     image_bin = complement(image_bin)
    #     image_bin = image_bin.convert('L')
    #     image_bin = tresholding(image_bin, 1)
    #     mask = []
    #     for i in range(9):
    #         mask.append([])
    #         for j in range(9):
    #             mask[i].append(1)
    #     result = fill_holes(result, mask, (4, 4))
    #     result = complement(result)
    #     result = difference(result, image_bin)
    #     result = result.convert('RGBA')
    #     result = color_region(result, (0, 255, 0, 255), (0, 0, 0, 255))
    #     result.save("results/questao_5/resultado_c_verde.png")
    #     # image.save("results/questao_5/resultado_c_verde.png")
        
    #     result = extract_region(image, (255, 255, 0, 255))
    #     result = complement(result)
    #     result = result.convert('L')
    #     result = tresholding(result, 1)
    #     image_bin = extract_region(image, (255, 255, 0, 255))
    #     image_bin = complement(image_bin)
    #     image_bin = image_bin.convert('L')
    #     image_bin = tresholding(image_bin, 1)
    #     mask = []
    #     for i in range(9):
    #         mask.append([])
    #         for j in range(9):
    #             mask[i].append(1)
    #     result = fill_holes(result, mask, (4, 4))
    #     result = complement(result)
    #     result = difference(result, image_bin)
    #     result = result.convert('RGBA')
    #     result = color_region(result, (255, 255, 0, 255), (0, 0, 0, 255))
    #     result.save("results/questao_5/resultado_c_amarelo.png")
        
    #     result = extract_region(image, (0, 0, 255, 255))
    #     result = complement(result)
    #     result = result.convert('L')
    #     result = tresholding(result, 1)
    #     image_bin = extract_region(image, (0, 0, 255, 255))
    #     image_bin = complement(image_bin)
    #     image_bin = image_bin.convert('L')
    #     image_bin = tresholding(image_bin, 1)
    #     mask = []
    #     for i in range(9):
    #         mask.append([])
    #         for j in range(9):
    #             mask[i].append(1)
    #     result = fill_holes(result, mask, (4, 4))
    #     result = complement(result)
    #     result = difference(result, image_bin)
    #     result = result.convert('RGBA')
    #     result = color_region(result, (0, 0, 255, 255), (0, 0, 0, 255))
    #     result.save("results/questao_5/resultado_c_azul.png")
    with Image.open("results/questao_5/resultado_b.png") as image:
        green_region = Image.open("results/questao_5/resultado_c_verde.png")
        result = extract_region(image, (0, 255, 0, 255))
        result = difference(result, green_region)
        result = complement(result)
        green_region = extract_region(image, (0, 255, 0, 255))
        image = complement(image)
        result = complement(result)
        result = addition(result, image)
        result = complement(result)
        image = result

        yellow_region = Image.open("results/questao_5/resultado_c_amarelo.png")
        result = extract_region(image, (255, 255, 0, 255))
        result = difference(result, yellow_region)
        result = complement(result)
        yellow_region = extract_region(image, (255, 255, 0, 255))
        image = complement(image)
        result = complement(result)
        result = addition(result, image)
        result = complement(result)
        image = result

        blue_region = Image.open("results/questao_5/resultado_c_azul.png")
        result = extract_region(image, (0, 0, 255, 255))
        result = difference(result, blue_region)
        result = complement(result)
        blue_region = extract_region(image, (0, 0, 255, 255))
        image = complement(image)
        result = complement(result)
        result = addition(result, image)
        result = complement(result)
        image = result


        mask = []
        for i in range(21):
            mask.append([])
            for j in range(21):
                mask[i].append(1)
        red_region = extract_region(image, (255, 0, 0, 255))
        red_region = complement(red_region)
        red_region = tresholding(red_region, 1)
        red_region = closing(red_region, mask, (10, 10))
        red_region = complement(red_region)
        red_region.show()
        red_region = color_region(red_region, (255, 0, 0, 255), (0, 0, 0, 255))
        red_region.show()

        red_region = complement(red_region)
        image = complement(image)
        result = addition(red_region, image)
        result = complement(result)
        image = result
        
        image.save("results/questao_5/resultado_c_completo.png")


if __name__ == "__main__":
    questao_5()
