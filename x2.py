from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import sys
import os
import imghdr

def is_valid_image(filename):
    image_type = imghdr.what(filename)
    return image_type is not None

if len(sys.argv) > 1:
  filename = sys.argv[1]
  if not is_valid_image(filename):
    print("The file you specified is not an image.")
    exit (1)
else:
  print("No file in arguments provided.")
  exit (1)

img_01 = Image.open(filename)
base_name, extension = os.path.splitext(filename)
newfilename = f"{base_name}_x2{extension}"

img_01_size = img_01.size
im2arr = np.array(img_01)

width=img_01_size[0]
height=img_01_size[1]
width1=img_01_size[0]
height1=img_01_size[1]

newimage=[]
column=[]
pom=0
row2=[]
for j in range (height):
  row=[]
  for i in range(width):
    if i==0:
      row.append([im2arr[j][i][0],im2arr[j][i][1],im2arr[j][i][2]])
    else:
      r1=float(im2arr[j][i-1][0])
      g1=float(im2arr[j][i-1][1])
      b1=float(im2arr[j][i-1][2])
      r2=float(im2arr[j][i][0])
      g2=float(im2arr[j][i][1])
      b2=float(im2arr[j][i][2])
      r3=int((r1+r2)/2)
      g3=int((g1+g2)/2)
      b3=int((b1+b2)/2)
      row.append([r3,g3,b3])
      row.append([im2arr[j][i][0],im2arr[j][i][1],im2arr[j][i][2]])
  column.append(row)
  
column2=[]  
width=len(column[0])
for j in range(height):
  row2=[]
  if j==0:
    column2.append(column[j])
  if j>0:
    for i in range(width):
      r1=float(column[j-1][i][0])
      g1=float(column[j-1][i][1])
      b1=float(column[j-1][i][2])
      r2=float(column[j][i][0])
      g2=float(column[j][i][1])
      b2=float(column[j][i][2])
      r3=int((r1+r2)/2)
      g3=int((g1+g2)/2)
      b3=int((b1+b2)/2)
      row2.append([r3,g3,b3])
    column2.append(row2)
    column2.append(column[j])
    
x=np.array(column2, dtype=np.uint8)
im = Image.fromarray(x)
# Enhance brightness
#enhancer = ImageEnhance.Brightness(im)
#im = enhancer.enhance(1.2)

# Enhance sharpness
enhancer = ImageEnhance.Sharpness(im)
im = enhancer.enhance(1.5)
# Enhance contrast
#enhancer = ImageEnhance.Contrast(im)
#im = enhancer.enhance(1.2)
im = im.filter(ImageFilter.MedianFilter(size=3))
im.save(newfilename)
