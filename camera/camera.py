"""Opens any attached camera(s) and streams frames to the server."""

import cv2
import socket

class Camera:

    SERVER_IP_DEFAULT = '192.168.1.156'
    SERVER_PORT_DEFAULT = 42069

    def __init__(self) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self) -> None:
        # TODO: Get all the cameras attached to the system, not just the first one.
        print('Opening camera 0...')
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            # TODO: Stream this frame to the server.
            # `frame` is a 2D array of RGB values (so technically a 3D array) each with a range of 0-255.
            print('Capturing frame...')
            _, frame = cap.read()

            # Display the resulting frame
            cv2.imshow('Webcam', frame)

            # Set the JPEG quality to 50 (lower quality, smaller file size)
            jpeg_encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
            _, buffer = cv2.imencode('.jpg', frame, jpeg_encode_params)
            image_data = buffer.tobytes()
            print(f'Image data size: {len(image_data)} bytes')
            self.__socket.sendto(image_data, (Camera.SERVER_IP_DEFAULT, Camera.SERVER_PORT_DEFAULT))

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def _send_frame(frame) -> None:
        # Send the frame to the frame aggregation server.
        pass

if __name__ == "__main__":
    print('Starting camera...')
    camera = Camera()
    camera.run()