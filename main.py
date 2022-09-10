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
    #     result = thresholding(result, 1)
    #     image_bin = extract_region(image, (0, 255, 0, 255))
    #     image_bin = complement(image_bin)
    #     image_bin = image_bin.convert('L')
    #     image_bin = thresholding(image_bin, 1)
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
    #     result = thresholding(result, 1)
    #     image_bin = extract_region(image, (255, 255, 0, 255))
    #     image_bin = complement(image_bin)
    #     image_bin = image_bin.convert('L')
    #     image_bin = thresholding(image_bin, 1)
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
    #     result = thresholding(result, 1)
    #     image_bin = extract_region(image, (0, 0, 255, 255))
    #     image_bin = complement(image_bin)
    #     image_bin = image_bin.convert('L')
    #     image_bin = thresholding(image_bin, 1)
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

    # with Image.open("results/questao_5/resultado_b.png") as image:
    #     green_region = Image.open("results/questao_5/resultado_c_verde.png")
    #     result = extract_region(image, (0, 255, 0, 255))
    #     result = difference(green_region, result, 'white')
    #     green_region = extract_region(image, (0, 255, 0, 255))
    #     result = addition(result, image, 'white')
    #     image = result

    #     yellow_region = Image.open("results/questao_5/resultado_c_amarelo.png")
    #     result = extract_region(image, (255, 255, 0, 255))
    #     result = difference(yellow_region, result, 'white')
    #     yellow_region = extract_region(image, (255, 255, 0, 255))
    #     result = addition(result, image, 'white')
    #     image = result

    #     blue_region = Image.open("results/questao_5/resultado_c_azul.png")
    #     result = extract_region(image, (0, 0, 255, 255))
    #     result = difference(blue_region, result, 'white')
    #     blue_region = extract_region(image, (0, 0, 255, 255))
    #     result = addition(result, image, 'white')
    #     image = result


    #     mask = []
    #     for i in range(21):
    #         mask.append([])
    #         for j in range(21):
    #             mask[i].append(1)
    #     result = extract_region(image, (255, 0, 0, 255))
    #     result = complement(result)
    #     result = thresholding(result, 1)
    #     result = closing(result, mask, (10, 10))
    #     result = complement(result)
    #     result = color_region(result, (255, 0, 0, 255), (0, 0, 0, 255))
    #     result = addition(result, image, 'white')
    #     image = result
        
    #     image.save("results/questao_5/resultado_c_completo.png")

    with Image.open("results/questao_5/resultado_c_completo.png") as image:
        mask = []
        for i in range(9):
            mask.append([])
            for j in range(9):
                mask[i].append(1)
        result = complement(image)
        result = result.convert('L')
        result = thresholding(result, 1)
        skeleton = create_skeleton(result, mask, (2, 2))
        result = Image.new('L', (image.width, image.height))
        for item in skeleton:
            result = union(result, item)
        result.save("results/questao_5/resultado_d.png")
        result.show()
        result = reconstruct_image(skeleton, mask, (2, 2))
        result.show()
        result.save("results/questao_5/resultado_d.png")
        result.show()


if __name__ == "__main__":
    questao_5()
