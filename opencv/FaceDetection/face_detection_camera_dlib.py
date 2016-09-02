import cv2
import dlib
detector = dlib.get_frontal_face_detector()

cascPath = "haarcascade_frontalface_alt.xml"
# cascPath = "lbpcascade_frontalface.xml"
# cascPath = "haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640)
video_capture.set(4, 480)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dets = detector(gray, 1)
    # faces = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.06,
    #     minNeighbors=8,
    #     # minSize=(30, 30),
    #
    #     # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    # )

    # Draw a rectangle around the faces
    # for (x, y, w, h) in faces:
    for i, d in enumerate(dets):
        cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)


    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()