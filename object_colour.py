import cv2

ref_point = []
clipping = False

def click_and_crop(event, x, y, flags, param):

    global ref_point, clipping

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        clipping = True

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        clipping = False


def find_object_colour(hue_sensitivity = 10, sat_sensitivity = 10, value_sensitivity = 10):

    stream = cv2.VideoCapture(0)

    while True:
        _, frame = stream.read()
        frame = cv2.flip(frame, 1)
        original_frame = frame.copy()

        cv2.putText(frame, 'Press <Space> to capture image', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
        cv2.imshow('Image', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 32:
            break

    stream.release()
    cv2.destroyWindow('Image')

    frame = original_frame.copy()

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', click_and_crop)

    while True:
        if len(ref_point) == 2:
            cv2.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 2)

        cv2.putText(frame, 'Select a ROI', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow('Image', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            frame = original_frame.copy()

        elif key == 32:
            break

    cv2.destroyAllWindows()

    blurred = cv2.GaussianBlur(original_frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    roi = hsv[min(ref_point[0][1], ref_point[1][1]) : max(ref_point[0][1], ref_point[1][1]),
              min(ref_point[0][0], ref_point[1][0]) : max(ref_point[0][0], ref_point[1][0]), :]

    mean = cv2.mean(roi)[: 3]

    if mean[1] < 40 < mean[2]:  # White object
        lower_range = (0, 0, 0)
        upper_range = (360, 40, 255)

    elif mean[2] < 40:  # Black object
        lower_range = (0, 0, 0)
        upper_range = (360, 255, 40)
    else:
        lower_range = (mean[0] - hue_sensitivity, mean[1] - sat_sensitivity, mean[2] - value_sensitivity)
        upper_range = (mean[0] + hue_sensitivity, 255, 255)

    return lower_range, upper_range
