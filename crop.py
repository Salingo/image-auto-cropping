import os
import sys
import numpy as np
from PIL import Image, ImageChops

SOURCE_FOLDER = sys.argv[-2]
TRIM_GROUP_MODE = int(sys.argv[-1])

def trim_single(img):
	img_temp = img.convert('RGB')
	bg = Image.new(img_temp.mode, img_temp.size, img_temp.getpixel((0,0)))
	diff = ImageChops.difference(img_temp, bg)
	bbox = diff.getbbox()
	img_cropped = img.crop(bbox)
	return img_cropped

''' Trim all images in the SOURCE_FOLDER by the common minimum bbox '''
def trim_group(imgs):
	bboxs = []
	for img in imgs:
		img_temp = img.convert('RGB')
		bg = Image.new(img_temp.mode, img_temp.size, img_temp.getpixel((0,0)))
		diff = ImageChops.difference(img_temp, bg)
		bbox = diff.getbbox()
		bboxs.append(bbox)
	bboxs = np.array(bboxs)
	common_bbox = np.zeros((4))
	common_bbox[0] = np.min(bboxs, axis=0)[0]
	common_bbox[1] = np.min(bboxs, axis=0)[1]
	common_bbox[2] = np.max(bboxs, axis=0)[2]
	common_bbox[3] = np.max(bboxs, axis=0)[3]
	imgs_cropped = []
	for img in imgs:
		img = img.crop(common_bbox)
		imgs_cropped.append(img)
	return imgs_cropped


if __name__ == "__main__":
	file_names = os.listdir(SOURCE_FOLDER)
	images = []
	images_name = []
	for file_name in file_names:
		if file_name.split('.')[1] == 'png' or file_name.split('.')[1] == 'jpg' or file_name.split('.')[1] == 'jpeg':
			image = Image.open(os.path.join(SOURCE_FOLDER, file_name))
			if TRIM_GROUP_MODE:
				images.append(image)
				images_name.append(file_name)
			else:
				image_cropped = trim_single(image)
				image_cropped.save(os.path.join(SOURCE_FOLDER, file_name))
				print("\ncropped: "+file_name)
	if TRIM_GROUP_MODE:
		images_cropped = trim_group(images)
		for i in range(len(images_cropped)):
			images_cropped[i].save(os.path.join(SOURCE_FOLDER, images_name[i]))
