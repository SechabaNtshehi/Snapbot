import cv2 as cv
import numpy as np


class CropBot:
	def cropSnap(self, coordinates, in_file_path, out_file_path):

		image = cv.imread(in_file_path)
		roi_x, roi_y, roi_width, roi_height = coordinates['x'], coordinates['y'], coordinates['width'], coordinates['height']
		roi = image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

		image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB) #converts full image to rgb
		roi_rgb = cv.cvtColor(roi, cv.COLOR_BGR2RGB) #converts region of interest to rgb
		filename = out_file_path
		cv.imwrite(filename, roi)
