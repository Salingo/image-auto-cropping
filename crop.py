import os
import sys
from PIL import Image, ImageChops

CROP_FOLDER = sys.argv[1]

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0))) # Get the background color from the top left pixel
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

if __name__ == "__main__":
	files = os.listdir(CROP_FOLDER)
	for file in files:
		if file.split('.')[1] == 'png' or file.split('.')[1] == 'jpg' or file.split('.')[1] == 'jpeg':
			image = Image.open(CROP_FOLDER+file) # The image to be cropped
			new_image = trim(image)
			new_image.save(CROP_FOLDER+file) # Overwrite original files
			print("Cropped: "+file)