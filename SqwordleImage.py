from PIL import Image
import numpy
from SQLite3_tools import *
from math import sqrt, trunc
from BlendPixelArt import Blend


def GenerateImage(db_file, player, palette='rainbow', blend=1):

    c1, c2, c3, c4, c5, c6, c7, c8 = Palette(palette)

    try:
        conn = create_connection(db_file)
        curse = conn.cursor()
        query = 'SELECT u' + str(player) + ' FROM wordlestats ORDER BY game ASC'
        scores = [score[0] for score in curse.execute(query)]
        curse.close()
        conn.close()
    except:
        return False

    scores = list(filter(None, scores))

    scoreLen = len(scores)
    imgWidth = trunc(sqrt(scoreLen)) + 1

    img = []
    for i in range(imgWidth):
        img.append([0]*imgWidth)

    for iScore in range(imgWidth * imgWidth):
        if iScore >= len(scores):
            color = c8
        else:
            if scores[iScore] == 1:
                color = c1
            elif scores[iScore] == 2:
                color = c2
            elif scores[iScore] == 3:
                color = c3
            elif scores[iScore] == 4:
                color = c4
            elif scores[iScore] == 5:
                color = c5
            elif scores[iScore] == 6:
                color = c6
            elif scores[iScore] == 7:
                color = c7
            elif scores[iScore] == None:
                color = c8
        
        prow = trunc(iScore / imgWidth) # Get the row
        pcol = iScore % imgWidth # Get the column
        img[prow][pcol] = color

    img_new = Blend(img, blend)
    img_array = numpy.array(img_new, dtype=numpy.uint8)
    image = Image.fromarray(img_array)
    image = image.resize((480, 480), resample=Image.NEAREST)
    image.save("wordle_image.png")

    return True

def Palette(palette):
    if palette.lower() == 'rainbow':
        #Rainbow
        c1 = (255, 0, 0)
        c2 = (255, 127, 0)
        c3 = (222, 255, 0)
        c4 = (0, 255, 0)
        c5 = (0, 0, 255)
        c6 = (75, 0, 130)
        c7 = (148, 0, 211)
        c8 = (255, 255, 255)

    elif palette.lower() == 'candy':
        #Candy
        c1 = (255, 207, 210)
        c2 = (241, 192, 232)
        c3 = (207, 186, 240)
        c4 = (163, 196, 243)
        c5 = (144, 219, 244)
        c6 = (142, 236, 245)
        c7 = (152, 245, 225)
        c8 = (255, 255, 255)

    elif palette.lower() == 'fire':
        #Fire
        c1 = (106, 4, 15)
        c2 = (157, 2, 8)
        c3 = (208, 0, 0)
        c4 = (220, 47, 2)
        c5 = (232, 93, 4)
        c6 = (244, 140, 6)
        c7 = (250, 163, 7)
        c8 = (0, 0, 0)

    elif palette.lower() == 'muted':
        #Muted
        c1 = (249, 65, 68)
        c2 = (243, 114, 44)
        c3 = (248, 150, 30)
        c4 = (249, 199, 79)
        c5 = (144, 190, 109)
        c6 = (67, 170, 139)
        c7 = (87, 117, 144)
        c8 = (255, 255, 255)

    elif palette.lower() == 'cool':
        #Cool
        c1 = (94, 96, 206)
        c2 = (83, 144, 217)
        c3 = (78, 168, 222)
        c4 = (72, 191, 227)
        c5 = (86, 207, 225)
        c6 = (100, 223, 223)
        c7 = (114, 239, 221)
        c8 = (0, 0, 0)

    elif palette.lower() == 'warm':
        #Warm
        c1 = (255, 149, 0)
        c2 = (255, 162, 0)
        c3 = (255, 170, 0)
        c4 = (255, 183, 0)
        c5 = (255, 195, 0)
        c6 = (255, 208, 0)
        c7 = (255, 221, 0)
        c8 = (0, 0, 0)

    elif palette.lower() == 'murica':
        #Murica
        c1 = (160, 0, 28)
        c2 = (192, 0, 33)
        c3 = (255, 0, 43)
        c4 = (64, 123, 167)
        c5 = (0, 78, 137)
        c6 = (0, 41, 98)
        c7 = (0, 4, 58)
        c8 = (255, 255, 255)

    else:
        c1,c2,c3,c4,c5,c6,c7,c8 = Palette('rainbow')
    
    return c1,c2,c3,c4,c5,c6,c7,c8