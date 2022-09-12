from spatial_filtering import *
from morfologic_operations import *
from diverse_operators import *


def questao_1():  
    with Image.open("imgs/filtragem_espacial/lena_gray.bmp") as image:
        result, laplacian_image = laplacian_filter(image, -8, False, False)
        result.save("results/questao_1/letra_a/lena_laplacian_sharpened_-8.bmp")
        laplacian_image.save("results/questao_1/letra_a/lena_laplacian_unadjusted_-8.bmp")
        result, laplacian_image = laplacian_filter(image, -4, False, True)
        result.save("results/questao_1/letra_a/lena_laplacian_sharpened_-4.bmp")
        laplacian_image.save("results/questao_1/letra_a/lena_laplacian_adjusted_-4.bmp")
        result = unsharp_masking(image, 3, 3)
        result.save("results/questao_1/letra_b/lena_unsharp_masking_3x3.bmp")
        result = high_boost(image, 3, 3, 2)
        result.save("results/questao_1/letra_c/lena_high_boost_3x3_k-2.bmp")
        result = high_boost(image, 3, 3, 5)
        result.save("results/questao_1/letra_c/lena_high_boost_3x3_k-5.bmp")
        result = high_boost(image, 3, 3, 10)
        result.save("results/questao_1/letra_c/lena_high_boost_3x3_k-10.bmp")
        result = prewitt_border_detection(image, True)
        result.save("results/questao_1/letra_d/lena_prewitt_horizontal.bmp")
        result = prewitt_border_detection(image, False)
        result.save("results/questao_1/letra_d/lena_prewitt_vertical.bmp")
        result = sobel_border_detection(image, True)
        result.save("results/questao_1/letra_d/lena_sobel_horizontal.bmp")
        result = sobel_border_detection(image, False)
        result.save("results/questao_1/letra_d/lena_sobel_vertical.bmp")


