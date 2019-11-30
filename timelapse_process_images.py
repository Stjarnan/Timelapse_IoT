# import the necessary packages
from imutils.video import VideoStream
from imutils import paths
import progressbar
import argparse
import cv2
import os

# function to get the frame number from the image path
def get_number(imagePath):
	return int(imagePath.split(os.path.sep)[-1][:-4])

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, 
	help="Path to the input directory of image files")
ap.add_argument("-o", "--output", required=True, 
	help="Path to the output video directory")
ap.add_argument("-f", "--fps", type=int, default=30, 
	help="Frames per second of the output video")
args = vars(ap.parse_args())

# initialize the FourCC and video writer
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
writer = None

# grab the paths to the images, then initialize output file name and
# output path 
imagePaths = list(paths.list_images(args["input"]))
outputFile = "{}.avi".format(args["input"].split(os.path.sep)[2])
outputPath = os.path.join(args["output"], outputFile)
print("Building {}...".format(outputPath))

# initialize the progress bar
widgets = ["Building Video: ", progressbar.Percentage(), " ", 
	progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(imagePaths), 
	widgets=widgets).start()

# loop over all sorted input image paths
for (i, imagePath) in enumerate(sorted(imagePaths, key=get_number)):
	# load the image
	image = cv2.imread(imagePath)

	# initialize the video writer if needed
	if writer is None:
		(H, W) = image.shape[:2]
		writer = cv2.VideoWriter(outputPath, fourcc, args["fps"],
			(W, H), True)

	# write the image to output video
	writer.write(image)
	pbar.update(i)

# release the writer object
print("Cleaning up...")
pbar.finish()
writer.release()
