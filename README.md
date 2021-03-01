# photo-standardize

Ever seen a fancy-shmancy "Meet the Team" page with crisp, matching photos of all the big-shot employees? Worry no more: photo-standardize has got you covered! 

---

## Features
*requires Numpy and OpenCV*

- Single- or batch-image processing
- Automatic facial detection and centering
- Edge padding
- Replacement of greenscreen with background image
- Rotation
- Grayscaling
- Scaling
- Circle masking

---

# Examples

**Before:**
---
![face3](https://user-images.githubusercontent.com/76142641/109447804-87b94c80-7a12-11eb-891c-b7f254edd429.jpg)
![face1](https://user-images.githubusercontent.com/76142641/109447808-8851e300-7a12-11eb-8fff-02d273a5a9bd.jpg)
![face2](https://user-images.githubusercontent.com/76142641/109447809-88ea7980-7a12-11eb-9f03-8affc88923c5.jpg)

**After** `python standardize.py -f samples -r -15 -g -c -s 200 200`:

![img0](https://user-images.githubusercontent.com/76142641/109449094-93f2d900-7a15-11eb-86ee-10ae46d701a3.png)
![img1](https://user-images.githubusercontent.com/76142641/109449095-948b6f80-7a15-11eb-8242-a8e7eb73beb1.png)
![img2](https://user-images.githubusercontent.com/76142641/109449096-948b6f80-7a15-11eb-81ec-b44e2e6a6af8.png)

**Before:**
---
![kid](https://user-images.githubusercontent.com/76142641/109447805-8851e300-7a12-11eb-8560-f9da1255fde9.jpg)
![man](https://user-images.githubusercontent.com/76142641/109447806-8851e300-7a12-11eb-8069-6ace314f62cb.jpg)
![trump](https://user-images.githubusercontent.com/76142641/109447807-8851e300-7a12-11eb-8e01-5aab261f063f.jpg)

*I couldn't find any great greenscreen images, OK?*

**After** `python standardize.py -f samples -c -s 200 200 -b skybg.jpg`:

![img5](https://user-images.githubusercontent.com/76142641/109448785-cea84180-7a14-11eb-84bf-4313a1f07870.png)
![img3](https://user-images.githubusercontent.com/76142641/109448786-cf40d800-7a14-11eb-9109-7bd7fa9eb4b5.png)
![img4](https://user-images.githubusercontent.com/76142641/109448787-cf40d800-7a14-11eb-8538-c27ffd0663a9.png)

---

## Usage:

```
usage: standardize.py [-h] [-i IMGS] [-f FOLDER] [-o OUTPUT] [-p PADDING] [-b BACKGROUND] [-r ROTATION] [-g]
                      [-s SIZE SIZE] [-c]

Standardizes face images to create a uniform look.

optional arguments:
  -h, --help     show this help message and exit
  -i IMGS        paths to images to standardize
  -f FOLDER      path to a folder with images to standardize
  -o OUTPUT      name of output folder for standardized images
  -p PADDING     amount of pixels of padding around each face. default: 30
  -b BACKGROUND  path to background image. Images must be taken in front of a greenscreen for this option to work.
                 NOTE: ensure BG image is larger than greenscreen image
  -r ROTATION    rotate by the amount of degrees specified
  -g             makes images grayscale
  -s SIZE SIZE   scales all images to the specified X, Y value
  -c             outputs circular images
```