def questao_2():
    with Image.open("imgs/filtragem_espacial/lena_ruido.bmp") as image:
        result = weighted_arithmetic_mean_filter(image, [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        result.save("results/questao_2/lena_weighted_mean_filter_3x3_1s_cross.png")
        result = weighted_arithmetic_mean_filter(image, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        result.save("results/questao_2/lena_arithmetic_mean_filter_3x3_1s_square.png")
        result = weighted_arithmetic_mean_filter(image, [[1, 3, 1], [3, 16, 3], [1, 3, 1]])
        result.save("results/questao_2/lena_weighted_mean_filter_3x3_square_16_center.png")
        result = weighted_arithmetic_mean_filter(image, [[0, 1, 0], [1, 4, 1], [0, 1, 0]])
        result.save("results/questao_2/lena_weighted_mean_filter_3x3_cross_4_center.png")
        result = median_filter(image, 3, 3)
        result.save("results/questao_2/lena_median_filter_3x3_1_time.png")
        result = median_filter(result, 3, 3)
        result.save("results/questao_2/lena_median_filter_3x3_2_times.png")
        result = median_filter(result, 3, 3)
        result.save("results/questao_2/lena_median_filter_3x3_3_times.png")
        result = median_filter(result, 3, 3)
        result.save("results/questao_2/lena_median_filter_3x3_4_times.png")



def questao_3():
    with Image.open("imgs/operadores_morfologicos/triang_branco.png") as image1:
        with Image.open("imgs/operadores_morfologicos/losango_branco.png") as image2:
            result = union(image1, image2)
            result.save("results/questao_3/letra_a/triang_losango_union.png")
            result = intersection(image1, image2)
            result.save("results/questao_3/letra_b/triang_losango_intersection.png")
            result = difference(image1, image2)
            result.save("results/questao_3/letra_c/triang_losango_difference.png")
        with Image.open("imgs/operadores_morfologicos/quad_branco.png") as image2:
            result = union(image1, image2)
            result.save("results/questao_3/letra_a/triang_quad_union.png")
            result = intersection(image1, image2)
            result.save("results/questao_3/letra_b/triang_quad_intersection.png")
            result = difference(image1, image2)
            result.save("results/questao_3/letra_c/triang_quad_difference.png")


def questao_4():
    mask = []
    for i in range(5):
        mask.append([])
        for j in range(5):
            mask[i].append(1)
    with Image.open("imgs/operadores_morfologicos/folha.png") as image:
        result = dilation(image, mask, (2, 2))
        result.save("results/questao_4/letra_a/folha_dilation_5x5.png")
        result = erosion(image, mask, (2, 2))
        result.save("results/questao_4/letra_b/folha_erosion_5x5.png")
    with Image.open("imgs/operadores_morfologicos/imagem_abertura.png") as image:
        result = opening(image, mask, (2, 2))
        result.save("results/questao_4/letra_c/imagem_abertura.png")
    with Image.open("imgs/operadores_morfologicos/imagem_fechamento.png") as image:
        result = closing(image, mask, (2, 2))
        result.save("results/questao_4/letra_d/imagem_fechamento.png")


def questao_5_a():
    with Image.open("imgs/quadro.png") as image:
        result = extract_region(image, (0, 0, 0, 255))
        result = complement(result)
        result = closing(result, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], (2, 2))
        result = complement(result)
        image = addition(image, result, 'white')
        image.save("results/questao_5/resultado_a.png")


def questao_5_b():
    with Image.open("imgs/quadro.png") as image:
        result = extract_region(image, (0, 0, 0, 255))
        image = subtraction(image, result, 'white')
        image.save("results/questao_5/resultado_b.png")


def questao_5_c():
    pass


def questao_5_d():
    with Image.open("results/questao_5/resultado_c_completo.png") as image:
        mask = []
        for i in range(9):
            mask.append([])
            for j in range(9):
                mask[i].append(1)
        result = extract_region(image, (0, 255, 0, 255))
        result = complement(result)
        result = result.convert('L')
        result = thresholding(result, 1)
        skeleton = create_skeleton(result, mask, (4, 4))
        result = Image.new('L', (image.width, image.height))
        for item in skeleton:
            result = union(result, item)
        result = complement(result)
        result = color_region(result, (0, 255, 0, 255), (0, 0, 0, 255))
        result = color_region(result, (0, 0, 0, 255), (255, 255, 255, 255))
        result.save("results/questao_5/resultado_d_verde.png")
        result.show()
        result = reconstruct_image(skeleton, mask, (4, 4))
        result.show()

        
        result = extract_region(image, (255, 255, 0, 255))
        result = complement(result)
        result = result.convert('L')
        result = thresholding(result, 1)
        skeleton = create_skeleton(result, mask, (4, 4))
        result = Image.new('L', (image.width, image.height))
        for item in skeleton:
            result = union(result, item)
        result = complement(result)
        result = color_region(result, (255, 255, 0, 255), (0, 0, 0, 255))
        result = color_region(result, (0, 0, 0, 255), (255, 255, 255, 255))
        result.save("results/questao_5/resultado_d_amarelo.png")
        result.show()
        result = reconstruct_image(skeleton, mask, (4, 4))
        result.show()

        
        result = extract_region(image, (0, 0, 255, 255))
        result = complement(result)
        result = result.convert('L')
        result = thresholding(result, 1)
        skeleton = create_skeleton(result, mask, (4, 4))
        result = Image.new('L', (image.width, image.height))
        for item in skeleton:
            result = union(result, item)
        result = complement(result)
        result = color_region(result, (0, 0, 255, 255), (0, 0, 0, 255))
        result = color_region(result, (0, 0, 0, 255), (255, 255, 255, 255))
        result.save("results/questao_5/resultado_d_azul.png")
        result.show()
        result = reconstruct_image(skeleton, mask, (4, 4))
        result.show()


def questao_5_e():
    pass


def questao_5():
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

    with Image.open("results/questao_5/resultado_b.png") as image:
        green_region = Image.open("results/questao_5/resultado_c_verde.png")
        result = extract_region(image, (0, 255, 0, 255))
        result = subtraction(green_region, result, 'white')
        green_region = extract_region(image, (0, 255, 0, 255))
        result = addition(result, image, 'white')
        image = result

        yellow_region = Image.open("results/questao_5/resultado_c_amarelo.png")
        result = extract_region(image, (255, 255, 0, 255))
        result = subtraction(yellow_region, result, 'white')
        yellow_region = extract_region(image, (255, 255, 0, 255))
        result = addition(result, image, 'white')
        image = result

        blue_region = Image.open("results/questao_5/resultado_c_azul.png")
        result = extract_region(image, (0, 0, 255, 255))
        result = subtraction(blue_region, result, 'white')
        blue_region = extract_region(image, (0, 0, 255, 255))
        result = addition(result, image, 'white')
        image = result


        # mask = []
        # for i in range(21):
        #     mask.append([])
        #     for j in range(21):
        #         mask[i].append(1)
        # result = extract_region(image, (255, 0, 0, 255))
        # result = complement(result)
        # result = thresholding(result, 1)
        # result = closing(result, mask, (10, 10))
        # result = complement(result)
        # result = color_region(result, (255, 0, 0, 255), (0, 0, 0, 255))
        # result = addition(result, image, 'white')
        # image = result
        
        image.save("results/questao_5/resultado_c_completo.png")


if __name__ == "__main__":
    questao_2()
