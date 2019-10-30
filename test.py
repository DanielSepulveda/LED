import glob
import numpy as np
import pandas as pd
from pathlib import Path
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import os
import math

def transformCordinates(cords, wmax, hmax):
    parsed_cords = [float(x) for x in cords.split()]
    a = parsed_cords[0]
    b = parsed_cords[1]
    theta = parsed_cords[2]
    x = parsed_cords[3]
    y = parsed_cords[4]
    nx = math.pow(math.pow(a, 2) * math.pow(math.cos(theta), 2) + math.pow(b, 2) * math.pow(math.sin(theta), 2), 0.5)
    ny = math.pow(math.pow(a, 2) * math.pow(math.sin(theta), 2) + math.pow(b, 2) * math.pow(math.cos(theta), 2), 0.5)
    # print(parsed_cords)

    nh = int(ny * 2)
    nw = int(nx * 2)

    ejex = int(x - nx)
    ejey = int(y - ny)

    if (ejex < 0):
        ejex = 0
    if (ejey < 0):
        ejey = 0
    if (ejex + nw > wmax - 1):
        nw = wmax - ejex - 1
    if (ejey + nh > hmax - 1):
        nh = hmax - ejey - 1


    ncords = [ejex, ejey, nw, nh]
    
    return ncords

def returnEllipseListFiles(path):
    return [str(f) for f in Path(path).glob('**/*-ellipseList.txt')]

# Read files
pattern = re.compile("(\d)*_(\d)*_(\d*)_big_img_(\d)*")
def generateArray(file):
    with open(file, "r") as f:
        arr = f.read().splitlines()
    
    dicts = []
    i = 0
    while i < len(arr):
        name = arr[i]
        if (pattern.match(name)):
            val = "{}.jpg".format(name)
            try:
                ndict = dict()
                ndict["name"] = val

                img = mpimg.imread(os.path.join("dataset", val))
                # imgplot = plt.imshow(img)
                # plt.show()
                fig,ax = plt.subplots(1)
                ax.imshow(img)

                (h, w, _) = img.shape
                i = i + 1
                q = int(arr[i])
                temp = []
                while (q > 0):
                    i = i + 1
                    rec = transformCordinates(arr[i], w, h)
                    rect = patches.Rectangle(
                        (rec[0], rec[1]),rec[2],rec[3],
                        linewidth=1,
                        edgecolor='r',
                        facecolor='none')
                    ax.add_patch(rect)
                    temp.append(arr[i])
                    q = q - 1
                i = i + 1
                plt.show()
                ndict["annotations"] = temp
                dicts.append(ndict)
            except:
                print("{} not found...".format(val))
                i+=1
        else: i = i + 1

pattern = re.compile("(\d)*_(\d)*_(\d*)_big_img_(\d)*")

folder = glob.glob('./dataset/*.jpg')
folder = pd.Series(folder)
files = returnEllipseListFiles("labels")

arr1 = generateArray(files[4])
