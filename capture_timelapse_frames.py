# import the necessary packages
from imutils.video import VideoStream
from datetime import datetime
import argparse
import signal
import time
import cv2
import sys
import os

# function to handle keyboard interrupt
def signal_handler(sig, frame):
	print("You pressed `ctrl + c`! Your pictures are saved" \
		" in the output directory you specified.")
	sys.exit(0)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, 
	help="path to the output directory")
ap.add_argument("-d", "--delay", type=float, default=5.0, 
	help="delay in seconds between frames captured")
ap.add_argument("-p", "--display", type=int, default=0,
	help="boolean used to indicate if frames should be displayed")
args = vars(ap.parse_args())

# initialize the output path and create the output dir
outputDir = os.path.join(args["output"],
	datetime.now().strftime("%Y-%m-%d-%H%M"))
os.makedirs(outputDir)

# initialize the video stream and allow the camera sensor to warmup
print("warming up camera...")
vs = VideoStream(usePiCamera=True, resolution=(1920, 1280),
	framerate=30).start()
time.sleep(2.0)

# set the frame count
count = 0

# signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
print("Press `ctrl + c` to exit, or 'q' to quit if you have" \
	" the display option on.")

# loop over frames from the video stream
while True:
	# grab the next frame from the stream
	frame = vs.read()

	# draw the timestamp on the frame
	ts = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), 
		cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# write the current frame to output directory
	filename = "{}.jpg".format(str(count).zfill(16))
	cv2.imwrite(os.path.join(outputDir, filename), frame)

	# if the frame should be displayed to our screen
	if args["display"]:
		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break

	# increment the frame count and sleep for specified number of
	# seconds
	count += 1
	time.sleep(args["delay"])

# close any open windows and release the video stream pointer
print("cleaning up..")
if args["display"]:
	cv2.destroyAllWindows()
vs.stop()
