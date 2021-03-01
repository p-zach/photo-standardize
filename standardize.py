import os
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Standardizes face images to create a uniform look.")

parser.add_argument("-i", action="append", dest="imgs", default=[], help="paths to images to standardize")
parser.add_argument("-f", action="store", dest="folder", help="path to a folder with images to standardize")
parser.add_argument("-o", action="store", dest="output", default="output", help="name of output folder for standardized images")

parser.add_argument("-p", action="store", type=int, dest="padding", default=30, help="amount of pixels of padding around each face. default: 30")
parser.add_argument("-b", action="store", dest="background", help="path to background image. Images must be taken in front of a greenscreen for this option to work. NOTE: ensure BG image is larger than greenscreen image")
parser.add_argument("-r", action="store", type=float, dest="rotation", help="rotate by the amount of degrees specified")
parser.add_argument("-g", action="store_true", default=False, dest="grayscale", help="makes images grayscale")
parser.add_argument("-s", action="store", dest="size", nargs=2, default=[], help="scales all images to the specified X, Y value")
parser.add_argument("-c", action="store_true", dest="circle", default=False, help="outputs circular images")

args = parser.parse_args()

imgs = []

if len(args.imgs) == 0 and args.folder is None:
    print("No images provided.")

#region Loading

# if image names were provided, load them.
if len(args.imgs) > 0:
    for imgName in args.imgs:
        if os.path.isfile(imgName):
            imgs.append(cv2.imread(imgName))
            print("Loaded file " + imgName)
        else:
            print("File \"{}\" could not be found.".format(imgName))

# if a folder with images was provided, load those.
if not(args.folder is None):
    if os.path.isdir(args.folder):
        files = [f for f in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, f))]
        for f in files:
            imgs.append(cv2.imread(os.path.join(args.folder, f)))
            print("Loaded file " + f)
    else:
        print("Folder \"{}\" could not be found.".format(args.folder))

# load the Haar cascade to detect the faces.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#endregion

#region Utils

# Finds and returns an ROI for the face in an image.
def findFace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(face) == 0:
        return None
    return face[0]

# Pads an ROI by a specified amount while ensuring it remains entirely within the larger image.
def padRoi(roi, exp, img):
    (x, y, w, h) = roi
    x = x - exp if x - exp >= 0 else 0
    y = y - exp if y - exp >= 0 else 0
    w = w + (exp * 2) if w + (exp * 2) < img.shape[1] else img.shape[1]
    h = h + (exp * 2) if h + (exp * 2) < img.shape[0] else img.shape[0]
    return (x, y, w, h)

# Crops an image to just the specified ROI.
def cropToRoi(img, roi):
    (x, y, w, h) = roi
    return img[y:y+h, x:x+w]

# Scales all images in a list to the specified size.
def scaleAll(listImgs, x, y):
    for i in range(len(listImgs)):
        listImgs[i] = cv2.resize(listImgs[i], (x, y), interpolation=cv2.INTER_CUBIC)

# Replaces the greenscreen in an image with the specified background image.
def replaceGreenscreenWithBackground(img, bg):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # specify range of greens accepted (hsv format)
    minGreen = np.array([60-10, 60, 60])
    maxGreen = np.array([60+10, 255, 255])

    # find green pixels
    greenMask = cv2.inRange(hsv, minGreen, maxGreen)
    # flip mask so now we have non-green pixels
    maskInverse = cv2.bitwise_not(greenMask)

    bgResized = bg[:img.shape[0], :img.shape[1]]
    # mask background so it only covers green pixels
    bgMasked = cv2.bitwise_and(bgResized, bgResized, mask=greenMask)
    # mask the image so it only shows non-green pixels
    fg = cv2.bitwise_and(img, img, mask = maskInverse)

    return cv2.add(bgMasked, fg)

# Rotates image
def rotate(img, deg):
    h, w = img.shape[:2]
    rot = cv2.getRotationMatrix2D((w / 2, h / 2), deg, 1)
    return cv2.warpAffine(img, rot, (w, h))

# Applies circular mask to an image
def circle(img):
    h, w = img.shape[:2]
    mask = np.zeros((h,w), np.uint8)
    circleImg = cv2.circle(mask, (int(w/2), int(h/2)), int(w/2), (255,255,255), thickness=-1)
    _, alpha = cv2.threshold(circleImg, 1, 255, cv2.THRESH_BINARY)
    if type(img[0,0]) is np.uint8:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    b, g, r = cv2.split(img)
    rgba = [b,g,r,alpha]
    return cv2.merge(rgba, 4)

# Writes images in list to output directory
def saveAll(listImgs):
    try:
        os.mkdir(os.path.join(os.getcwd(), args.output))
    except FileExistsError:
        pass
    count = 0
    for i in listImgs:
        name = "img" + str(count) + ".png"
        cv2.imwrite(os.path.join(args.output, name), i)
        count += 1

#endregion

# Crop all images so they show just the faces.
for i in range(len(imgs)):
    faceRoi = findFace(imgs[i])
    if faceRoi is None:
        print("Face not found in an image. Make sure lighting is good and face is unobscured.")
        continue
    faceRoi = padRoi(faceRoi, args.padding, imgs[i])
    imgs[i] = cropToRoi(imgs[i], faceRoi)

# Resizing
if len(args.size) == 2:
    scaleAll(imgs, int(args.size[0]), int(args.size[1]))
elif len(args.size) > 0: print("ERROR: Improper amount of scaling parameters.")

# Greenscreening
if not(args.background is None):
    bg = cv2.imread(args.background)
    for i in range(len(imgs)):
        imgs[i] = replaceGreenscreenWithBackground(imgs[i], bg)

# Rotating
if not(args.rotation is None):
    for i in range(len(imgs)):
        imgs[i] = rotate(imgs[i], args.rotation)

# Grayscaling
if args.grayscale:
    for i in range(len(imgs)):
        imgs[i] = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2GRAY)

# Circle-ing
if args.circle:
    for i in range(len(imgs)):
        imgs[i] = circle(imgs[i])

saveAll(imgs)