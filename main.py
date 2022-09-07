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
    pass


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

    with Image.open("results/questao_5/resultado_b.png") as image:
        result = extract_region(image, (0, 255, 0, 255))
        result = complement(result)
        result = result.convert('L')
        result = tresholding(result, 1)
        result_marker = complement_border(result)
        result_complement = complement(result)
        result = geodesic_dilation(result_marker, result_complement, [[1, 1, 1],[1, 1, 1],[1, 1, 1]], (1, 1))
        result.show()
        result = complement(result)
        result = result.convert('L')
        result = color_region(image, (255, 0, 0, 255), (255, 255, 255, 255))



if __name__ == "__main__":
    questao_5()
