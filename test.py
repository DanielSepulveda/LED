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
import shutil

pattern = re.compile("(\d)*_(\d)*_(\d*)_big_img_(\d)*")
all_dicts = []
count = 0
cwd = os.getcwd()

def pdToXml(name, coordinates, size, img_folder):
    xml = ['<annotation>']
    xml.append("    <folder>{}</folder>".format(img_folder))
    xml.append("    <filename>{}</filename>".format(name))
    xml.append("    <source>")
    xml.append("        <database>Unknown</database>")
    xml.append("    </source>")
    xml.append("    <size>")
    xml.append("        <width>{}</width>".format(size["width"]))
    xml.append("        <height>{}</height>".format(size["height"]))
    xml.append("        <depth>3</depth>".format())
    xml.append("    </size>")
    xml.append("    <segmented>0</segmented>")

    for field in coordinates:
        xmin, ymin = max(0,field[0]), max(0,field[1])
        xmax = min(size["width"], field[0]+field[2])
        ymax = min(size["height"], field[1]+field[3])

        xml.append("    <object>")
        xml.append("        <name>Face</name>")
        xml.append("        <pose>Unspecified</pose>")
        xml.append("        <truncated>0</truncated>")
        xml.append("        <difficult>0</difficult>")
        xml.append("        <bndbox>")
        xml.append("            <xmin>{}</xmin>".format(int(xmin)))
        xml.append("            <ymin>{}</ymin>".format(int(ymin)))
        xml.append("            <xmax>{}</xmax>".format(int(xmax)))
        xml.append("            <ymax>{}</ymax>".format(int(ymax)))
        xml.append("        </bndbox>")
        xml.append("    </object>")
    xml.append('</annotation>')
    return '\n'.join(xml)

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
def generateArray(file):
    with open(file, "r") as f:
        arr = f.read().splitlines()
    
    dicts = []
    i = 0
    while i < len(arr):
        global count
        count+= 1
        name = arr[i]
        if (pattern.match(name)):
            val = "{}.jpg".format(name)
            try:
                ndict = dict()
                ndict["name"] = val

                img = mpimg.imread(os.path.join("dataset", val))

                # fig,ax = plt.subplots(1)
                # ax.imshow(img)

                (h, w, _) = img.shape
                i = i + 1
                q = int(arr[i])
                temp = []
                while (q > 0):
                    i = i + 1
                    rec = transformCordinates(arr[i], w, h)
                    # rect = patches.Rectangle(
                    #     (rec[0], rec[1]),rec[2],rec[3],
                    #     linewidth=1,
                    #     edgecolor='r',
                    #     facecolor='none')
                    # ax.add_patch(rect)
                    temp.append(rec)
                    q = q - 1
                i = i + 1
                # plt.show()
                ndict["annotations"] = temp
                ndict["size"] = {
                    'height': h,
                    'width': w
                }
                # dicts.append(ndict)
                all_dicts.append(ndict)
            except:
                print("{} not found...".format(val))
                i+=1
        else: i = i + 1

folder = glob.glob('./dataset/*.jpg')
folder = pd.Series(folder)
files = returnEllipseListFiles("labels")

for f in files:
    generateArray(f)

# print(len(folder))
# print(count)
# print(len(all_dicts))
# print(all_dicts[0])

for i in range(len(all_dicts)):
    f = all_dicts[i]
    f["xml"] = pdToXml(f["name"], f["annotations"], f["size"], "dataset")

res_dir = "result_dataset"

if not os.path.exists(res_dir):
    os.mkdir(res_dir)

for i in range(len(all_dicts)):
    f = all_dicts[i]
    try:
        if not os.path.isfile(os.path.join(res_dir, f["name"])):
            shutil.copy(os.path.join("dataset", f["name"]), res_dir)
        xmlfilename = f["name"].replace(".jpg", ".xml")
        if not os.path.isfile(os.path.join(res_dir, xmlfilename)):
            with open(os.path.join(res_dir, xmlfilename), "w") as temp_file:
                temp_file.write(f["xml"])
    except:
        print("error")
