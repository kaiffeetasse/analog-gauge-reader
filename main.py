import os
import math

import cv2 as cv
import numpy as np
import statistics

BAR_MIN = 0.95
LINES_ABOVE_Y = 310


def measure_gauge_from_image(filename):
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        return -1

    dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    counter = 0
    angles = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if l[3] < LINES_ABOVE_Y:
                cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
                cv.putText(cdstP, str(counter), (l[2] + 5, l[3] + 5), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
                print("line " + str(counter) + ": " + str(l[0]) + ", " + str(l[1]))
                print("line " + str(counter) + ": " + str(l[2]) + ", " + str(l[3]))

                angle = math.degrees(math.atan2(l[0] - l[1], l[2] - [3]))
                print("line " + str(counter) + " angle = " + str(angle))
                angles.append(angle)

                counter = counter + 1

    cv.imshow("Source", src)
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    # cv.imshow(filename, cdstP)

    avg_angle = statistics.mean(angles)
    print("avg angle = " + str(int(avg_angle)) + "°")

    bar = 0.0175153 * avg_angle + 1.50967
    print("bar = " + str(bar))

    cv.waitKey()
    return 0


if __name__ == "__main__":

    dir = "gauge_images"

    for filename in os.listdir(dir):
        if filename.endswith(".jpg"):
            file_name = os.path.join(dir, filename)
            print(file_name)
            measure_gauge_from_image(file_name)
        else:
            continue
