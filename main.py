import logging
import os
import math
import cv2 as cv
import numpy as np
import statistics

BAR_MIN = 0.95
LINES_ABOVE_Y = 310

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_bar_from_angle(angle):
    bar = 0.0175153 * angle + 1.50967
    return bar


def measure_gauge_from_image(filename):
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        logger.error('Error opening image!')
        return -1

    dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdstP = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    counter = 0
    angles = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            line = linesP[i][0]

            if line[3] < LINES_ABOVE_Y:
                cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv.LINE_AA)
                cv.putText(cdstP, str(counter), (line[2] + 5, line[3] + 5), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

                logger.debug("line " + str(counter) + ": " + str(line[0]) + ", " + str(line[1]))
                logger.debug("line " + str(counter) + ": " + str(line[2]) + ", " + str(line[3]))

                angle = math.degrees(math.atan2(line[0] - line[1], line[2] - [3]))
                logger.debug("line " + str(counter) + " angle = " + str(angle))
                angles.append(angle)

                counter = counter + 1

    cv.imshow("Source", src)
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    # cv.imshow(filename, cdstP)

    avg_angle = statistics.mean(angles)
    logger.info("avg angle = " + str(int(avg_angle)) + "°")

    bar = get_bar_from_angle(avg_angle)
    logger.info("bar = " + str(bar))

    cv.waitKey()


if __name__ == "__main__":

    dir = "images/gauges"

    for filename in os.listdir(dir):
        if filename.endswith(".jpg"):
            file_name = os.path.join(dir, filename)

            logger.info(file_name)
            measure_gauge_from_image(file_name)
        else:
            continue
