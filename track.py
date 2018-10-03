import cv2
import numpy as np
import datetime
from threading import Thread
from collections import deque
from object_colour import find_object_colour


class ThreadedWebcamStream:
    def __init__(self, src = 0):

        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target = self.update, args = ()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        self._end = datetime.datetime.now()

    def update(self):
        self._numFrames += 1
        self._end = datetime.datetime.now()

    def elapsed(self):
        return max([1, (self._end - self._start).total_seconds()])

    def fps(self):
        return self._numFrames/self.elapsed()


def track_object(colour_lower, colour_upper, shape = 'any', max_deque_len = 64):
    points = deque(maxlen = max_deque_len)

    stream = ThreadedWebcamStream().start()
    fps = FPS().start()

    while True:

        fps.update()

        frame = stream.read()
        frame = cv2.flip(frame, 1)
        if frame is None:
            break

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, colour_lower, colour_upper)
        mask = cv2.erode(mask, None, iterations = 3)
        mask = cv2.dilate(mask, None, iterations = 3)



        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        cv2.putText(mask, str(len(contours)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)
        cv2.imshow('Mask', mask)
        cv2.imshow('HSV', hsv)

        if len(contours) > 0:
            contour = max(contours, key = cv2.contourArea)

            moment = cv2.moments(contour)
            center = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00']))

            if cv2.contourArea(contour) > 150:
                if shape == 'circle':
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                if shape == 'rect':
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if shape == 'any':
                    polygon = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)
                    cv2.drawContours(frame, [polygon], -1, (0, 255, 0), 2)

                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        points.appendleft(center)

        for i in range(1, len(points)):

            if points[i - 1] is None or points[i] is None:
                continue

            thickness = int(np.sqrt(max_deque_len / float(i + 1)) * 2.5)
            cv2.line(frame, points[i - 1], points[i], (0, 0, 255), thickness)

        cv2.putText(frame, str(fps.fps()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            break


    stream.stop()
    fps.stop()

    cv2.destroyAllWindows()

if __name__ == '__main__':

    lower_range, upper_range = find_object_colour(10, 10, 10)
    track_object(lower_range, upper_range, shape  = 'rect')
