from optparse import OptParseError
from spatial_filtering import *
from morfologic_operations import *

with Image.open("imgs/quadro.png") as image:
    result = tresholding(image, 1)
    result = result.convert('RGB')
    image = difference(image, result)
    image.show()
