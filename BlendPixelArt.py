from math import floor, ceil, sqrt
# Blend pixel art

def Blend(img, n):
    # Get image width
    imgWidth = len(img)

    img_new = []
    if n == 1:
        newWidth = n*imgWidth
    else:
        newWidth = n*imgWidth - (n-1)
    for i in range(newWidth):
        img_new.append([0]*newWidth)

    for i in range(newWidth):
        for j in range(newWidth):
            if (i == 0 and j == 0) or (i%n == 0 and j%n == 0):
                img_new[i][j] = img[int(i/n)][int(j/n)]
            else:
                ilow = int(floor(i/n))
                ihigh = int(ceil(i/n))
                jlow = int(floor(j/n))
                jhigh = int(ceil(j/n))

                iup = (i/n) % 1
                idwn = 1 - (i/n) % 1
                jbak = (j/n) % 1
                jfwd = 1 - (j/n) % 1
                
                if ilow == ihigh:
                    r = img[ilow][jlow][0] * jfwd + \
                        img[ilow][jhigh][0] * jbak

                    g = img[ilow][jlow][1] * jfwd + \
                        img[ilow][jhigh][1] * jbak

                    b = img[ilow][jlow][2] * jfwd + \
                        img[ilow][jhigh][2] * jbak

                elif jlow == jhigh:
                    r = img[ilow][jlow][0] * idwn + \
                        img[ihigh][jlow][0] * iup

                    g = img[ilow][jlow][1] * idwn + \
                        img[ihigh][jlow][1] * iup

                    b = img[ilow][jlow][2] * idwn + \
                        img[ihigh][jlow][2] * iup

                else:
                    r = (img[ilow][jlow][0] * jfwd + \
                        img[ilow][jhigh][0] * jbak + \
                        img[ihigh][jlow][0] * jfwd + \
                        img[ihigh][jhigh][0] * jbak)/4 + \
                        (img[ilow][jlow][0] * idwn + \
                        img[ilow][jhigh][0] * idwn + \
                        img[ihigh][jlow][0] * iup + \
                        img[ihigh][jhigh][0] * iup)/4

                    g = (img[ilow][jlow][1] * jfwd + \
                        img[ilow][jhigh][1] * jbak + \
                        img[ihigh][jlow][1] * jfwd + \
                        img[ihigh][jhigh][1] * jbak)/4 + \
                        (img[ilow][jlow][1] * idwn + \
                        img[ilow][jhigh][1] * idwn + \
                        img[ihigh][jlow][1] * iup + \
                        img[ihigh][jhigh][1] * iup)/4

                    b = (img[ilow][jlow][2] * jfwd + \
                        img[ilow][jhigh][2] * jbak + \
                        img[ihigh][jlow][2] * jfwd + \
                        img[ihigh][jhigh][2] * jbak)/4 + \
                        (img[ilow][jlow][2] * idwn + \
                        img[ilow][jhigh][2] * idwn + \
                        img[ihigh][jlow][2] * iup + \
                        img[ihigh][jhigh][2] * iup)/4

                img_new[i][j] = (int(r),int(g),int(b))
    return img_new