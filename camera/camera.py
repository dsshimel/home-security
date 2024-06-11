"""Opens any attached camera(s) and streams frames to the server."""

import cv2

class Camera:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        # TODO: Get all the cameras attached to the system.
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            # TODO: Stream this frame to the server.
            ret, frame = cap.read()

            # Display the resulting frame
            cv2.imshow('Webcam', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    camera = Camera()
    camera.run()